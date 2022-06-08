import json
from inflection import camelize
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import packer
import enum
import arrow


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


class Model(Base):
    __tablename__ = 'Models'
    Id = Column(INT, primary_key=True)
    CategoryId = Column(INT, nullable=False)
    ModelName = Column(String, default=None)
    ModelUrl = Column(String, default=None)
    MaximumMemory = Column(String, default=None)
    Slots = Column(String, default=None)
    StandardMemory = Column(String, default=None)
    MemSuggestInfo = Column(String, default=None)
    StrgType = Column(String, default=None)
    StrgSuggestInfo = Column(String, default=None)
    LastUpdate = Column(DateTime, default=datetime.utcnow())


def create_db():
    connection_string = 'sqlite:///crucial_db.sqlite'
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
