import requests
from bs4 import BeautifulSoup

req_brands = requests.get('https://www.crucial.com/upgrades')

soup_brands = BeautifulSoup(req_brands.content, "html.parser")

brand_links = soup_brands.find_all("a", {"class": "small text-left button hollow secondary element_item"})

for iterator in brand_links:
    print(iterator.text)
    print('https://www.crucial.com' + iterator["href"])
