from sqlalchemy import select
from sqlalchemy.orm import load_only
from session import get_session
from helper import get_only_selected_fields, get_valid_data, popper
from models import Model, Brand, Category
from scalar import Modelql


async def get_models(info):
    """ Get all models resolver """
    selected_fields = get_only_selected_fields(Model, info)
    async with get_session() as s:
        sql = select(Model, Brand, Category).join(Category.CategoryName, Category.Id == Model.CategoryId).join(
            Brand.BrandName, Brand.Id == Category.BrandId).filter(Model.Status == 100).order_by(Model.Id).limit(10)
        # db_models = (await s.execute(sql)).all()
        db_models = (await s.execute(sql)).all()  # todo limit(10)

    models_data_list = []
    for model in db_models:
        model_dict = get_valid_data(model.Model, Model)
        model_dict["categoryName"] = model.Category.CategoryName
        model_dict["brandName"] = model.Brand.BrandName
        model_dict = popper(model_dict, selected_fields)
        models_data_list.append(Modelql(**model_dict))

    return models_data_list


async def get_model(model_id, info):
    """ Get specific model by id resolver """
    selected_fields = get_only_selected_fields(Model, info)
    async with get_session() as s:
        sql = select(Model).options(load_only(*selected_fields)) \
            .filter(Model.Id == model_id).order_by(Model.ModelName)
        db_model = (await s.execute(sql)).scalars().unique().one()

    model_dict = get_valid_data(db_model, Model)
    return Modelql(**model_dict)
