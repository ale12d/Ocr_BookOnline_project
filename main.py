import requests
from bs4 import BeautifulSoup
import csv

données = []
en_tete = ("product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
           "number_available", "product_description", "category", "review_rating", "image_url")

# Code html du site
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Création du fichier csv + affichage de l'en-tête
with open('Données.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)

    # Code html des catégories catalogue des livres
    listCatalogue = soup.find_all('div', attrs={'class': "image_container"})
    listCategory = soup.find_all('ul', attrs={'class': "nav nav-list"})

    for a in listCategory:
        for li in a.findAll('li'):
            urlCategory = "http://books.toscrape.com/" + li.find('a')["href"]
            print(urlCategory)
            print(li.get_text())


    for b in listCatalogue:
        # Code html du livre
        urlBook = "http://books.toscrape.com/" + b.find('a')["href"]
        pagebook = requests.get(urlBook)
        soupbook = BeautifulSoup(pagebook.content, 'html.parser')

        # Extraction code html de la barre d'infos
        info = soupbook.find('table', attrs={'class': 'table table-striped'})

        # Extraction des infos
        title = soupbook.find('li', attrs={'class': "active"})
        upc = info.find(text="UPC").findNext('td').contents[0]
        priceInc = info.find(text="Price (incl. tax)").findNext('td').contents[0]
        priceExc = info.find(text="Price (incl. tax)").findNext('td').contents[0]
        nbAAv = info.find(text="Availability").findNext('td').contents[0]
        descPro = soupbook.find(text="Product Description").findNext('p').contents[0]
        category = 0

        # print(title.get_text())

        # Ecriture des infos extraite dans le fichier csv
        données = [urlBook, upc, title.get_text(), priceExc, priceInc, nbAAv, descPro, ]
        writer.writerows([données])