from elasticsearch import Elasticsearch
#from fastapi import FastAPI
#from typing import List, Union
#from pydantic import BaseModel
#import json 
from core.configs import elastic_settings
index_='crucial'
#NODE_NAME = 'crucial3'
es = Elasticsearch(hosts=elastic_settings.elastic_connection_string, verify_certs=False,
                   ssl_show_warn=False)
       
def get_query(name, brand_name):
    if brand_name is None or len(brand_name.strip()) == 0:
        baseQuery = {
            "query": {
                "match": {
                    "name": {'query':name}
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

def ids_from_elastic (name_, brand_name_, size):
    base_query= get_query(name_, brand_name_)
    result=es.search(index=index_, body= base_query ,size=size)
    max_score = result['hits']['max_score'] if result['hits']['max_score'] is not None else 0
    result_ids = list()
    for index, item in enumerate(result['hits']['hits']):
        if item['_score'] > (max_score * 0.5):
           result_ids.append(dict(doc_count=index, key=item['_source']['id']))
    return result_ids
    

    
