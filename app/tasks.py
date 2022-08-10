from .celery import app
import requests


@app.task(queue="crucial", exchange="crucial")
def fetchCrucialModel(url):
    # url = 'https://httpstat.us/500'
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.text


@app.task(queue="memorycow", exchange="memorycow")
def fetchMemorycowModel(url):
    # url = 'https://httpstat.us/500'
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.text


if __name__ == '__main__':
    fetchCrucialModel('https://www.crucial.com/compatible-upgrade-for/hp---compaq/hp-22-b203la-all-in-one')
