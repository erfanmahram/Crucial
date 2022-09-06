import strawberry
from pydantic import typing
from strawberry.types import Info
from resolver import get_model, get_models
from scalar import ModelqlType
from graphql import GraphQLError


@strawberry.type
class Query:
    @strawberry.field
    async def models(self, info: Info) -> typing.List[ModelqlType]:
        """ Get all users """
        models_data_list = await get_models(info)
        return models_data_list

    @strawberry.field
    async def model(self, info: Info, model_id: int) -> ModelqlType:
        """ Get user by id """
        try:
            model_dict = await get_model(model_id, info)
            return model_dict
        except:
            info.context['response'].status_code = 401
            raise GraphQLError('Model Id ' + str(model_id) + ' Not Found!')
