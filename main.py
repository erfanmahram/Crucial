import re
from bs4 import BeautifulSoup
import json
import requests
import pathlib


def get_details_memorycow(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find(class_="technical-specification table width-100 border-1 colour-grey-light")
    product_title = soup.find('title')
    pattern = r'^[^\|]*'
    title = re.findall(pattern, product_title.text)
    toc = dict(title=title[0])
    for row in table.find_all('tr'):
        toc[f"{row.find_all('td')[0].text.strip()}"] = row.find_all('td')[1].text.strip()
    return toc


def get_items_memorycow(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'lxml')
    target_box = soup.find_all("a", {"class": "block font-size-18 fixed-font-size line-height-1pt3 colour-black "
                                              "font-weight-600 underline-on-hover"})
    counter = 0
    tod = list()
    for i in target_box:
        tod.append(get_details_memorycow(i['href']))
        counter += 1
    return tod


def suggestion_extract(soup):
    pattern = re.compile(r"var prodListJS(.*?)';$", re.MULTILINE | re.DOTALL)
    rawJ = soup.find_all('script', attrs={'type': 'text/javascript'}, text=pattern)
    pattern2 = r"var prodListJS(memory|ssd|Externalssd) = '(.*?)';$"
    ad = re.compile(r'\xe2\x80\xa2')
    result = dict()
    for item in rawJ:
        json_file = re.findall(pattern2, item.text, re.MULTILINE)
        assert len(json_file) == 1
        js = json.loads(json_file[0][1].encode('utf8').decode('unicode_escape'))
        for a in js:
            if 'specs' in a:
                a['specs'] = [f.strip() for f in ad.split(a['specs'])]
            # if a == 'specs':
            #     [f.strip() for f in ad.split(a)]
        result[json_file[0][0]] = js
    return result


# def test_suggestion_extract():
#     path = pathlib.Path.cwd().joinpath('test')
#     for pth in path.glob('model_*.html'):
#         soup = BeautifulSoup(pth.read_text(encoding='utf-8'), 'lxml')
#         result = suggestion_extract(soup)
#         print(result)
#
#
# def test_extract_main():
#     path = pathlib.Path.cwd().joinpath('test')
#     for pth in path.glob('main.html'):
#         soup = BeautifulSoup(pth.read_text(), 'lxml')
#         result = extract_main(soup)
#         print(result)


def extract_main(soup):
    main_brand_list = list()
    main_brand_name = list()
    tag = soup.find_all("a", {"class": "small text-left button hollow secondary element_item"})
    for iterator in tag:
        main_brand_list.append('https://www.crucial.com' + iterator["href"])
        main_brand_name.append(iterator.text)
    return main_brand_name, main_brand_list


def decider(url):
    items = None
    if "www.memorycow.co" in url:
        items = get_items_memorycow(
            "https://www.memorycow.co.uk/laptop/dell/inspiron-11-3000-series/dell-inspiron-11-3158-laptop")
    elif "eu.crucial.com" in url:
        # test suggestion extract
        path = pathlib.Path.cwd().joinpath('test')
        for pth in path.glob('model_*.html'):
            soup = BeautifulSoup(pth.read_text(encoding='utf-8'), 'lxml')
            items = suggestion_extract(soup)

        # test extract main
        path = pathlib.Path.cwd().joinpath('test')
        for pth in path.glob('main.html'):
            soup = BeautifulSoup(pth.read_text(), 'lxml')
            items = extract_main(soup)
            print(items)
    return items


def json_fixer(json_file):
    fixed_json = list()
    if isinstance(json_file, list):
        for item in json_file:
            if 'Product Type/Family' not in item:
                continue
            if item['Product Type/Family'] == 'RAM':
                try:
                    integrated_memory_suggestion = dict(Title=item['title'], Capacity=item['Memory Capacity'],
                                                        Speed=item['Speed (Data Rate)'],
                                                        ManufactureTech=item['Form Factor'], ModuleType=item['Module Type'],
                                                        Voltage=item['Memory Voltage'],
                                                        Specs=[item['CAS Latency'], item['Memory Voltage'],
                                                               item['Module Type'], item['Error Check'], item['Pins'],
                                                               item['Rank'], item['Chip Organization'], item['Form Factor'],
                                                               item['Speed (Data Rate)']],
                                                        Category=item['Product Type/Family'])
                except:
                    integrated_memory_suggestion = dict(Title=item['title'], Status='This item has Error')
                fixed_json.append(integrated_memory_suggestion)
            elif item['Product Type/Family'] == 'SSD':
                try:
                    integrated_storage_suggestion = dict(Title=item['title'], Capacity=item['SSD Capacity'],
                                                         Interface=item['SSD Host Interface'],
                                                         FormFactor=item['SSD Form Factor'],
                                                         Specs=[item['SSD Capacity'], item['SSD Host Interface'],
                                                                item['Read Speed'], item['Write Speed']],
                                                         Category=item['Product Type/Family'])
                except:
                    integrated_storage_suggestion = dict(Title=item['title'], Status='This item has Error')
                fixed_json.append(integrated_storage_suggestion)
    elif isinstance(json_file, dict):
        for item in json_file['memory']:
            try:
                integrated_memory_suggestion = dict(Title=item['title'], Capacity=item['total-capacity'],
                                                    Speed=item['speed'], ManufactureTech=item['technology'],
                                                    ModuleType=item['module-type'], Voltage=item['voltage'],
                                                    Specs=item['specs'], Category='memory')
            except:
                integrated_memory_suggestion = dict(Title=item['title'], Status='This item has Error')
            fixed_json.append(integrated_memory_suggestion)
        for item in json_file['ssd']:
            try:
                integrated_storage_suggestion = dict(Title=item['title'], Capacity=item['density-ssd'],
                                                     Interface=item['interface'], FormFactor=item['form-factor'],
                                                     Specs=item['specs'], Category='ssd')
            except:
                integrated_storage_suggestion = dict(Title=item['title'], Status='This item has Error')
            fixed_json.append(integrated_storage_suggestion)
    return fixed_json


if __name__ == '__main__':
    # result = decider("https://www.memorycow.co.uk/laptop/dell/inspiron-11-3000-series/dell-inspiron-11-3158-laptop")

    result = decider("https://eu.crucial.com/compatible-upgrade-for/acer/aspire-3-a315-21")

    final_json = json_fixer(result)

    # with open('fixed-info.json', 'w') as w:
    #     w.write(json.dumps(final_json))



    # with open('table-of-details.json', 'w') as w:
    #     w.write(json.dumps(result))
