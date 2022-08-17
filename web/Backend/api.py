try:
    from flask import app, Flask, Response, request, jsonify
    from flask_restful import Resource, Api, reqparse
    import elasticsearch
    from elasticsearch import Elasticsearch
    import datetime
    import concurrent.futures
    import requests
    import json
    import es_config
    from logzero import logger
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import db_config
    from models import Resource, Model, Category, Brand, PageStatus
    import os
except Exception as e:
    print("Modules Missing {}".format(e))

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = db_config.connection_string
db = SQLAlchemy(app)

# ------------------------------------------------------------------------------------------------------------

NODE_NAME = 'crucial'
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
                        "field": "id",
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
    res = es.search(index=NODE_NAME, size=15, body=baseQuery)
    result = list()
    res2 = list()
    for i in res['hits']['hits']:
        if i['_source']['brand_name'] not in result:
            result.append(i['_source']['brand_name'])
    for index, item in enumerate(result):
        res2.append(dict(doc_count=index, key=item))
    return dict(result=res2)


@app.route('/name', methods=['GET'])
def name():
    name = request.args.get('name', None)
    brandName = request.args.get('brand', None)
    baseQuery = get_query(name, brandName)
    res = es.search(index=NODE_NAME, size=15, body=baseQuery)
    result = list()
    for index, item in enumerate(res['hits']['hits']):
        result.append(dict(doc_count=index, key=item['_source']['name']))
    return dict(result=result)


@app.route('/search', methods=['GET', 'POST'])
def search():
    name = request.args.get('name', None)
    brandName = request.args.get('brand', None)
    baseQuery = get_query(name, brandName)
    res = es.search(index=NODE_NAME, size=15, body=baseQuery)
    result = list()
    for index, item in enumerate(res['hits']['hits']):
        result.append(dict(doc_count=index, key=item['_source']['id']))
    json_result = list()
    model_result = db.session.query(Model).filter(Model.Id.in_([i['key'] for i in result])).all()
    for model in model_result:
        category = db.session.query(Category).filter(Category.Id == model.CategoryId).first()
        brand = db.session.query(Brand).filter(Brand.Id == category.BrandId).first()
        json_result.append(
            dict(ModelName=model.ModelName, MaximumMemory=model.MaximumMemory, Slots=model.Slots,
                 StandardMemory=model.StandardMemory, StrgType=model.StrgType, CategoryName=category.CategoryName,
                 BrandName=brand.BrandName, ModelUrl=model.ModelUrl, MoreInfo=model.SuggestInfo))
    print(json_result)
    j = str(json_result)
    return j


project_dir = os.path.dirname(os.path.abspath(__file__))
my_files = r'/static/data/'
file_dir = project_dir + my_files


@app.route('/get_data', methods=['POST'])
def get_data_function():
    user = request.form['user']

    if user == 'two':

        json_file = file_dir + r'data_set_2.json'

        with open(json_file) as f:
            js_object = json.load(f)
            return jsonify(js_object)

    else:
        json_file = file_dir + r'data_set_1.json'

        with open(json_file) as f:
            js_object = json.load(f)
            return jsonify(js_object)


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

# api.add_resource(Controller, "/autocomplete")

if __name__ == '__main__':
    app.run(debug=True, port=4000)
