import requests
import urllib
import urllib.request
import time
from bs4 import BeautifulSoup

def make_soup(url):
    page = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(page, "html.parser")
    return soupdata

soup = make_soup("https://www.matchendirect.fr/france/")