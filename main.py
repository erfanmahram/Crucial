import time
import requests
from bs4 import BeautifulSoup


class Extractor:
    main_brand_list = list()
    main_brand_name = list()
    branch_links = list()
    branch_names = list()
    sb_names = list()
    sb_links = list()

    @staticmethod
    def extract_main(soup):

        tag = soup.find_all("a", {"class": "small text-left button hollow secondary element_item"})

        for iterator in tag:
            Extractor.main_brand_list.append('https://www.crucial.com' + iterator["href"])
            Extractor.main_brand_name.append(iterator.text)
        return Extractor.main_brand_name, Extractor.main_brand_list

    @staticmethod
    def extract_branch():
        for mit in Extractor.main_brand_list:
            time.sleep(2)
            try:
                time.sleep(2)
                res = requests.get(mit)
                mit_soup = BeautifulSoup(res.content, 'lxml')
                tag = mit_soup.find_all("div", {"class": "small-12 columns oem-alphabet-header"})
                for i in tag:
                    mytag = i.find_all_next("a", {"class": "small text-left button hollow secondary element_item"})
                    for j in mytag:
                        Extractor.branch_names.append(j.text)
                        Extractor.branch_links.append('https://www.crucial.com' + j["href"])

                return Extractor.branch_names, Extractor.branch_links

            except Exception as g:
                print('error', g)

    @staticmethod
    def extract_sub_branch():
        for jit in Extractor.branch_links:
            time.sleep(2)
            try:
                time.sleep(2)
                sub_branch_req = requests.get(f'https://www.crucial.com{jit}')
                sb_soup = BeautifulSoup(sub_branch_req.content, 'lxml')
                sb_tag = sb_soup.find_all("div", {"class": "small-12 columns oem-alphabet-header"})
                for item in sb_tag:
                    subtag = item.find_all_next("a", {"class": "small text-left button hollow secondary element_item"})
                    for finder in subtag:
                        Extractor.sb_names.append(finder.get_text())
                        Extractor.sb_links.append('https://www.crucial.com' + finder["href"])
                return Extractor.sb_names, Extractor.sb_links
            except Exception as e:
                print('error', e)
