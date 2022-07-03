import time
from politeness_manager import politeness_checker, Scheduler, NotPolite
import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Politeness
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import timedalta_store
from models import Resource, Model, Category, Brand, PageStatus
from datetime import datetime
from logzero import logger
import soup_parser
from events import Event
from requests.exceptions import HTTPError, RequestException
from unifier import suggestion_json_fixer

scheduler = Scheduler()
handler = Event()


def update_scheduler(connection_string):
    """
    update scheduler from politeness table
    :param connection_string:
    :return:
    """
    engine = create_engine(connection_string)
    with Session(engine) as session:
        updated_data = {}
        for row in session.query(Politeness):
            updated_data[row.TaskName] = timedelta(minutes=row.Interval)
        scheduler.update_politeness(updated_data)


@politeness_checker(scheduler=scheduler)
def fetchCrucial(url):
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'lxml')


@politeness_checker(scheduler=scheduler)
def fetchMemorycow(url):
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'lxml')


def main():
    """
    1: get resource
    2: get brands
    3: get categories
    4: get models
    """

    engine = create_engine(db_config.connection_string)

    # Crawling on Resource for Brands
    logger.info('Crawling on Resource table to get Brands')
    with Session(engine) as session:
        resources = session.query(Resource).filter(
            Resource.LastUpdate + timedalta_store.POLITENESS_RESOURCE_CRAWL_INTERVAL < datetime.utcnow()).all()
    logger.info(f"{len(resources)} Resources are ready to crawl")
    for resource in resources:
        try:
            logger.debug(f'getting soup for {resource.ResourceName}({resource.ResourceUrl})')
            soup = handler.call('fetch', resource.Id, resource.ResourceUrl)
            brands = handler.call('get_brands', resource.Id, soup)
            with Session(engine) as session:
                for brand in brands:
                    _b = Brand(ResourceId=resource.Id, BrandName=brand['brand_name'].lower().strip(),
                               BrandUrl=brand['brand_url'])
                    if session.query(Brand).filter(Brand.ResourceId == _b.ResourceId).filter(
                            Brand.BrandName == _b.BrandName).filter(Brand.BrandUrl == _b.BrandUrl).first() is None:
                        session.add(_b)
                        logger.debug(f"Brand with id: {_b.Id} and brand_name: {_b.BrandName} added")
                    else:
                        logger.error(f"Brand with id: {_b.Id} and brand_name: {_b.BrandName} is not None")
                        continue
                session.query(Resource).filter(Resource.Id == resource.Id).update(
                    {Resource.LastUpdate: datetime.utcnow()})
                session.commit()
                logger.warning('Session added to database')
        except NotImplementedError as nie:
            logger.exception(nie)
            continue
        except NotPolite as np:
            logger.exception(np)
            continue

    # Crawling on Brands for Categories
    logger.info('Crawling on Brands table to get Categories')
    with Session(engine) as session:
        brands = session.query(Brand).filter(
            Brand.LastUpdate + timedalta_store.POLITENESS_BRAND_CRAWL_INTERVAL < datetime.utcnow()).filter(
            Brand.Status != PageStatus.Finished).order_by(Brand.RetryCount.desc()).limit(5).all()
        logger.info(f"These brands {brands} are going to crawl")
    for brand in brands:
        try:
            with Session(engine) as session:
                logger.warning(f"add one more retry count to brandId {brand.Id}")
                session.query(Brand).filter(brand.Id == Brand.Id).update(
                    {Brand.RetryCount: brand.RetryCount + 1, Brand.LastUpdate: datetime.utcnow()})
                session.commit()
            try:
                logger.debug(f'getting soup for {brand.BrandName}({brand.BrandUrl})')
                soup = handler.call('fetch', brand.ResourceId, brand.BrandUrl)
            except HTTPError as he:
                if he.response.status_code == 404:
                    logger.error(f"Error 404 for brandId: {brand.Id} - ResourceId: {brand.ResourceId}")
                    brand.Status = PageStatus.NotFound
                elif he.response.status_code == 500:
                    logger.error(f"Error 500 for brandId: {brand.Id} - ResourceId: {brand.ResourceId}")
                    brand.Status = PageStatus.ServerError
                else:
                    logger.exception(he)
                    raise he

            categories = handler.call('get_categories', brand.ResourceId, soup)
            with Session(engine) as session:
                for category in categories:
                    _c = Category(BrandId=brand.Id, CategoryName=category['category_name'].lower().strip(),
                                  CategoryUrl=category['category_url'], ResourceId=brand.ResourceId)
                    if session.query(Category).filter(Category.BrandId == _c.BrandId).filter(
                            Category.CategoryName == _c.CategoryName).filter(
                        Category.CategoryUrl == _c.CategoryUrl).first() is None:
                        session.add(_c)
                        logger.debug(f"Category with id: {_c.Id} and category_name: {_c.CategoryName} added")
                    else:
                        logger.error(f"Category with id: {_c.Id} and category_name: {_c.CategoryName} is not None")
                        continue
                session.query(Brand).filter(Brand.Id == brand.Id).update(
                    {Brand.LastUpdate: datetime.utcnow(), Brand.Status: PageStatus.Finished})
                session.commit()
                logger.warning('Session Committed to database')

        except NotPolite as np:
            logger.exception(np)
            continue

    # Crawling on Categories for Models
    logger.info('Crawling on Categories table to get Models Name and Url')
    with Session(engine) as session:
        categories = session.query(Category, Brand).join(Brand, Brand.Id == Category.BrandId).filter(
            Category.LastUpdate + timedalta_store.POLITENESS_CATEGORY_CRAWL_INTERVAL < datetime.utcnow()).filter(
            Category.Status != PageStatus.Finished).order_by(Category.Id, Category.RetryCount.desc()).limit(5).all()
        logger.info(f"These categories {categories} are going to crawl")
    for category in categories:
        try:
            with Session(engine) as session:
                logger.warning(f"add one more retry count to categoryId {category.Category.Id}")
                session.query(Category).filter(category.Category.Id == Category.Id).update(
                    {Category.RetryCount: category.Category.RetryCount + 1, Category.LastUpdate: datetime.utcnow()})
                session.commit()
            try:
                logger.debug(f'getting soup for {category.Category.CategoryName}({category.Category.CategoryUrl})')
                soup = handler.call('fetch', category.Brand.ResourceId, category.Category.CategoryUrl)
            except HTTPError as he:
                if he.response.status_code == 404:
                    logger.error(f"Error 404 for CategoryId: {category.Id} - ResourceId: {category.ResourceId}")
                    category.Status = PageStatus.NotFound
                elif he.response.status_code == 500:
                    logger.error(f"Error 500 for CategoryId: {category.Id} - ResourceId: {category.ResourceId}")
                    category.Status = PageStatus.ServerError
                else:
                    logger.exception(he)
                    raise he

            models = handler.call('get_models', category.Brand.ResourceId, soup)
            with Session(engine) as session:
                for model in models:
                    _m = Model(CategoryId=category.Category.Id, ModelName=model['model_name'].lower().strip(),
                               ModelUrl=model['model_url'], ResourceId=category.Category.ResourceId)
                    if session.query(Model).filter(Model.CategoryId == _m.CategoryId).filter(
                            Model.ModelName == _m.ModelName).filter(
                        Model.ModelUrl == _m.ModelUrl).first() is None:
                        session.add(_m)
                        logger.debug(f"Model with id: {_m.Id} and model_name: {_m.ModelName} added")
                    else:
                        logger.error(f"Model with id: {_m.Id} and model_name: {_m.ModelName} is not None")
                        continue
                session.query(Category).filter(Category.Id == category.Category.Id).update(
                    {Category.LastUpdate: datetime.utcnow(), Category.Status: PageStatus.Finished})
                session.commit()
                logger.warning("Session Committed to database")

        except NotPolite as np:
            logger.exception(np)
            continue

    # Crawling on Models for info
    logger.info('Crawling on Models table to get Models info')
    with Session(engine) as session:
        models = session.query(Model).filter(
            Model.LastUpdate + timedalta_store.POLITENESS_MODEL_CRAWL_INTERVAL < datetime.utcnow()).filter(
            Model.Status != PageStatus.Finished).order_by(Model.RetryCount.asc()).limit(5).all()
        logger.info(f"These models {models} are going to crawl")
    for model in models:
        try:
            with Session(engine) as session:
                session.query(Model).filter(model.Id == Model.Id).update(
                    {Model.RetryCount: model.RetryCount + 1})
                session.commit()
                logger.warning(f"add one more retry count to modelId {model.Id}")
            try:
                logger.debug(f'getting soup for {model.ModelName}({model.ModelUrl})')
                soup = handler.call('fetch', model.ResourceId, model.ModelUrl)
            except HTTPError as he:
                if he.response.status_code == 404:
                    logger.error(f"Error 404 for ModelId: {model.Id} - ResourceId: {model.ResourceId}")
                    model.Status = PageStatus.NotFound
                elif he.response.status_code == 500:
                    logger.error(f"Error 500 for ModelId: {model.Id} - ResourceId: {model.ResourceId}")
                    model.Status = PageStatus.ServerError
                else:
                    logger.exception(he)
                    raise he
            except RequestException as re:
                logger.exception(re)
                raise re

            model_info = handler.call('get_models_info', model.ResourceId, soup)
            model_suggestion = handler.call('get_models_suggestion', model.ResourceId, soup)
            suggestion_info = suggestion_json_fixer(model_suggestion, model.ResourceId)
            with Session(engine) as session:
                _model = session.query(Model).filter(Model.Id == model.Id).first()
                if _model is None:
                    logger.error(f"This model is None: {_model}")
                    continue
                if len(model_info) > 0:
                    logger.info(f"adding/updating model info for modelId {model.Id}")
                    _model.LastUpdate = datetime.utcnow()
                    _model.Status = PageStatus.Finished
                    _model.MaximumMemory = model_info['Maximum Memory'].lower().strip()
                    _model.Slots = model_info['Number Of Memory Sockets'].lower().strip()
                    _model.StandardMemory = model_info['Maximum Memory Per Slot'].lower().strip()
                    try:
                        _model.StrgType = model_info['SSD Interface'].lower().strip()
                    except:
                        _model.StrgType = 'no info'
                    _model.SuggestInfo = suggestion_info
                else:
                    logger.error(f"No Info was found for modelId {model.Id}")
                    _model.Status = PageStatus.NoInfo
                    _model.LastUpdate = datetime.utcnow()
                session.commit()
                logger.warning("session committed to database")
        except NotPolite as np:
            logger.exception(np)
            continue
        except Exception as e:
            logger.exception(e)
            continue


