import db_config
from sqlalchemy import create_engine, select
from models import Base

engine_lite = create_engine(db_config.dev_connection_string)
engine_cloud = create_engine(db_config.prod_connection_string)

with engine_lite.connect() as conn_lite:
    with engine_cloud.connect() as conn_cloud:
        for table in Base.metadata.sorted_tables:
            data = [dict(row) for row in conn_lite.execute(select(table.c))]
            for d in data:
                try:
                    conn_cloud.execute(table.insert().values(d))
                except:
                    continue
