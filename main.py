#from elasticsearch import Elasticsearch
from fastapi import FastAPI
from typing import List, Union
from sqlalchemy.orm import Session
from db import models
import schemas
from db.database import SessionLocal, engine
from db.models import Model, Category, Brand
import searchelastic

#models.Base.metadata.create_all(bind=engine)
# Dependency
#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#Session = Depends(get_db)
#session = Session
session=SessionLocal()
app = FastAPI()
infos=list()

@app.get("/search/", response_model=List[schemas.ResultShow]) 
def search_info(name_: Union[str, None] = None, brand_name_:Union[str, None] = None):
	ids=searchelastic.result_from_elastic (name_, brand_name_)
	model_result = session.query(Model, Brand, Category).join(Category, Category.Id == Model.CategoryId).join(
        Brand, Brand.Id == Category.BrandId).filter(Model.Id.in_([i['key'] for i in ids]), Model.Status==100).all()
	for model in model_result:
		  model_items=schemas.ModelShow.from_orm(model.Model)
		  brand_items=schemas.BrandShow.from_orm(model.Brand)
		  category_items=schemas.CategoryShow.from_orm(model.Category)
		  item = schemas.ResultShow(**model_items.dict(), **brand_items.dict(), **category_items.dict() )
		  infos.append(item)
		  
	return infos
	
	
    
    
       
