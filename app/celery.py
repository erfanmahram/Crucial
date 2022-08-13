from celery import Celery
from dotenv import load_dotenv
import os


load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS_CONNECTION_STRING = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

app = Celery('app',
             broker=REDIS_CONNECTION_STRING + '/9',
             backend=REDIS_CONNECTION_STRING + '/10',
             include=['app.tasks'])
app.conf.update(
    result_serializer='pickle',
    result_expires=3600,
    worker_prefetch_multiplier=1,
    accept_content=['application/json', 'application/x-python-serialize'],
    task_default_queue='crucial'
)
app.control.rate_limit('app.tasks.fetchCrucialModel', '1/m')
app.control.rate_limit('app.tasks.fetchMemorycowModel', '2/m')
app.control.time_limit('app.tasks.fetchCrucialModel', soft=60 * 60, hard=65 * 60, reply=True)
app.control.time_limit('app.tasks.fetchMemorycowModel', soft=60 * 60, hard=65 * 60, reply=True)


app.conf.broker_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}
app.conf.result_backend_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}

# two ques: [crucial and memorycow]
# prefetch = 1
# raitelimit = 1/m on each que
