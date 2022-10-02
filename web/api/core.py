import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Fast Api GraphQL Strawberry"
    PROJECT_VERSION: str = "0.0.1"
    HOST_HTTP: str = os.environ.get("HOST_HTTP", "https://")
    HOST_URL = "0.0.0.0"
    HOST_PORT = 5000
    BASE_URL: str = HOST_HTTP + HOST_URL + ":" + str(HOST_PORT)
    # POSTGRES_USER = "postgres"
    # POSTGRES_PASSWORD = "faisal"
    # POSTGRES_SERVER = "db_graphql"
    # POSTGRES_PORT = 5432
    # POSTGRES_DB = "graphql_db"
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
