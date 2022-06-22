from politeness_manager import politeness_checker, Scheduler, NotPolite
import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Politeness
from datetime import timedelta
from bs4 import BeautifulSoup
import requests

scheduler = Scheduler()


def update_scheduler(connection_string):
    """
    update scheduler from politeness table
    :param connection_string:
    :return:
    """
    engine = create_engine(connection_string)
    with Session(engine) as session:
        updated_data = {}
        for row in session.query(Politeness):
            updated_data[row.TaskName] = timedelta(minutes=row.Interval)
        scheduler.update_politeness(updated_data)


@politeness_checker(scheduler=scheduler)
def fetchCrucial(url, source_id):
    assert source_id == 2, ValueError('Source Id mismatch')
    pass


@politeness_checker(scheduler=scheduler)
def fetchMemorycow(url, source_id):
    assert source_id == 1, ValueError('Source Id mismatch')
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'lxml')


if __name__ == '__main__':
    update_scheduler(db_config.connection_string)
    try:
        fetchMemorycow('https://www.memorycow.co.uk/laptop/alienware/m15-series/alienware-m15-r3-laptop')
        print('fetched one')
    except NotPolite as e:
        print(e)
    try:
        fetchMemorycow('https://www.memorycow.co.uk/laptop')
        print('fetched two')
    except NotPolite as e:
        print(e)
