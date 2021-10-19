import requests
from bs4 import BeautifulSoup
import csv

i = 0
n = 0

données = []
en_tete = ("product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
           "number_available", "product_description", "category", "review_rating", "image_url")

# Code html du site
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

listCat = []
listURLcat = []

# Création du fichier csv + affichage de l'en-tête
with open('Données.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)

    # Code html des catégories et catalogues des livres
    listCatalogue = soup.find_all('div', attrs={'class': "image_container"})
    listCategory = soup.find_all('div', attrs={'class': "side_categories"})

    for a in listCategory:
        for li in a.findAll('li'):
            urlCategory = "http://books.toscrape.com/" + li.find('a')["href"]
            listCat.append(li.get_text().replace("\n", "").strip())
            listURLcat.append(urlCategory)

    del listCat[0]
    del listURLcat[0]
    print("Choisir une catégorie")
    print(listCat)
    CategoryChoise = input()


    for n in range(len(listCat)):
        if CategoryChoise == listCat[n]:
            pagecat = requests.get(listURLcat[n])
            soupcat = BeautifulSoup(pagecat.content, 'html.parser')
            listCatalogue = soupcat.find_all('div', attrs={'class': "image_container"})

            for b in listCatalogue:
                # Code html du livre
                urlBook = "http://books.toscrape.com/catalogue/" + b.find('a')["href"][9:]

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
                img = soupbook.find('div', attrs={'class': "item active"}).find('img')["src"]
                rating = soupbook.find('p', attrs={'class': "instock availability"}).find_next_sibling('p')['class'][1]

                print(rating)
                print(title.get_text())

                # Ecriture des infos extraite dans le fichier csv
                données = [urlBook, upc, title.get_text(), priceExc, priceInc, nbAAv, descPro, CategoryChoise, rating, img]
                writer.writerows([données])
        elif CategoryChoise in listCat:
            n + 1

