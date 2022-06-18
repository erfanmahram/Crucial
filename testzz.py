import pathlib
import time
import logzero
from bs4 import BeautifulSoup
from main import Extractor
from multiprocessing import Process as mp


def test_suggestion_extract():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('main.html'):
        soup = BeautifulSoup(pth.read_text(), 'lxml')
        result = Extractor().extract_main(soup)
        print(result)


def test_suggestion_extract2():
    result2 = Extractor().extract_branch()
    print(result2)


def test_suggestion_extract3():
    result3 = Extractor().extract_sub_branch()
    print(result3)


if __name__ == '__main__':
    logzero.logger.info('p1 started')
    p1 = mp(target=test_suggestion_extract())
    p1.start()
    logzero.logger.info('p2 started')
    p2 = mp(target=test_suggestion_extract2())
    p2.start()
    logzero.logger.info('p3 started')
    p3 = mp(target=test_suggestion_extract3())
    p3.start()
    p1.join()
    p2.join()
    p3.join()
