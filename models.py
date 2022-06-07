import json
from inflection import camelize
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import enum
import arrow


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


Base = declarative_base()


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
    LastUpdate = Column(DateTime, default=datetime.utcnow())


class Category(Base):
    __tablename__ = 'Category'
    Id = Column(INT, primary_key=True)
    BrandId = Column(INT, nullable=False)
    CategoryName = Column(String, default=None)
    CategoryUrl = Column(String, default=None)
    LastUpdate = Column(DateTime, default=datetime.utcnow())


class ModelRam(Base):
    __tablename__ = 'Models (Ram)'
    Id = Column(INT, primary_key=True)
    CategoryId = Column(INT, nullable=False)
    ModelName = Column(String, default=None)
    ModelUrl = Column(String, default=None)
    MaximumMemory = Column(String, default=None)
    Slots = Column(String, default=None)
    StandardMemory = Column(String, default=None)
    MemSuggestInfo = Column(String, default=None)
    MemSuggestCL = Column(String, default=None)
    LastUpdate = Column(DateTime, default=datetime.utcnow())


class ModelStorage(Base):
    __tablename__ = 'Models (Storage)'
    Id = Column(INT, primary_key=True)
    CategoryId = Column(INT, nullable=False)
    ModelName = Column(String, default=None)
    ModelUrl = Column(String, default=None)
    StrgType = Column(String, default=None)
    StrgSuggestInfo = Column(String, default=None)
    LastUpdate = Column(DateTime, default=datetime.utcnow())


def create_db():
    connection_string = 'sqlite:///crucial_db.sqlite'
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import mssql

    print(CreateTable(Resource.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(Brand.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(Category.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(ModelRam.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(ModelStorage.__table__).compile(dialect=mssql.dialect()))
    create_db()
