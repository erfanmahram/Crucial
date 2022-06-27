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
def fetchCrucial(url, source_id):
    assert source_id == 2, ValueError('Source Id mismatch')
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'lxml')


@politeness_checker(scheduler=scheduler)
def fetchMemorycow(url, source_id):
    assert source_id == 1, ValueError('Source Id mismatch')
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
    with Session(engine) as session:
        resources = session.query(Resource).filter(
            Resource.LastUpdate + timedalta_store.POLITENESS_RESOURCE_CRAWL_INTERVAL < datetime.utcnow()).all()
    for resource in resources:
        if resource.Id == 1:
            try:
                soup = handler.call('fetch', resource.Id, resource.ResourceUrl, resource.Id)
                brands = handler.call('get_brands', resource.Id, soup)
                with Session(engine) as session:
                    for brand in brands:
                        _b = Brand(ResourceId=resource.Id, BrandName=brand['brand_name'].lower(),
                                   BrandUrl=brand['brand_url'])
                        if session.query(Brand).filter(Brand.ResourceId == _b.ResourceId).filter(
                                Brand.BrandName == _b.BrandName).filter(Brand.BrandUrl == _b.BrandUrl).first() is None:
                            session.add(_b)
                        else:
                            continue
                    session.query(Resource).filter(Resource.Id == resource.Id).update(
                        {Resource.LastUpdate: datetime.utcnow()})
                    session.commit()

            except NotPolite as np:
                logger.exception(np)
                continue

    # Crawling on Brands for Categories
    with Session(engine) as session:
        brands = session.query(Brand).filter(
            Brand.LastUpdate + timedalta_store.POLITENESS_BRAND_CRAWL_INTERVAL < datetime.utcnow()).filter(
            Brand.Status != PageStatus.Finished).limit(5).all()
    for brand in brands:
        try:
            soup = handler.call('fetch', brand.ResourceId, brand.BrandUrl, brand.ResourceId)
            categories = handler.call('get_categories', brand.ResourceId, soup)
            with Session(engine) as session:
                for category in categories:
                    _c = Category(BrandId=brand.Id, CategoryName=category['category_name'].lower(),
                                  CategoryUrl=category['category_url'], Status=PageStatus.ReadyToCrawl)
                    if session.query(Category).filter(Category.BrandId == _c.BrandId).filter(
                            Category.CategoryName == _c.CategoryName).filter(
                        Category.CategoryUrl == _c.CategoryUrl).first() is None:
                        session.add(_c)
                    else:
                        continue
                session.query(Brand).filter(Brand.Id == brand.Id).update(
                    {Brand.LastUpdate: datetime.utcnow(), Brand.Status: PageStatus.Finished})
                session.commit()

        except NotPolite as np:
            logger.exception(np)
            continue

    # # Crawling on Models
    # with Session(engine) as session:
    #     resources = session.query(Model).filter(
    #         Model.LastUpdate + timedalta_store.POLITENESS_MODEL_CRAWL_INTERVAL < datetime.utcnow()).filter(
    #         Model.Status != PageStatus.Finished).all()
    # for resource in resources:
    #     try:
    #         soup = handler.call('fetch', resource.Id, resource.ResourceUrl, resource.Id)
    #         brands = handler.call('get_brands', resource.Id, soup)
    #         with Session(engine) as session:
    #             for brand in brands:
    #                 _b = Brand(ResourceId=resource.Id, BrandName=brand['brand_name'].lower(),
    #                            BrandUrl=brand['brand_url'])
    #                 if session.query(Brand).filter(Brand.ResourceId == _b.ResourceId).filter(
    #                         Brand.BrandName == _b.BrandName).filter(Brand.BrandUrl == _b.BrandUrl).first() is None:
    #                     session.add(_b)
    #                 else:
    #                     continue
    #             session.query(Resource).filter(Resource.Id == resource.Id).update(
    #                 {Resource.LastUpdate: datetime.utcnow()})
    #             session.commit()
    #
    #     except NotPolite as np:
    #         logger.exception(np)
    #         continue


if __name__ == '__main__':
    handler.register('fetch', 1, fetchMemorycow)
    # handler.register('fetch', 2, fetchCrucial)
    handler.register('get_brands', 1, soup_parser.get_memorycow_brands)

    handler.register('get_categories', 1, soup_parser.get_memorycow_category)
    main()
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
