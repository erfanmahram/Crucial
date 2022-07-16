from soup_parser import get_suggestion_memorycow, get_suggestion_crucial
from unifier import suggestion_json_fixer
# from main import extract_main
import pathlib
from bs4 import BeautifulSoup
import requests
from soup_parser import get_memorycow_model_info, get_crucial_model_info
import click



def test_suggestion_extract():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('model_*.html'):
        soup = BeautifulSoup(pth.read_text(encoding='utf-8'), 'lxml')
        result = get_suggestion_crucial(soup)
        print(result)


def test_extract_main():
    path = pathlib.Path.cwd().joinpath('test')
    for pth in path.glob('main.html'):
        soup = BeautifulSoup(pth.read_text(), 'lxml')
        result = extract_main(soup)
        print(result)

def get_soup(source):
    if isinstance(source, str):
        response = requests.get(source)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        return soup
    elif isinstance(source, pathlib.Path):
        soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'lxml')
        return soup
    else:
        raise NotImplementedError


def decider():
    test_cases = [
        {
            'sourceId': 1,
            'soup': get_soup(
                'https://www.memorycow.co.uk/laptop/dell/inspiron-11-3000-series/dell-inspiron-11-3158-laptop')
        }, {
            'sourceId': 2,
            'soup': get_soup(pathlib.Path('test/disney-netpal'))
         }, {
            'sourceId': 2,
            'soup': get_soup(pathlib.Path('test/model_2.html'))
        }, {
            'sourceId': 2,
            'soup': get_soup('https://eu.crucial.com/compatible-upgrade-for/acer/aspire-3-a315-21')
        }
    ]
    for item in test_cases:

        if item['sourceId'] == 1:
            items = get_suggestion_memorycow(item['soup'])
            print(suggestion_json_fixer(items, 1))
        elif item['sourceId'] == 2:
            items = get_suggestion_crucial(item['soup'])
            print(suggestion_json_fixer(items, 2))
        else:
            raise NotImplementedError


if __name__ == '__main__':
    # result = decider("https://www.memorycow.co.uk/laptop/dell/inspiron-11-3000-series/dell-inspiron-11-3158-laptop")
    # decider()
    # with open('fixed-info.json', 'w') as w:
    #     w.write(json.dumps(final_json))
    source_id = click.prompt('enter source id', type=int)
    url = click.prompt('enter url', type=str)
    soup = get_soup(url)
    if source_id == 1:
        var = get_memorycow_model_info(soup)
        sugg = get_suggestion_memorycow(soup)
    elif source_id == 2:
        var = get_crucial_model_info(soup)
        sugg = get_suggestion_crucial(soup)
    print(var)
    print(sugg)
    print(suggestion_json_fixer(sugg, source_id))
