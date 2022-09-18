import os
from dotenv import load_dotenv
load_dotenv()
class Elastic_Settings:
     ES_USER = os.getenv('ES_USER')
     ES_PASSWORD = os.getenv('ES_PASSWORD')
     ES_HOST = os.getenv('ES_HOST')
     ES_PORT = os.getenv('ES_PORT')
     elastic_connection_string = f"https://{ES_USER}:{ES_PASSWORD}@{ES_HOST}:{ES_PORT}"
     es_node_name = os.getenv('NODE_NAME')
     
     
elastic_settings = Elastic_Settings()

class DB_Settings():
     DB_USER = os.getenv('DB_USER')
     DB_PASSWORD = os.getenv('DB_PASSWORD')
     DB_HOST = os.getenv('DB_HOST')
     DB_PORT = os.getenv('DB_PORT')
     DB_NAME = os.getenv('DB_NAME')
     PYTHON_ENV = os.getenv('PYTHON_ENV')
     dev_connection_string = 'sqlite:///crucial_db.sqlite'
     prod_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_settings = DB_Settings()


if db_settings.PYTHON_ENV == 'prod':
    connection_string = db_settings.prod_connection_string
else:
    connection_string = db_settings.dev_connection_string





