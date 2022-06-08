from main import suggestion_extract
import pathlib
from bs4 import BeautifulSoup


def test_suggestion_extract():
    path = pathlib.Path.cwd().joinpath('/test')