if __name__ == '__main__':
    handler.register('fetch', 1, fetchMemorycow)
    handler.register('fetch', 2, fetchCrucial)
    handler.register('get_brands', 1, soup_parser.get_memorycow_brands)
    handler.register('get_brands', 2, soup_parser.get_crucial_brands)
    handler.register('get_categories', 1, soup_parser.get_memorycow_category)
    handler.register('get_categories', 2, soup_parser.get_crucial_category)
    handler.register('get_models', 1, soup_parser.get_memorycow_models)
    handler.register('get_models', 2, soup_parser.get_crucial_models)
    handler.register('get_models_info', 1, soup_parser.get_memorycow_model_info)
    handler.register('get_models_info', 2, soup_parser.get_crucial_model_info)
    handler.register('get_models_suggestion', 1, soup_parser.get_suggestion_memorycow)
    handler.register('get_models_suggestion', 2, soup_parser.get_suggestion_crucial)
    counter = 1
    while True:
        logger.info(f"run number {counter}")
        main()
        counter += 1
        logger.info(f"!!! 120 Seconds sleep for next run !!!")
        time.sleep(120)

    # update_scheduler(db_config.connection_string)
    # try:
    #     fetchMemorycow('https://www.memorycow.co.uk/laptop/alienware/m15-series/alienware-m15-r3-laptop')
    #     print('fetched one')
    # except NotPolite as e:
    #     print(e)
    # try:
    #     fetchMemorycow('https://www.memorycow.co.uk/laptop')
    #     print('fetched two')
    # except NotPolite as e:
    #     print(e)
