try:
    from flask import app, Flask, Response, request
    from flask_restful import Resource, Api, reqparse
    import elasticsearch
    from elasticsearch import Elasticsearch
    import datetime
    import concurrent.futures
    import requests
    import json
    import es_config
except Exception as e:
    print("Modules Missing {}".format(e))

app = Flask(__name__)
api = Api(app)

# ------------------------------------------------------------------------------------------------------------

NODE_NAME = 'crucial'
es = Elasticsearch(hosts=es_config.elastic_connection_string, verify_certs=False,
                   ssl_show_warn=False)

# ------------------------------------------------------------------------------------------------------------


"""
{
"wildcard": {
    "title": {
        "value": "{}*".format(self.query)
    }
}
}

"""


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.baseQuery = {
            "query": {
                "match": {
                    "brand_name": {
                        "query": "{}".format(self.query)
                    }
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

    def get(self):
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res


@app.route('/brand-name', methods=['GET'])
def brand_name():
    query = request.args.get('query', None)
    baseQuery = {
        "query": {
            "match": {
                "brand_name": {
                    "query": "{}*".format(query)
                }
            }
        },
        "aggs": {
            "auto_complete": {
                "terms": {
                    "field": "brand_id",
                    "order": {
                        "_count": "desc"
                    },
                    "size": 25
                }
            }
        }
    }
    res = es.search(index=NODE_NAME, size=10000, body=baseQuery)
    result = list()
    for index, item in enumerate(res['hits']['hits']):
        result.append(dict(doc_count=index, key=item['_source']['brand_name']))
    return dict(result=result)


@app.route('/name', methods=['GET'])
def name():
    query = request.args.get('query', None)
    brandName = brand_name()['result']
    baseQuery = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "brand_name": {
                                "query":  "{}*".format(brandName)
                            }
                        }
                    },
                    {
                        "match": {
                            "name": {
                                "query": "{}*".format(query)
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "auto_complete": {
                "terms": {
                    "field": "id",
                    "order": {
                        "_count": "desc"
                    },
                    "size": 25
                }
            }
        }
    }
    res = es.search(index=NODE_NAME, size=10000, body=baseQuery)
    result = list()
    for index, item in enumerate(res['hits']['hits']):
        result.append(dict(doc_count=index, key=item['_source']['name']))
    return dict(result=result)


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, "/autocomplete")

if __name__ == '__main__':
    app.run(debug=True, port=4000)
