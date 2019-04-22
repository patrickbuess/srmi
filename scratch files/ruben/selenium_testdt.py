from selenium import webdriver
chrome_path = r"C:\Users\Ruben\Documents\Python packages\chromedriver_win32.73\chromedriver.exe"
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import time
import re
import csv


# OPEN Chrome TO NAVIGATE WEBSITE
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.comparis.ch/immobilien/result")
assert "Immobilien" in driver.title

# TYPE IN POSTAL CODE AND HIT ENTER
searchField = driver.find_element_by_id("SearchParams_LocationSearchString")
searchField.send_keys("8000")
searchField.send_keys(Keys.ENTER)

# WAIT 5 SECONDS AND GET CURRENT URL
time.sleep(0)
initialUrl = driver.current_url

print(initialUrl)
# FIND OUT HOW MANY PAGES THERE ARE
nrOfPages = int(driver.find_element_by_css_selector("ul.pagination li:nth-last-child(2) a").get_attribute("innerHTML"))
print("Nr of Pages = "+str(nrOfPages))

# PRESS PAGINATION NEXT BUTTON (NECESSARY TO GET THE SECOND PAGE URL, WHICH CAN BE USED TO GENERATE ALL REMAINING URLS)
nextButton = driver.find_element_by_css_selector('.pagination-next a')
nextButton.click()

# GET URL OF SECOND PAGE
time.sleep(0)
secondUrl = driver.current_url

# CREATE ALL REMAINING URLS
allUrls = [initialUrl, secondUrl]
plainUrl = re.sub('&page=1', '', secondUrl)

for i in range(2, nrOfPages):
    allUrls.append(plainUrl+"&page="+str(i))

print(allUrls)
print("First URL: "+initialUrl)
print("Second URL: "+secondUrl)
print("Nr of Pages = "+str(nrOfPages))

urlList = []


# GET URLS OF LISTINGS
for i in range(0, 2):  # normally range(0, len(urlList))
    try:
        page = urllib.request.urlopen(allUrls[i])  # connect to website
    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('a.title'):
        urlList.append("https://www.comparis.ch"+a['href'])




print(urlList)

addresses = []

# GET INFOS ON LISTINGS
for i in urlList:
    try:
        page = urllib.request.urlopen(i)  # connect to website
    except:
        print("An error occured.")

    soup = BeautifulSoup(page, 'html.parser')

    for a in soup.select('div.dt.label-text dd'):
        addresses.append(a)

print(addresses)

