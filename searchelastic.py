from elasticsearch import AsyncElasticsearch
from core.configs import elastic_settings

index_=elastic_settings.es_node_name 

es = AsyncElasticsearch(hosts=elastic_settings.elastic_connection_string, verify_certs=False,
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
                        "order":  {"avg_score": "desc"},
                        "size": 25
                    },
                   "aggs": {
                	"avg_score": {
                    		"avg": {"script": "_score"}
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

async def ids_from_elastic (name_, brand_name_, size_):
    base_query= get_query(name_, brand_name_)
    result= await es.search(index=index_, body= base_query ,size=size_)
    max_score = result['hits']['max_score'] if result['hits']['max_score'] is not None else 0
    result_ids = list()
    for index, item in enumerate(result['hits']['hits']):
        if item['_score'] > (max_score * 0.5):
           result_ids.append(dict(doc_count=index, key=item['_source']['id']))
    return result_ids

async def brands_from_elastic (brand_name_, size_):
    base_query= get_query(None, brand_name_)
    result= await es.search(index=index_, body= base_query ,size=size_)
    return  result['aggregations']['auto_complete']['buckets']
    
async def names_from_elastic (name_, size_):
    base_query= get_query(name_,None)
    result= await es.search(index=index_, body= base_query ,size=size_)
    name_list=list()   
    for item in result['hits']['hits']:
    	name_list.append(item['_source']['name'])
    return  name_list    
    

    
