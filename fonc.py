from bs4 import BeautifulSoup
import requests

def get_cat_and_url(list_ctgrs):
    list = []
    listURL = []
    for a in list_ctgrs:
        for li in a.findAll('li'):
            url_category = "http://books.toscrape.com/" + li.find('a')["href"]
            list.append(li.get_text().replace("\n", "").strip())
            listURL.append(url_category)
    del list[0]
    del listURL[0]
    return list, listURL

def get_product_info(i):
    url_book = "http://books.toscrape.com/catalogue/" + i.find('a')["href"][9:]
    pagebook = requests.get(url_book)
    soupbook = BeautifulSoup(pagebook.content, 'html.parser')

    # Extraction code html de la barre d'infos
    info = soupbook.find('table', attrs={'class': 'table table-striped'})

    # Extraction des infos
    title = soupbook.find('li', attrs={'class': "active"})
    upc = info.find(text="UPC").findNext('td').contents[0]
    price_inc = info.find(text="Price (incl. tax)").findNext('td').contents[0]
    price_exc = info.find(text="Price (incl. tax)").findNext('td').contents[0]
    nb_avail = info.find(text="Availability").findNext('td').contents[0]
    img = soupbook.find('div', attrs={'class': "item active"}).find('img')["src"]
    rating = soupbook.find('p', attrs={'class': "instock availability"}).find_next_sibling('p')['class'][1]

    if soupbook.find(text="Product Description"):
        pro_desc = soupbook.find(text="Product Description").findNext('p').contents[0]
    else:
        pro_desc = "no description"

    return url_book, title, upc, price_inc, price_exc, nb_avail, img , rating, pro_desc

def get_additional_page(soupcat_fo, listURL_cat_fo, n_fo, additional_page_fo, retain_fo, add_write_fo, pagecat_sup):
    pager = soupcat_fo.find('li', attrs={'class': "next"})

    if pager:
        page_sup = listURL_cat_fo[n_fo - additional_page_fo][:-10] + pager.find('a')['href']
        additional_page_fo = additional_page_fo + 1
        retain_fo = 1
        add_write_fo = 'a'
        pagecat_sup = requests.get(page_sup)

    else:
        retain_fo = 0

    return retain_fo, add_write_fo, pagecat_sup, additional_page_fo
