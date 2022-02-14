import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re

def getItem_from_wikiInfoBox(url, infobox_item):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    lhs = soup.find_all('th', {"class":"infobox-label"}) # get lhs of the InfoBox
    lhs_bool = [c.text == infobox_item for c in lhs]
    rhs = soup.find_all('td', {"class":"infobox-data"}) # rhs of InfoBox
    rhs_text = [c.text for c in rhs]

    items = rhs_text[lhs_bool.index(True)]
    items = re.sub('\[[0-9]+]', '', items).split(', ') # remove references and split by comma
    items = [i[0].upper() + i[1:].lower() for i in items] # format capital letters
    return items

def get_wikiURL_from_disease(disease):
    wiki_wiki = wikipediaapi.Wikipedia('en') # english
    page_py = wiki_wiki.page(disease)
    return page_py.fullurl

def retrieveFacts(disease, fact):
    url = get_wikiURL_from_disease(disease)
    fact = '{}{}'.format(fact[0].upper(), fact[1:].lower()) # ensure correct formatting
    return getItem_from_wikiInfoBox(url, fact)

x = retrieveFacts('Heart Failure','Symptoms')