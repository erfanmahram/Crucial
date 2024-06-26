from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from schema import Query
from elasticsearch import AsyncElasticsearch
import es_config
from sqlalchemy import select
from models import Model, Category, Brand
from session import get_session

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=True))
NODE_NAME = es_config.ES_INDEX_NAME
es = AsyncElasticsearch(hosts=es_config.elastic_connection_string, verify_certs=False, ssl_show_warn=False)


def get_query(name, brand_name):
    if brand_name is None or len(brand_name.strip()) == 0:
        baseQuery = {
            "query": {
                "match": {
                    "name": {'query': name}
                }
            }
        }
    elif name is None or len(name.strip()) == 0:
        baseQuery = {
            "query": {
                "match": {
                    "brand_name": {
                        "query": brand_name
                    }
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "brand_id",
                        "order": [
                            {
                                "score": "desc"

                            }, {
                                "_count": "desc"

                            }
                        ]
                    },
                    "aggs": {
                        "score": {
                            "max": {
                                "script": "_score"
                            }
                        }
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
                                    "query": brand_name
                                }
                            }
                        },
                        {
                            "match": {
                                "name": {
                                    "query": name
                                }
                            }
                        }
                    ]
                }
            }
        }
    return baseQuery


def create_app():
    app = FastAPI()
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    @app.get('/', include_in_schema=False)
    async def route():
        return RedirectResponse(url='/docs')

    @app.get('/brandName')
    async def brand_name(query, size=20):
        baseQuery = get_query(None, query)
        es_result = await es.search(index=NODE_NAME, size=size, body=baseQuery)
        async with get_session() as session:
            sql = select(Brand).filter(
                Brand.Id.in_([j['key'] for j in es_result['aggregations']['auto_complete']['buckets']]))
            agg_brand_name = (await session.execute(sql)).all()
        brands = {brand.Brand.Id: brand.Brand.BrandName for brand in agg_brand_name}
        agg_buck = dict()
        for item in es_result['aggregations']['auto_complete']['buckets']:
            if brands[item['key']] not in agg_buck.keys():
                agg_buck[brands[item['key']]] = item['doc_count']
            elif agg_buck[brands[item['key']]] < item['doc_count']:
                agg_buck[brands[item['key']]] = item['doc_count']
        result = [i for i in agg_buck.keys()]
        return dict(result=result)

    @app.get('/modelName')
    async def model_name(name, brandName='', size=20):
        baseQuery = get_query(name, brandName)
        res = await es.search(index=NODE_NAME, size=size, body=baseQuery)
        result = list()
        for index, item in enumerate(res['hits']['hits']):
            result.append(item['_source']['name'])
        return dict(result=result)

    @app.get('/search')
    async def search_models(name='', brandName='', size=100, _from=0):
        baseQuery = get_query(name, brandName)
        res = await es.search(index=NODE_NAME, size=size, from_=_from, body=baseQuery)
        result = list()
        result2 = dict()
        max_score = res['hits']['max_score'] if res['hits']['max_score'] is not None else 0
        for index, item in enumerate(res['hits']['hits']):
            if item['_score'] > (max_score * 0.5):
                result.append(dict(doc_count=index, key=item['_source']['id']))
                result2[item['_source']['id']] = index
        json_result = list()
        async with get_session() as session:
            sql = select(Model, Brand, Category).join(
                Category, Category.Id == Model.CategoryId).join(
                Brand, Brand.Id == Category.BrandId).filter(Model.Id.in_([i['key'] for i in result]))
            model_result = (await session.execute(sql)).all()
        for model in model_result:
            json_result.append(
                dict(modelId=model.Model.Id, modelName=model.Model.ModelName, maximumMemory=model.Model.MaximumMemory,
                     slots=model.Model.Slots,
                     standardMemory=model.Model.StandardMemory, storageType=model.Model.StrgType,
                     categoryName=model.Category.CategoryName,
                     brandName=model.Brand.BrandName, modelUrl=model.Model.ModelUrl))

        json_result.sort(key=lambda x: result2[x["modelId"]])
        # return json.dumps(json_result, ensure_ascii=False)
        return json_result

    return app
