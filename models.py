import json
from inflection import camelize
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import enum
import arrow


# def traverse(item: dict) -> dict:
#     if isinstance(item, dict):
#         to_return = dict()
#         for i in item:
#             to_return[camelize(i, False)] = traverse(item[i])
#         return to_return
#     if isinstance(item, str):
#         try:
#             if item.startswith('[') or item.startswith('{'):
#                 _d = json.loads(item)
#                 return traverse(_d)
#             else:
#                 return item
#         except:
#             return item
#     elif isinstance(item, list):
#         to_return = list()
#         for i in item:
#             to_return.append(traverse(i))
#         return to_return
#     elif isinstance(item, datetime):
#         return arrow.get(item).isoformat()
#     else:
#         return item


Base = declarative_base()


class Device(Base):
    __tablename__ = 'Devices'
    Id = Column(INT, primary_key=True)
    BrandName = Column(String)
    SubBrandName = Column(String)
    LastUpdate = Column(DateTime, default=None)


class DRam(Base):
    __tablename__ = 'DRam'
    DRamId = Column(INT, primary_key=True)
    Technology = Column(String(8), default=None)
    MaximumMemory = Column(String, default=None)
    StandardMemory = Column(String)
    Slot = Column(INT, default=1)
    CompatibleMemory = Column(String, default=None)
    LastUpdate = Column(DateTime, default=None)


class Storage(Base):
    __tablename__ = 'Storages'
    SSDId = Column(INT, primary_key=True)
    InternalStorage = Column(String)
    CompatibleSSD = Column(String, default=None)
    LastUpdate = Column(DateTime, default=None)


def create_db():
    connection_string = 'sqlite:///crucial_db.sqlite'
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import mssql

    print(CreateTable(Device.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(DRam.__table__).compile(dialect=mssql.dialect()))
    print(CreateTable(Storage.__table__).compile(dialect=mssql.dialect()))
    create_db()
