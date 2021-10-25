import requests
from bs4 import BeautifulSoup
import csv
import os

inter = 0
u = 0
progress = 0

header = ("product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
          "number_available", "product_description", "category", "review_rating", "image_url")

# Code html du site
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

list_cat = []
listURL_cat = []

# Création du dossier Livres
if not os.path.exists('Books'):
    os.mkdir('Books', 0o777)

if not os.path.exists('Image'):
    os.mkdir('Image', 0o777)

# Code html des catégories et catalogues des livres
list_catalog = soup.find_all('div', attrs={'class': "image_container"})
list_categories = soup.find_all('div', attrs={'class': "side_categories"})

# Ajout des catégories et de ses URL dans une liste
for a in list_categories:
    for li in a.findAll('li'):
        url_category = "http://books.toscrape.com/" + li.find('a')["href"]
        list_cat.append(li.get_text().replace("\n", "").strip())
        listURL_cat.append(url_category)
del list_cat[0]
del listURL_cat[0]

for n in range(30 + len(list_cat)):

    # Création du fichier csv + affichage de l'en-tête

    if inter == 0:
        pagecat = requests.get(listURL_cat[n-u])
        add_write = 'w'
    soupcat = BeautifulSoup(pagecat.content, 'html.parser')
    list_catalog = soupcat.find_all('div', attrs={'class': "image_container"})

    with open("Books/" + list_cat[n - u] + ".csv", add_write) as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        if inter == 0:
            writer.writerow(header)

        for b in list_catalog:
            # Code html du livre
            url_book = "http://books.toscrape.com/catalogue/" + b.find('a')["href"][9:]
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

            # print(title.get_text())

            img_data = requests.get(url + img[6:]).content
            with open("Image/" + title.get_text().replace('/', '-') + '.jpg', 'wb') as handler:
                handler.write(img_data)

            progress = progress+1
            print(str(progress/10 ) + '%')

            # Ecriture des infos extraite dans le fichier csv
            data = [url_book, upc, title.get_text(), price_exc, price_inc, nb_avail, pro_desc, list_cat[n - u], rating,
                    img]
            writer.writerows([data])

    pager = soupcat.find('li', attrs={'class': "next"})

    if pager:
        page_sup = listURL_cat[n-u][:-10] + pager.find('a')['href']
        u = u + 1
        inter = 1
        add_write = 'a'
        pagecat = requests.get(page_sup)

    else:
        inter = 0
