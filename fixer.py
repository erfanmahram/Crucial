from models import Model, PageStatus
import db_config
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session
from collections import defaultdict

engine = create_engine(db_config.connection_string)

with Session(engine) as session:
    models = session.query(Model).filter(Model.Status == PageStatus.Finished).order_by(func.random()).order_by(
        Model.RetryCount.asc()).all()

    for model in models:
        fixed_json = defaultdict(list)
        for item in model.SuggestInfo:
            if item['Category'].lower() == 'memory' or item['Category'].lower() == 'ram':
                fixed_json['ram'].append(item)
            elif item['Category'].lower() == 'externalssd' or item['Category'].lower() == 'external ssd':
                fixed_json['externalSsd'].append(item)
            else:
                fixed_json['ssd'].append(item)
        if 'ram' not in model.SuggestInfo:
            fixed_json['ram'] = []
        if 'ssd' not in model.SuggestInfo:
            fixed_json['ssd'] = []
        if 'externalSsd' not in model.SuggestInfo:
            fixed_json['externalSsd'] = []
        model.SuggestInfo = fixed_json
        session.commit()
