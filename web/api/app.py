from fastapi import FastAPI, Form
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from schema import Query

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=True))


def create_app():
    app = FastAPI()
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    return app
