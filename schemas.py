from typing import List, Union
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
         
class BrandShow(BaseModel):
    BrandName : Union[str, None] = None #r
    class Config:
        orm_mode = True

class CategoryShow(BaseModel):
    CategoryName : Union[str, None] = None #r
    class Config:
        orm_mode = True

class ModelShow(BaseModel):
    ModelName : Union[str, None] = None #r
    ModelUrl : Union[str, None] = None #r
    MaximumMemory : Union[str, None] = None #r
    Slots : Union[str, None] = None #r
    StandardMemory : Union[str, None] = None #r
    StrgType : Union[str, None] = None #r 
    class Config:
        orm_mode = True

class ResultShow(BrandShow, CategoryShow, ModelShow):
     pass
     class Config:
          orm_mode = True
         





