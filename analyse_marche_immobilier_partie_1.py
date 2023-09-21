import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm

def get_all_pages():
    urls=[]
    Departement=['nouvelle-aquitaine','ile-de-france','occitanie','auvergne-rhone-alpes','grand-est','pays-de-la-loire','provence-alpes-cote-d-azur']
    
    for j in Departement:
        page_number=0
        for i in tqdm(range(10)):
            i= f"https://fr.foncia.com/achat/{j}/appartement/page-{page_number}"
            print(f'On est entrain de scrapper la page numéro {page_number+1}')
            page_number+=1
            urls.append(i)
    return urls

def appart_foncia(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content, "html.parser")

    offres=soup.find_all('div', {"class":"foncia-card-content-left"})
    data=[]
    
    for offre in offres:
        Prix=None
        Description=None
        Surface=None
        Adresse=None
        try:
            Prix=offre.find('div', {"class":"foncia-card-price"}).text.strip()
        except:
            pass
        try:
            Description=offre.find('span',{"class":"foncia-card-title-small-title"}).text.strip()
        except:
            pass
        try:
            Surface=offre.find('span', {"class":"foncia-card-surface ng-star-inserted"}).text.strip()
        except:
            pass
        try:
            Adresse=offre.find('p', {"class":"foncia-card-place"}).text.strip()
        except:
            pass
        data.append([Prix, Description, Surface, Adresse])
    return data

def apparts_foncia():
    pages=get_all_pages()
    data = []
    for page in pages:
        data += appart_foncia(url=page)
    df = pd.DataFrame(data, columns=["Prix", "Description", "Surface", "Adresse"])
    df.to_excel(r"...\estimation_immo.xlsx", index=False)
    print(f"Données sauvegardées dans estimation_immo.xlsx")

apparts_foncia()