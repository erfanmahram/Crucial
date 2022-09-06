from typing import List, Union
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
         
class BrandShow(BaseModel):
    BrandName : Union[str, None] = None #r
    #BrandUrl : Union[str, None] = None 
    #Status :int ##?? Column(INT, default=PageStatus.ReadyToCrawl)
    #RetryCount :int 
    #LastUpdate :datetime
    class Config:
        orm_mode = True

class CategoryShow(BaseModel):
    #Id :int 
    #ResourceId :int
    #BrandId : Column(INT, nullable=False)
    CategoryName : Union[str, None] = None #r
    #CategoryUrl : Union[str, None] = None
    #Status : int
    #RetryCount :int 
    #LastUpdate = datatime

    class Config:
        orm_mode = True
        
        
        
class ModelShow(BaseModel):
    #Id : int #r
    #ResourceId : int
    #CategoryId : int  
    ModelName : Union[str, None] = None #r
    ModelUrl : Union[str, None] = None #r
    MaximumMemory : Union[str, None] = None #r
    Slots : Union[str, None] = None #r
    StandardMemory : Union[str, None] = None #r
    #MemoryGuess : Union[str, None] = None
    StrgType : Union[str, None] = None #r 
    #SuggestInfo: int  #Column('SuggestInfo', String, default=None)
    #Status : int  #Column(INT, default=PageStatus.ReadyToCrawl)
    #RetryCount: int # = Column(INT, default=0)
    #Indexed: int #Column(INT, default=0)
    #LastUpdate: datatime # = Column(DateTime, default=datetime.utcnow())
    class Config:
        orm_mode = True

class ResultShow(BrandShow, CategoryShow, ModelShow):
     pass
     class Config:
          orm_mode = True
         





