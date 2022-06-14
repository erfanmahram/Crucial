import re
from bs4 import BeautifulSoup
import json
import requests


def get_suggestion_memorycow(soup):
    def get_details_memorycow(url):
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
    tod = list()    # table of details
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





