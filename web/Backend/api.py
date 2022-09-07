from flask import Flask, request, make_response, jsonify
from flask_restful import Api
from elasticsearch import Elasticsearch
import json
import es_config
from flask_sqlalchemy import SQLAlchemy
import db_config
from models import Model, Category, Brand

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = db_config.connection_string
db = SQLAlchemy(app)

# ------------------------------------------------------------------------------------------------------------

NODE_NAME = es_config.ES_INDEX_NAME
es = Elasticsearch(hosts=es_config.elastic_connection_string, verify_certs=False,
                   ssl_show_warn=False)


# ------------------------------------------------------------------------------------------------------------


def get_query(name, brandName):
    if brandName is None or len(brandName.strip()) == 0:
        baseQuery = {
            "query": {
                "match": {
                    "name": "{}*".format(name)
                }
            }
        }
    elif name is None or len(name.strip()) == 0:
        baseQuery = {
            "query": {
                "match": {
                    "brand_name": {
                        "query": "{}*".format(brandName)
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
    else:
        baseQuery = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "brand_name": {
                                    "query": "{}*".format(brandName)
                                }
                            }
                        },
                        {
                            "match": {
                                "name": {
                                    "query": "{}*".format(name)
                                }
                            }
                        }
                    ]
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
    return baseQuery


@app.route('/brand-name', methods=['GET'])
def brand_name():
    query = request.args.get('query', None)
    baseQuery = get_query(None, query)
    es_result = es.search(index=NODE_NAME, size=15, body=baseQuery)
    agg_brand_name = {brand.Id: brand.BrandName for brand in db.session.query(Brand).filter(
        Brand.Id.in_([j['key'] for j in es_result['aggregations']['auto_complete']['buckets']])).all()}
    agg_buck = {agg_brand_name[item['key']]: item['doc_count'] for item in
                es_result['aggregations']['auto_complete']['buckets']}
    result = [k for k, v in sorted(agg_buck.items(), key=lambda item: item[1], reverse=True)]
    return dict(result=result)


@app.route('/name', methods=['GET'])
def name():
    name = request.args.get('name', None)
    brandName = request.args.get('brand', None)
    baseQuery = get_query(name, brandName)
    res = es.search(index=NODE_NAME, size=15, body=baseQuery)
    result = list()
    for index, item in enumerate(res['hits']['hits']):
        result.append(item['_source']['name'])
    return dict(result=result)


@app.route('/product', methods=['GET', 'POST'])
def product():
    id = request.args.get('query', None)
    if id is None:
        return make_response(jsonify("Page Not Found"), 404)
    model = db.session.query(Model).filter(Model.Id == int(id)).filter(Model.Status == 100).first()
    if model is None:
        return {"message": "Not Found", "statusCode": 404}, 404
    json_result = dict(suggestion=model.SuggestInfo, name=model.ModelName)
    return json.dumps(json_result, ensure_ascii=False)


@app.route('/search', methods=['GET', 'POST'])
def search():
    name = request.args.get('name', None)
    brandName = request.args.get('brand', None)
    baseQuery = get_query(name, brandName)
    res = es.search(index=NODE_NAME, size=100, body=baseQuery)
    result = list()
    result2 = dict()
    max_score = res['hits']['max_score'] if res['hits']['max_score'] is not None else 0
    for index, item in enumerate(res['hits']['hits']):
        if item['_score'] > (max_score * 0.5):
            result.append(dict(doc_count=index, key=item['_source']['id']))
            result2[item['_source']['id']] = index
    json_result = list()
    model_result = db.session.query(Model, Brand, Category).join(
        Category, Category.Id == Model.CategoryId).join(
        Brand, Brand.Id == Category.BrandId).filter(Model.Id.in_([i['key'] for i in result])).all()

    for model in model_result:
        json_result.append(
            dict(modelId=model.Model.Id, modelName=model.Model.ModelName, maximumMemory=model.Model.MaximumMemory,
                 slots=model.Model.Slots,
                 standardMemory=model.Model.StandardMemory, storageType=model.Model.StrgType,
                 categoryName=model.Category.CategoryName,
                 brandName=model.Brand.BrandName, modelUrl=model.Model.ModelUrl))

    json_result.sort(key=lambda x: result2[x["modelId"]])
    return json.dumps(json_result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
