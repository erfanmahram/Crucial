import asyncio
from fastapi import FastAPI
from typing import List, Union
import json
from db import models
import schemas
from db.database import async_session
from db.models import Model, Category, Brand
from sqlalchemy import select
from fastapi.responses import JSONResponse
import searchelastic
app = FastAPI()
infos=list()

@app.get("/search/", response_model=List[schemas.ResultShow]) 
async def search_info(name: Union[str, None] = None, brand_name:Union[str, None] = None):
	ids= await searchelastic.ids_from_elastic (name, brand_name, size_=100)
	async with async_session() as session:
		sql = select(Model, Brand, Category).join(
                	Category, Category.Id == Model.CategoryId).join(
                	Brand, Brand.Id == Category.BrandId).where(Model.Id.in_([i['key'] for i in ids]), Model.Status==100)
		model_result = (await session.execute(sql)).all()
			
	for model in model_result:
		  model_items=schemas.ModelShow.from_orm(model.Model)
		  brand_items=schemas.BrandShow.from_orm(model.Brand)
		  category_items=schemas.CategoryShow.from_orm(model.Category)
		  item = schemas.ResultShow(**model_items.dict(), **brand_items.dict(), **category_items.dict() )
		  infos.append(item)		  
	return infos
@app.get("/product/")
async def suggest_info(id :Union[int, None] = None, responses={
        400: {
              "description": "invalid request message"
        },
        404: {
              "description": "No user with this ID in the database",
        },} ):
	if id is None:
		#return json.dumps({"Page Not Found": 404}),404
		return JSONResponse (status_code=400, content={"message": "Bad Request!"})
	async with async_session() as session:
		sql = select(Model).where(Model.Id == int(id), Model.Status == 100)
		model = (await session.execute(sql)).first()
		
	if model is None:
		return JSONResponse (status_code=404, content={"message": "Not Found!"})
	result = dict(suggestion=model.Model.SuggestInfo, name=model.Model.ModelName)
	return result

@app.get("/brand-name")
async def brand_info(brand_name:Union[str, None] = None):
	brands_els = await searchelastic.brands_from_elastic ( brand_name, size_=100)
	async with async_session() as session:
		sql = select(Brand).where(Brand.Id.in_([item['key'] for item in brands_els]), Brand.Status==100)
		brand_db= (await session.execute(sql)).all()
	agg_brand_name=list()
	for brand in brand_db:
		agg_brand_name.append(brand.Brand.BrandName)
	result={'Result': agg_brand_name}     
	return dict(Result=agg_brand_name)
@app.get("/name")
async def name_info(name:Union[str, None] = None):
	names_els = await searchelastic.names_from_elastic ( name, size_=100)	 
	return dict(Result=names_els)    
	
	
    
    
       
