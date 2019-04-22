from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.request
import random
from lxml.html import fromstring
import requests
import time
import re
import datetime


from DBOperations import DBOperations
from helpclasses import UrlList

# THIS CODE ITERATES THROUGH POSTAL CODES AND GETS URLS OF LISTINGS, STORES THEM IN A DATABASE


# FUNCTION TO GET PROXY LIST
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies


# GET PROXY LIST, NEEDED TO CHANGE PROXY FROM TIME TO TIME
proxies = get_proxies()
print(proxies)

# GET FAKE USERAGENT VIA FAKE_USERAGENT PACKAGE
ua = UserAgent()
headers = ua.random

# TEST PROXY
url = 'https://httpbin.org/ip'

proxyWorks = False
print("START")
while proxyWorks is False:
    global proxy
    print("Request")
    proxy = random.choice(proxies)
    try:
        print("TRY")
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        proxyWorks = True
        print(response.json())
    except:
        # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")

print("SUCCESS")
print(proxy)


# SET PROXY FOR SELENIUM
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxy,
    'ftpProxy': proxy,
    'sslProxy': proxy,
    'noProxy': ''  # set this value as desired
    })

driver = webdriver.Firefox(proxy=proxy)
driver.get("https://www.comparis.ch/immobilien/result")

# TYPE IN POSTAL CODE AND HIT ENTER
searchField = driver.find_element_by_id("SearchParams_LocationSearchString")
searchField.send_keys("8000")
searchField.send_keys(Keys.ENTER)

# WAIT 5 SECONDS AND GET CURRENT URL
time.sleep(5)
initialUrl = driver.current_url

print(initialUrl)
# FIND OUT HOW MANY PAGES THERE ARE
nrOfPages = int(driver.find_element_by_css_selector("ul.pagination li:nth-last-child(2) a").get_attribute("innerHTML"))
print("Nr of Pages = "+str(nrOfPages))

# PRESS PAGINATION NEXT BUTTON (NECESSARY TO GET THE SECOND PAGE URL, WHICH CAN BE USED TO GENERATE ALL REMAINING URLS)
nextButton = driver.find_element_by_css_selector('.pagination-next a')
nextButton.click()

# GET URL OF SECOND PAGE
time.sleep(5)
secondUrl = driver.current_url

# CREATE ALL REMAINING URLS
allUrls = [initialUrl, secondUrl]
plainUrl = re.sub('&page=1', '', secondUrl)

for i in range(2, nrOfPages):
    allUrls.append(plainUrl+"&page="+str(i))


# GET URLS OF LISTINGS
urlListings = []
for i in range(0, 2):  # normally range(0, len(urlList))
    try:
        page = urllib.request.urlopen(allUrls[i])  # connect to website
    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('a.title'):
        urlListings.append("https://www.comparis.ch"+a['href'])

print(urlListings)


# CHECK WHETHER URLS ARE IN UrlList already
checkedUrls = UrlList(DBOperations("kezenihi_srmidb"))
allCheckedUrls = checkedUrls.getAllUrls()
print(allCheckedUrls)

# REMOVE DOUBE ENTRIES
validUrls = [x for x in urlListings if x not in allCheckedUrls]
print("These are the valid URLS: ")
print(*validUrls, sep = ", ")

# INSERT NEW URLS
insertUrls = []
d = datetime.datetime.today()
for url in urlListings:
    insertUrls.append((url, 0, d.strftime('%Y-%m-%d')))

checkedUrls.insertNewUrls(insertUrls)


#
# addresses = []
#
# # GET INFOS ON LISTINGS
# for i in urlList:
#     try:
#         page = urllib.request.urlopen(i)  # connect to website
#     except:
#         print("An error occured.")
#
#     soup = BeautifulSoup(page, 'html.parser')
#
#     for a in soup.select('div.item-price.large strong'):
#         addresses.append(a)
#
# print(addresses)
