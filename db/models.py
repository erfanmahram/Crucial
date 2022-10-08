import json
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import Column, MetaData, ForeignKey
from datetime import datetime, timedelta
import enum
from db.database import Base #.session 
import arrow
from inflection import camelize
from urllib.parse import quote


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
        data = json.loads(self._SuggestInfo)
        for i in data.get('ram', []):
            i['buy'] = f'https://torob.com/search/?category=523&query={quote(i["Title"])}'
        for i in data.get('ssd', []):
            i['buy'] = f'https://torob.com/search/?category=1016&query={quote(i["Title"])}'
        for i in data.get('externalSsd', []):
            i['buy'] = f'https://torob.com/search/?category=243&query={quote(i["Title"])}'
        return data

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


