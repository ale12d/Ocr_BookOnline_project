import requests
from bs4 import BeautifulSoup
from fonc import *
import csv
import os

retain = 0
additional_page = 0
progress = 0
add_write = 'w'
pagecat = 0

header = ("product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
          "number_available", "product_description", "category", "review_rating", "image_url")

# Code html du site
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Création du dossier Livres
if not os.path.exists('Books'):
    os.mkdir('Books', 0o777)

if not os.path.exists('Image'):
    os.mkdir('Image', 0o777)

# Code html des catégories et catalogues des livres
list_categories = soup.find_all('div', attrs={'class': "side_categories"})

# Ajout des catégories et de ses URL dans une liste

list_cat, listURL_cat = get_cat_and_url(list_categories)

for n in range(30 + len(list_cat)):

    # Création du fichier csv + affichage de l'en-tête

    if retain == 0:
        pagecat = requests.get(listURL_cat[n - additional_page])
        add_write = 'w'
    soupcat = BeautifulSoup(pagecat.content, 'html.parser')
    list_catalog = soupcat.find_all('div', attrs={'class': "image_container"})

    with open("Books/" + list_cat[n - additional_page] + ".csv", add_write, encoding="utf-8", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',',)
        if retain == 0:
            writer.writerow(header)

        for b in list_catalog:

            url_book, title, upc, price_inc, price_exc, nb_avail, img , rating, pro_desc = get_product_info(b)
            # print(title.get_text())

            img_data = requests.get(url + img[6:]).content
            with open("Image/" + title.get_text().replace('/', '-').replace(':', '-').replace('\"', ' ').replace('*', ' ').replace('?', ' ') + '.jpg', 'wb') as handler:
                handler.write(img_data)

            progress = progress + 1
            print(str(progress / 10) + '%')

            # Ecriture des infos extraite dans le fichier csv
            data = [url_book, upc, title.get_text(), price_exc, price_inc, nb_avail, pro_desc, list_cat[n - additional_page], rating, img]
            writer.writerows([data])

    retain, add_write, pagecat, additional_page = get_additional_page(soupcat, listURL_cat, n, additional_page, retain, add_write, pagecat)
