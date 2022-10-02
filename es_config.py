from dotenv import load_dotenv
import os

load_dotenv()
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASSWORD')
ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_INDEX_NAME = os.getenv('ES_INDEX_NAME')

elastic_connection_string = f"https://{ES_USER}:{ES_PASSWORD}@{ES_HOST}:{ES_PORT}"
