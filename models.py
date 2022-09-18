import json
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import enum
from db_config import connection_string
from logzero import logger
import timedalta_store
import arrow
from inflection import camelize

Base = declarative_base()


def traverse(item: dict) -> dict:
    if isinstance(item, dict):
        to_return = dict()
        for i in item:
            to_return[camelize(i, False)] = traverse(item[i])
        return to_return
    if isinstance(item, str):
        try:
            if item.startswith('[') or item.startswith('{'):
                _d = json.loads(item)
                return traverse(_d)
            else:
                return item
        except:
            return item
    elif isinstance(item, list):
        to_return = list()
        for i in item:
            to_return.append(traverse(i))
        return to_return
    elif isinstance(item, datetime):
        return arrow.get(item).isoformat()
    else:
        return item


class PageStatus(enum.IntEnum):
    ReadyToCrawl = 0
    NoInfo = 50
    Finished = 100
    NotFound = 404
    ServerError = 500


class Resource(Base):
    __tablename__ = 'Resources'
    Id = Column(INT, primary_key=True)
    ResourceName = Column(String, default=None)
    ResourceUrl = Column(String, default=None)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"ID: {self.Id}, R_Name: {self.ResourceName}"


class Brand(Base):
    __tablename__ = 'Brands'
    Id = Column(INT, primary_key=True)
    ResourceId = Column(INT, nullable=False)
    BrandName = Column(String, default=None)
    BrandUrl = Column(String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"ID: {self.Id}, B_Name: {self.BrandName}"


class Category(Base):
    __tablename__ = 'Category'
    Id = Column(INT, primary_key=True)
    ResourceId = Column(INT, nullable=False)
    BrandId = Column(INT, nullable=False)
    CategoryName = Column(String, default=None)
    CategoryUrl = Column(String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"ID: {self.Id}, C_Name: {self.CategoryName}"


class Model(Base):
    __tablename__ = 'Models'
    Id = Column(INT, primary_key=True)
    ResourceId = Column(INT, nullable=False)
    CategoryId = Column(INT, nullable=False)
    ModelName = Column(String, default=None)
    ModelUrl = Column(String, default=None)
    MaximumMemory = Column(String, default=None)
    Slots = Column(String, default=None)
    StandardMemory = Column(String, default=None)
    MemoryGuess = Column(String, default=None)
    StrgType = Column(String, default=None)
    _SuggestInfo = Column('SuggestInfo', String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    Indexed = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"ID: {self.Id}, R_ID: {self.ResourceId}, M_Name: {self.ModelName}"

    @property
    def SuggestInfo(self):
        return json.loads(self._SuggestInfo)

    @SuggestInfo.setter
    def SuggestInfo(self, a):
        if isinstance(a, str):
            self._SuggestInfo = a
        else:
            self._SuggestInfo = json.dumps(a, ensure_ascii=False)

    def as_dict(self, expose=False):
        hide = ['CreateDate', 'TodayLoad', 'WindowHead']
        d = {c.name: getattr(self, c.name) for c in self.table.columns if (expose or c.name not in hide)}
        return traverse(d)


class Politeness(Base):
    __tablename__ = "Politeness"
    TaskName = Column(String(32), primary_key=True)
    Interval = Column(INT, default=5)
    LastRun = Column(DateTime, default=datetime.utcnow())
    NextRun = Column(DateTime, default=datetime.utcnow() + timedelta(minutes=1))


def create_db():
    logger.info('Creating Database')
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    create_db()

    engine = create_engine(connection_string)
    with Session(engine) as session:
        logger.info('Setting Politeness')
        im = Politeness(TaskName='fetchCrucial', Interval=2)
        var1 = Politeness(TaskName='fetchMemorycow', Interval=1)
        if session.query(Politeness).filter(Politeness.TaskName == im.TaskName).first() is None:
            session.add(im)
        if session.query(Politeness).filter(Politeness.TaskName == var1.TaskName).first() is None:
            session.add(var1)
        logger.info('Adding Sources into Resource table!')
        r1 = Resource(Id=1, ResourceName='Memorycow', ResourceUrl='https://www.memorycow.co.uk/laptop',
                      LastUpdate=datetime.utcnow() - timedalta_store.POLITENESS_RESOURCE_CRAWL_INTERVAL)
        r2 = Resource(Id=2, ResourceName='Crucial', ResourceUrl='https://www.crucial.com/upgrades',
                      LastUpdate=datetime.utcnow() - timedalta_store.POLITENESS_RESOURCE_CRAWL_INTERVAL)
        if session.query(Resource).filter(Resource.Id == r1.Id).first() is None:
            session.add(r1)
        else:
            assert r1.ResourceUrl == session.query(Resource).filter(Resource.Id == r1.Id).first().ResourceUrl
        if session.query(Resource).filter(Resource.Id == r2.Id).first() is None:
            session.add(r2)
        else:
            assert r2.ResourceUrl == session.query(Resource).filter(Resource.Id == r2.Id).first().ResourceUrl
        session.commit()
