import html

import requests
import value as value
from selenium import webdriver
chrome_path = r"C:\Users\Ruben\Documents\Python packages\chromedriver_win32.73\chromedriver.exe"
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import time
import re



c = requests.get('https://www.comparis.ch/immobilien/marktplatz/details/show/20597549').content
soup = BeautifulSoup(c, 'html.parser')

for i in range(1,20):
    dt = soup.find_all('dt')[i].string
    dd = soup.find_all('dd')[i].string
    print(dt)
    print(dd)

#dd = soup.find_all('dd').count()
#print(dd)
#print(soup.title.parent.title.text)

#RealValue = soup.find("dt", {"class":"label-text"}).string
#print(RealValue)

# dt = soup.find_all('dt').text
# print(dt)

