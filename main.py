def extract_main(soup):
    main_brand_list = list()
    main_brand_name = list()

    tag = soup.find_all("a", {"class": "small text-left button hollow secondary element_item"})

    for iterator in tag:
        main_brand_list.append('https://www.crucial.com' + iterator["href"])
        main_brand_name.append(iterator.text)

    return main_brand_name, main_brand_list
