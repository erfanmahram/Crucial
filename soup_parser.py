import re
from bs4 import BeautifulSoup
import json
import requests
import time
from logzero import logger


def get_memorycow_brands(soup):
    """
    Returns brand name and url as a list of dicts.
    :param soup:
    :return: [{"brand_name": "Asus", "brand_url": "https://www.memorycow.co.uk/laptop/asus"}]
    """
    links = list()
    brands = soup.find_all('a', class_='device-grid-item block text-center font-size-14 line-height-1pt4')
    for i in brands:
        links.append({"brand_name": i.find('div', class_='table-cell').text, "brand_url": i['href']})

    return links


def get_crucial_brands(soup):
    """
    Returns brand name and url as a list of dicts.
    :param soup:
    :return: [{"brand_name": "Asus", "brand_url": "https://www.crucial.com/upgrades/asus"}]
    """
    links = list()
    brands = soup.find_all('a', class_='small text-left button hollow secondary element_item')
    for i in brands:
        links.append(
            {"brand_name": i.text, "brand_url": 'https://www.crucial.com' + i['href']})

    return links


def get_memorycow_category(soup):
    """
    Returns category name and url as a list of dicts.
    :param soup:
    :return: [{"category_name": "Chromebook Series", "category_url":
               "https://www.memorycow.co.uk/laptop/toshiba/chromebook-series"}]
    """
    category = list()
    categories = soup.find_all('div', class_='columns margin-10 end')
    for i in categories:
        category.append({"category_name": i['data-title'], "category_url": i.contents[1]['href']})
    return category


def get_crucial_category(soup):
    """
    Returns category name and url as a list of dicts.
    :param soup:
    :return: [{"category_name": "ASUS All-in-One", "category_url":
               "https://www.crucial.com/upgrades/asus/asus-all-in-one"}]
    """
    category = list()
    categories = soup.find_all('a', class_='small text-left button hollow secondary element_item')
    for i in categories:
        category.append({"category_name": i.text, "category_url": 'https://www.crucial.com' + i['href']})
    return category


def get_memorycow_models(soup):
    """
    Returns model name and url as a list of dicts.
    :param soup:
    :return: [{"model_name": "apple macbook pro early 2011 - 13-inch 2.3ghz core i5", "model_url":
     "https://www.memorycow.co.uk/laptop/apple/2011-macbook-pro/apple-macbook-pro-early-2011-13-inch-2.3ghz-core-i5-laptop"}]
    """
    model = list()
    models = soup.find_all('div', class_='columns margin-b10 end')
    for i in models:
        model.append({"model_name": i['data-title'], "model_url": i.contents[1]['href']})
    return model


def get_crucial_models(soup):
    """
    Returns model name and url as a list of dicts.
    :param soup:
    :return: [{"model_name": "1015E", "model_url":
     "https://www.crucial.com/compatible-upgrade-for/asus/1015e"}]
    """
    model = list()
    models = soup.find_all('a', class_='small text-left button hollow secondary element_item')
    for i in models:
        model.append({"model_name": i.text, "model_url": 'https://www.crucial.com' + i['href']})
    return model


def get_memorycow_model_info(soup):
    """
    Returns model's info as a dictionary.
    :param soup:
    :return: {'Number Of Memory Sockets': ' 2', 'Maximum Memory': ' 3GB', 'Maximum Memory Per Slot': ' 1GB/2GB'}
    """
    table = soup.find(id="large-table")
    base_info = dict()
    if table:
        rows = table.find_all('td')
        for i in range(len(rows)):
            txt = rows[i].text.strip()
            if 'Maximum Memory Per Slot' in txt or 'Maximum Memory' in txt or 'SSD Interface' in txt or \
                    'Number Of Memory Sockets' in txt:
                base_info[txt if 'Slot' not in txt else 'Standard memory'] = rows[i + 1].text.strip()
    base_info['MemoryGuess'] = guess_memorycow_memory(table)
    return base_info


def guess_memorycow_memory(soup):
    guessed_info = list()
    rows = soup.find_all('td')
    for i in range(0, len(rows), 2):
        if 'memory' in rows[i].text.lower():
            key = rows[i].text.strip()
            key = key if key[-1] != ':' else key[:-1]
            value = rows[i + 1].text.strip()
            value = value if value[-1] != ':' else value[:-1]
            guessed_info.append(dict(key=key, value=value))
    return guessed_info


def guess_crucial_memory(soup):
    """

    :param soup:
    :return: [{"key": "240-pin DDR2 DIMM Banking", "value": "2 (2 banks of 1)"}]
    """
    table = soup.find_all('div', class_="small-6 colummns cell")
    guessed_info = list()
    for i in range(0, len(table), 2):
        key = table[i].text.strip()
        key = key if key[-1] != ':' else key[:-1]
        value = table[i + 1].text.strip()
        value = value if value[-1] != ':' else value[:-1]
        guessed_info.append(dict(key=key, value=value))
    return guessed_info


def get_crucial_model_info(soup):
    """
    Returns model's info as a dictionary.
    :param soup:
    :return: {'Slots:': '2', 'Maximum memory:': ' 3GB', 'Standard memory:': ' 1GB/2GB'}
    """
    table = soup.find(id="memorytabContainerId")
    base_info = dict()
    if table:
        rows = table.find_all('div', class_="small-6 colummns cell")
        for i in range(len(rows)):
            if 'Maximum memory:' in rows[i].text.strip():
                base_info['Maximum Memory'] = rows[i + 1].text.strip()
            if 'Slots:' in rows[i].text.strip():
                base_info['Number Of Memory Sockets'] = rows[i + 1].text.strip()
            if 'Standard memory:' in rows[i].text.strip():
                base_info['Standard memory'] = rows[i + 1].text.strip()
        if 'Standard memory' in base_info and 'Maximum memory' not in base_info:
            base_info['Maximum memory'] = 'no info'
        if 'Standard memory' in base_info and 'Slots' not in base_info:
            base_info['Slots'] = 'no info'
        base_info['MemoryGuess'] = guess_crucial_memory(soup)

    table = soup.find(id="storagetabContainerId")
    storage_table = table.find('div', class_='small-12 large-5 columns')
    if len(storage_table.find_all('p')) > 1:
        storage = ', '.join([i.text.strip() for i in storage_table.find_all('p')[1].find_all('b')])
    else:
        storage = 'no info'
    base_info['SSD Interface'] = storage

    return base_info


def get_suggestion_memorycow(soup):
    def get_details_memorycow(url):
        logger.info(f"getting json of this url: ({url})")
        time.sleep(2.5)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find(class_="technical-specification table width-100 border-1 colour-grey-light")
        product_title = soup.find('title')
        pattern = r'^[^\|]*'
        title = re.findall(pattern, product_title.text)
        toc = dict(title=title[0])
        for row in table.find_all('tr'):
            toc[f"{row.find_all('td')[0].text.strip()}"] = row.find_all('td')[1].text.strip()
        return toc

    target_box = soup.find_all("a", {"class": "block font-size-18 fixed-font-size line-height-1pt3 colour-black "
                                              "font-weight-600 underline-on-hover"})
    tod = list()  # table of details
    for i in target_box:
        tod.append(get_details_memorycow(i['href']))
    return tod


def get_suggestion_crucial(soup):
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
