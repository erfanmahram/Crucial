import re
import json


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


def extract_main(soup):
    main_brand_list = list()
    main_brand_name = list()

    tag = soup.find_all("a", {"class": "small text-left button hollow secondary element_item"})

    for iterator in tag:
        main_brand_list.append('https://www.crucial.com' + iterator["href"])
        main_brand_name.append(iterator.text)

    return main_brand_name, main_brand_list
