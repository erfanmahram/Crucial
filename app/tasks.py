from .celery import app
import requests
from bs4 import BeautifulSoup


@app.task(queue="crucial", exchange="crucial")
def fetchCrucial(url):
    # url = 'https://httpstat.us/500'
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')
    # return 1


@app.task(queue="memorycow", exchange="memorycow")
def fetchMemorycow(url):
    # url = 'https://httpstat.us/500'
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


