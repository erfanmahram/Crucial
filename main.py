import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testmodel import Brand, Branch

engine = create_engine('sqlite:///crucial_db.sqlite')
with Session(bind=engine) as session:
    def extract_main(soup):
        main_brand_list = list()
        main_brand_name = list()
        branch_links = list()
        branch_names = list()

        tag = soup.find_all("a", {"class": "small text-left button hollow secondary element_item"})

        for iterator in tag:
            main_brand_list.append('https://www.crucial.com' + iterator["href"])
            main_brand_name.append(iterator.text)
            importer = Brand(BrandName=iterator.text, BrandUrl='https://www.crucial.com' + iterator["href"])
            session.add(importer)
            session.commit()

        for mit in main_brand_list:
            res = requests.get(mit)
            mit_soup = BeautifulSoup(res.content, 'lxml')
            tag = mit_soup.find_all("div", {"class": "small-12 columns oem-alphabet-header"})
            for i in tag:
                mytag = i.find_all_next("a", {"class": "small text-left button hollow secondary element_item"})
                for j in mytag:
                    branch_names.append(j.text)
                    branch_links.append('https://www.crucial.com' + j["href"])
                    importer2 = Branch(BranchName=j.text, BranchUrl='https://www.crucial.com' + j["href"])
                    session.add(importer2)
                    session.commit()

        return main_brand_name, main_brand_list, branch_names, branch_links
