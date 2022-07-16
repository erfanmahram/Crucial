from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
PYTHON_ENV = os.getenv('PYTHON_ENV')

dev_connection_string = 'sqlite:///crucial_db.sqlite'
prod_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if PYTHON_ENV == 'prod':
    connection_string = prod_connection_string
else:
    connection_string = dev_connection_string
