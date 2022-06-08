from main import suggestion_extract, extract_main
import pathlib
from bs4 import BeautifulSoup


def test_suggestion_extract():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('model_*.html'):
        soup = BeautifulSoup(pth.read_text(encoding='utf-8'), 'lxml')
        result = suggestion_extract(soup)

        print(result)


def test_extract_main():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('main.html'):
        soup = BeautifulSoup(pth.read_text(), 'lxml')
        result = extract_main(soup)
        print(result)
