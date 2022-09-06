import json
from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import Column, MetaData, ForeignKey
from datetime import datetime, timedelta
import enum
#from db_config import connection_string
from db.database import Base #.session 
#from logzero import logger


#Base = declarative_base()


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

    def __repr__(self):#???
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

    def __repr__(self):#???
        return f"ID: {self.Id}, B_Name: {self.BrandName}"


class Category(Base):#???
    __tablename__ = 'Category'
    Id = Column(INT, primary_key=True)
    ResourceId = Column(INT, nullable=False)
    BrandId = Column(INT, nullable=False)
    CategoryName = Column(String, default=None)
    CategoryUrl = Column(String, default=None)
    Status = Column(INT, default=PageStatus.ReadyToCrawl)
    RetryCount = Column(INT, default=0)
    LastUpdate = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):#???
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

    #def __repr__(self):#???
    #    return f"ID: {self.Id}, R_ID: {self.ResourceId}, M_Name: {self.ModelName}"

    @property#????
    def SuggestInfo(self):
        return json.loads(self._SuggestInfo)

    @SuggestInfo.setter#????
    def SuggestInfo(self, a):
        if isinstance(a, str):
            self._SuggestInfo = a
        else:
            self._SuggestInfo = json.dumps(a, ensure_ascii=False)






