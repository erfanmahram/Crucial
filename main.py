#from elasticsearch import Elasticsearch
from fastapi import FastAPI
from typing import List, Union
import json
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
def search_info(name: Union[str, None] = None, brand_name:Union[str, None] = None):
	ids=searchelastic.ids_from_elastic (name, brand_name, size=100)
	model_result = session.query(Model, Brand, Category).join(Category, Category.Id == Model.CategoryId).join(
        Brand, Brand.Id == Category.BrandId).filter(Model.Id.in_([i['key'] for i in ids]), Model.Status==100).all()
	for model in model_result:
		  model_items=schemas.ModelShow.from_orm(model.Model)
		  brand_items=schemas.BrandShow.from_orm(model.Brand)
		  category_items=schemas.CategoryShow.from_orm(model.Category)
		  item = schemas.ResultShow(**model_items.dict(), **brand_items.dict(), **category_items.dict() )
		  infos.append(item)
		  
	return infos
@app.get("/product/")
def suggest_info(id :Union[int, None] = None ):
	if id is None:
		return json.dumps({"Page Not Found": 404}),404
	model = session.query(Model).filter(Model.Id == int(id), Model.Status == 100).first()
	if model is None:
		return json.dumps({"message": "Not Found", "statusCode": 404}), 404
	json_result = dict(suggestion=model.SuggestInfo, name=model.ModelName)
	return json.dumps(json_result, ensure_ascii=False)
    
	
	
    
    
       
