import requests
from bs4 import BeautifulSoup

main_brand_list = list()
main_brands = list()

req_brands = requests.get('https://www.crucial.com/upgrades')
soup_brands = BeautifulSoup(req_brands.content, "lxml")


def extract_main(soup):

    with open(f'./html/main.html', 'w') as writer:

        writer.write(str(soup))

    with open(f'./html/main.html', 'r') as reader:

        brand_links = reader.read()
        inspector = BeautifulSoup(brand_links, 'lxml')
        tag = inspector.find_all("a", {"class": "small text-left button hollow secondary element_item"})

    for iterator in tag:
        main_brand_list.append('https://www.crucial.com' + iterator["href"])
        main_brands.append(iterator.text)


if __name__ == "__main__":
    extract_main(soup_brands)
    print(main_brands)
    print(main_brand_list)
