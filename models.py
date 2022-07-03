import json
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import enum
from db_config import connection_string
from logzero import logger


Base = declarative_base()


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


class Brand(Base):
    __tablename__ = 'Brands'
    Id = Column(INT, primary_key=True)
    ResourceId = Column(INT, nullable=False)
    BrandName = Column(String, default=None)
    BrandUrl = Column(String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())


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
    StrgType = Column(String, default=None)
    _SuggestInfo = Column('SuggestInfo', String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    @property
    def SuggestInfo(self):
        return json.loads(self._SuggestInfo)

    @SuggestInfo.setter
    def SuggestInfo(self, a):
        if isinstance(a, str):
            self._SuggestInfo = a
        else:
            self._SuggestInfo = json.dumps(a, ensure_ascii=False)


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
        r1 = Resource(Id=1, ResourceName='Memorycow', ResourceUrl='https://www.memorycow.co.uk/laptop')
        r2 = Resource(Id=2, ResourceName='Crucial', ResourceUrl='https://www.crucial.com/upgrades')
        if session.query(Resource).filter(Resource.Id == r1.Id).first() is None:
            session.add(r1)
        else:
            assert r1.ResourceUrl == session.query(Resource).filter(Resource.Id == r1.Id).first().ResourceUrl
        if session.query(Resource).filter(Resource.Id == r2.Id).first() is None:
            session.add(r2)
        else:
            assert r2.ResourceUrl == session.query(Resource).filter(Resource.Id == r2.Id).first().ResourceUrl
        session.commit()
