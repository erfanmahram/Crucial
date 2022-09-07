import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch
import db_config
import es_config
from logzero import logger
from models import Model, Category, Brand


def index_data(engine):
    index_name = "crucial"
    es_client = Elasticsearch(hosts=es_config.elastic_connection_string, verify_certs=False,
                              ssl_show_warn=False)
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body={"settings": {"index": {"max_ngram_diff": 10}, "analysis": {
            "analyzer": {"autocomplete": {"tokenizer": "autocomplete", "filter": ["lowercase"]},
                         "autocomplete_search": {"tokenizer": "standard", "filter": ["lowercase"]}},
            "tokenizer": {
                "autocomplete": {"type": "ngram", "min_gram": 2, "max_gram": 12}}}}, "mappings": {"properties": {
            "name": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete"},
            "brand_name": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"}}}})
    with Session(engine) as session:
        models = session.query(Model).filter(Model.Status == 100).filter(Model.Indexed == 0).limit(1000).all()
    if len(models) == 0:
        return
    logger.info(f"{len(models)} Models are ready to add to index")
    actions = []
    with Session(engine) as session:
        for row in models:
            action = {"index": {"_index": 'crucial', "_id": row.Id}}
            model_doc = {
                "id": int(row.Id),
                "name": row.ModelName,
                "brand_name": session.query(Category, Brand).join(Brand, Brand.Id == Category.BrandId).filter(
                    Category.Id == row.CategoryId).first().Brand.BrandName,
                "brand_id": session.query(Category, Brand).join(Brand, Brand.Id == Category.BrandId).filter(
                    Category.Id == row.CategoryId).first().Brand.Id,
            }
            actions.append(action)
            actions.append(model_doc)
    bulk = es_client.bulk(index=index_name, body=actions)
    indexed_update = list()
    for item in bulk['items']:
        if 200 <= item['index']['status'] < 300:
            indexed_update.append(int(item['index']['_id']))
    with Session(engine) as session:
        moquery = session.query(Model).filter(Model.Id.in_(indexed_update)).update({Model.Indexed: 5})
        session.commit()
    result = es_client.count(index=index_name)
    print(result['count'])


if __name__ == '__main__':
    engine = create_engine(db_config.connection_string)
    while True:
        try:
            index_data(engine)
            print(engine.pool.status())
            time.sleep(61)
        except Exception as e:
            logger.exception(e)
            time.sleep(61)
            continue
