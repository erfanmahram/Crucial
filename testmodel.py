from sqlalchemy import INT, FLOAT, String, Unicode, DateTime, UnicodeText, BOOLEAN, INTEGER, BIGINT, LargeBinary
from sqlalchemy import create_engine, Column, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Brand(Base):
    __tablename__ = 'Brands'
    Id = Column(INT, primary_key=True)
    BrandName = Column(String, default=None)
    BrandUrl = Column(String, default=None)


class Branch(Base):
    __tablename__ = 'Branchs'
    Id = Column(INT, primary_key=True)
    BranchName = Column(String, default=None)
    BranchUrl = Column(String, default=None)


connection_string = 'sqlite:///crucial_db.sqlite'
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
