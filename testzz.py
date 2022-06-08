from main import extract_main
import pathlib
from bs4 import BeautifulSoup


def test_suggestion_extract():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('main.html'):
        soup = BeautifulSoup(pth.read_text(), 'lxml')
        result = extract_main(soup)
        print(result)

