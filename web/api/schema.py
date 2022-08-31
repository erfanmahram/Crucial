import strawberry
from pydantic import typing
from strawberry.types import Info
from resolver import get_model, get_models
from scalar import Modelql


@strawberry.type
class Query:
    @strawberry.field
    async def models(self, info: Info) -> typing.List[Modelql]:
        """ Get all users """
        models_data_list = await get_models(info)
        return models_data_list

    @strawberry.field
    async def model(self, info: Info, model_id: int) -> Modelql:
        """ Get user by id """
        model_dict = await get_model(model_id, info)
        return model_dict
