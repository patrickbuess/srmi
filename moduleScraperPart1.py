from selenium import webdriver
# chrome_path = r"C:\Users\Ruben\Documents\Python packages\chromedriver_win32\chromedriver.exe"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests
import time
import re
import datetime
from functionScraper import *
from classDBOperations import *
from classListingObject import *
from classHelpClasses import *


# THIS CODE ITERATES THROUGH POSTAL CODES AND GETS URLS OF LISTINGS, STORES THEM IN A DATABASE


# GET POSTALCODE
postalCodes = postalCodes(DBOperations("kezenihi_srmidb"))
postalCodesList = postalCodes.getAllPostalCodes()
pc = postalCodesList[0]

# ITERATE THROUGH POSTAL CODES
for pc in postalCodesList:
    try:
        print("SCRAPING FOR POSTAL CODE:")
        print(pc)

        # GET PROXY LIST, NEEDED TO CHANGE PROXY FROM TIME TO TIME
        proxies = get_proxies()

        # GET FAKE BROWSER USER AGENTS, CHANGED TOGETHER WITH PROXY
        ua = UserAgent()
        headers = ua.random

        # TEST PROXY
        url = 'https://httpbin.org/ip'

        proxyWorks = False
        print("GETTING PROXY")
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

        # SET PROXY FOR BEAUTIFULSOUP
        proxies = {
          "http": proxy,
          "https": proxy,
        }

        # SET PROXY FOR SELENIUM
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'noProxy': ''  # set this value as desired
            })

        # MAKE BROWSER HEADLESS
        options = Options()
        options.headless = True

        # OPEN HEADLESS BROWSER WINDOW AND VISIT INITIAL SEARCH PAGE OF COMPARIS
        driver = webdriver.Firefox(options=options, proxy=proxy)
        driver.get("https://www.comparis.ch/immobilien/result")

        # TYPE IN POSTAL CODE AND HIT ENTER
        searchField = driver.find_element_by_id("SearchParams_LocationSearchString")
        searchField.send_keys(str(pc))
        searchField.send_keys(Keys.ENTER)

        # WAIT 5 SECONDS AND GET CURRENT URL
        time.sleep(5)
        initialUrl = driver.current_url

        # FIND OUT HOW MANY PAGES THERE ARE
        nrOfPages = None
        try:
            nrOfPages = int(driver.find_element_by_css_selector("ul.pagination li:nth-last-child(2) a").get_attribute("innerHTML"))
            print("Number of Pages: "+str(nrOfPages))
        except Exception as e:
            print("No pages found")
            print(e)

        # IF NO PAGES ARE EXISTING ONLY SCRAPE THE URLS FROM THE INITIAL PAGE
        if (nrOfPages is not None):
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

        else:
            allUrls = [initialUrl]  # IF NO PAGINATION EXISTING

        # CLOSE HEADLESS BROWSER WINDOW
        driver.close()
        driver.quit()

        # GET URLS OF LISTINGS
        urlListings = []
        checkSuccess = False

        # SET COUNTER FOR CONSOLE OUTPUT
        counter = 1

        # ITERATE THROUGH ALL URLS AND SCRAPE LISTING URLS FROM THERE
        for i in allUrls:

            # VISIT URL, GET SOURCE CODE
            try:
                page = None
                print("Scrape listing URLs for Base URL: "+str(counter))
                page = requests.get(i, proxies=proxies, headers={'user-agent': headers}, timeout=60).content  # connect to website
            except:
                print("An error occured.")

            # IF REQUEST WAS SUCCESSFUL SCRAPE THROUGH SOURCE CODE
            if(page is not None):
                soup = BeautifulSoup(page, 'html.parser')
                d = datetime.datetime.today()

                # SET VAR TO TRUE TO INDICATE THAT THIS POSTAL CODE CAN BE MARKED AS SCRAPED WITH A CURRENT DATE
                checkSuccess = True
                print("Check was successful")

                # ITERATE THROUGH DIVS CONTAINING THE ADDRESS, POSTAL CODE AND URL
                # WE SCRAPE THE POSTAL CODE INITIALLY HERE, BECAUSE IT CAN BE EASIER DISTINGUISHED BETWEEN STREET AND POSTAL CODE
                for a in soup.select('div.content-column.columns'):
                    if (len(a.select('a.title')) > 0):
                        url = a.select('a.title')[0]['href']
                        print("--> Found URL: "+url)
                        if (len(a.select('span.street')) > 0):
                            street = a.select('span.street')[0].string
                        else:
                            street = 0
                        if (len(a.select('address')) > 0):
                            postal = str(a.select('address')[0].text).strip()
                            postal = re.findall("\d{4}", postal)
                            postal = postal[0]
                        else:
                            postal = 0

                        # APPEND FOUND URLS TO LIST UF URLS
                        urlListings.append(("https://en.comparis.ch"+url, street, postal, 0, d.strftime('%Y-%m-%d')))

            counter = counter+1

            print("Appended, length of URL list: "+str(len(urlListings)))

        # CHECK WHETHER URLS ARE IN UrlList already
        checkedUrls = UrlList(DBOperations("kezenihi_srmidb"))
        allCheckedUrls = checkedUrls.getAllUrls()

        # REMOVE DOUBE ENTRIES
        validUrls = [x for x in urlListings if x[0] not in allCheckedUrls]

        # IF VALID URLS ARE REMAINING, INSERT THEM INTO listingURL
        if (len(validUrls) > 0):
            # INSERT NEW URLS INTO listingURL
            print("Update listingURL table")
            checkedUrls.insertNewUrls(validUrls)
        else:
            print("No new URLS added")

        # UPDATE postalCodes TABLE WITH NEW DATE
        if (checkSuccess is True):
            print("Update postalCodes table")
            d = datetime.datetime.today()
            postalCodes.updateLastChecked(postalCode=pc, date=d.strftime('%Y-%m-%d'))

        print("\n\n")

    except Exception as e:
        print("THIS POSTAL CODE DID NOT RUN THROUGH")
        print(e)
        print("\n\n")
