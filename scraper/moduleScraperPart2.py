from bs4 import BeautifulSoup
import random
import requests
from fake_useragent import UserAgent
import datetime
import traceback
from scraper.functionScraper import *
from scraper.classListingObject import *
from scraper.classHelpClasses import *


# ####### SECOND PART SCRAPER ######
def scraper2():
    uncheckedUrls = True

    # INITIALISE DATABASE CONNECTION
    urlsToScrape = UrlList(DBOperations("kezenihi_srmidb3"))

    while uncheckedUrls is True:
        try:
            # SET RANDOM PROXY AND FAKE USER AGENT
            proxies = get_proxies()

            # GET FAKE USERAGENT VIA FAKE_USERAGENT PACKAGE
            ua = UserAgent()
            headers = ua.random

            # TEST PROXY
            url = 'https://httpbin.org/ip'

            proxyWorks = False
            print("GET PROXY")
            while proxyWorks is False:
                global proxy
                print("Request")
                proxy = random.choice(proxies)
                try:
                    print("TRY")
                    response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
                    proxyWorks = True
                    print(response.json())
                except:
                    # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
                    # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
                    print("Skipping. Connnection error")

            proxies = {
              "http": proxy,
              "https": proxy,
            }

            # GET UNCHECKED URLS
            urlsList = urlsToScrape.getUrlsID()
            urlsList = random.sample(urlsList, 10)

            # STORE URLS IN PROGRESS, SO THEY CAN BE UNCHECKED AT THE END
            urlsIDs = [item[0] for item in urlsList]

            # CHECK IF THERE ARE UNSCRAPED URLS AVAILABLE
            if (len(urlsList) == 0):
                uncheckedUrls = False

            else:
                urlsToScrape.markInProgress(1, urlsIDs)

                try:
                    # SCRAPE
                    url = urlsList[0]
                    for url in urlsList:

                        checkedURL = False
                        print("--> Check URL: "+url[1])
                        # CREATE LISTING OBJECT
                        listing = listingObject(DBOperations("kezenihi_srmidb3"))
                        listing.listingID = url[0]
                        listing.address = url[2]
                        listing.postalCode = url[3]

                        # c = requests.get(url[1], proxies=proxies, headers={'user-agent': headers}).content
                        c = None
                        try:
                            c = requests.get(url[1], proxies=proxies, headers={'user-agent': headers}, timeout=10).content
                        except Exception as e:
                            print("An error occured")
                            print(e)

                        if (c is not None):

                            print("Url checked successfully")
                            checkedURL = True
                            soup = BeautifulSoup(c, 'html.parser')

                            descrCheck = False
                            try:
                                listing.description = soup.select('#div_Description')[0].text.strip().replace("\n", "")
                                descrCheck = True
                            except:
                                print("No description available")

                            # CONVERT ADDRESS VIA GOOGLE GEOLOCATION API
                            print("RUN GEOLOCATION API")
                            api_key = "AIzaSyDLpLwScHEHrVpIQOVjSj0RaCOwrkuViNI"
                            query = (listing.address+", "+str(listing.postalCode)+", Switzerland").replace(" ","+")
                            try:
                                googleurl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&lang=de&key=' + api_key
                                result = requests.get(googleurl)
                                data = result.json()
                                location = data['results'][0]
                                listing.latitude = location['geometry']['location']['lat']
                                listing.longitude = location['geometry']['location']['lng']
                            except:
                                print("Google API was not successful")

                            # GET ATTRIBUTES GRID INFOS
                            listingAvailable = False
                            try:
                                infos = get_list_content_pairs(soup)
                                listingAvailable = True
                            except:
                                print("Listing is not available anymore.")

                            if (listingAvailable is True):
                                for info in infos:
                                    type = info.find('dt').string.strip()
                                    if (type == "Property type"):
                                        listing.category = info.find('dd').string.strip()
                                    if (type == "Rent per month"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.price = replaceMultiple(result, substitutions)
                                    if (type == "Rent per day"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.pricePerDay = replaceMultiple(result, substitutions)
                                    if (type == "Rent per week"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.pricePerWeek = replaceMultiple(result, substitutions)
                                    if (type == "Annual rent per m²"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.pricePerYear = replaceMultiple(result, substitutions)
                                    if (type == "Rent per month (without charges)"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.primaryCosts = replaceMultiple(result, substitutions)
                                    if (type == "Supplementary charges"):
                                        result = info.find('dd').string.strip()
                                        if(result != "On request"):
                                            substitutions = {"CHF ": "", ",": ""}
                                            listing.additionalCosts = replaceMultiple(result, substitutions)
                                    if (type == "Living space"):
                                        result = info.find('dd').string.strip().replace(" m²", "")
                                        if(result != "On request"):
                                            listing.size = result
                                    if (type == "Floor space"):
                                        result = info.find('dd').string.strip().replace(" m²", "")
                                        if(result != "On request"):
                                            listing.floorSpace = result
                                    if (type == "Property area"):
                                        result = info.find('dd').string.strip().replace(" m²", "")
                                        if(result != "On request"):
                                            listing.propertyArea = result
                                    if (type == "Rooms"):
                                        listing.rooms = info.find('dd').string.strip().replace("½", ".5")
                                    if (type == "Floor"):
                                        result = info.find('dd').string.strip().replace(". floor", "")
                                        if (result == "Ground floor"):
                                            listing.floor = 0
                                        elif (result == "Basement"):
                                            listing.floor = -1
                                        else:
                                            listing.floor = result
                                    if (type == "Available"):
                                        listing.available = info.find('dd').string.strip()
                                    if (type == "Year of construction"):
                                        listing.construction = info.find('dd').string.strip()
                                    if (type == "Lift"):
                                        listing.elevator = 1
                                    if (type == "Balcony/ies"):
                                        listing.balconies = 1
                                    if (type == "Motorway"):
                                        listing.motorway = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Shops"):
                                        listing.shops = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Public transport stop"):
                                        listing.publicTransport = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Kindergarten"):
                                        listing.kindergarten = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Primary school"):
                                        listing.primarySchool = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Secondary school"):
                                        listing.secondarySchool = info.find('dd').string.strip().replace(" m", "")
                                    if (type == "Minergie certified"):
                                        listing.minergie = 1
                                    if (type == "Pets allowed"):
                                        listing.pets = 1
                                    if (type == "Child-friendly"):
                                        listing.childFriendly = 1
                                    if (type == "Cable TV"):
                                        listing.cableTV = 1
                                    if (type == "New building"):
                                        listing.newBuilding = 1
                                    if (type == "Wheelchair accessible"):
                                        listing.wheelchair = 1
                                    if (type == "Outdoor parking"):
                                        listing.parkingOutdoor = 1
                                    if (type == "Indoor parking"):
                                        listing.parkingIndoor = 1
                                    if (type == "Veranda"):
                                        listing.veranda = 1
                                    if (type == "Swimming pool"):
                                        listing.pool = 1

                                # CREATE LIST WITH ONLY FILLED OUT VALUES, MAKES IT EASIER TO SEND PER SQL
                                insertDetails = []
                                insertDetailsKeys = []
                                for k, v in vars(listing).items():
                                    if (k in ["listingID", "category", "postalCode", "address", "latitude", "longitude", "price", "pricePerDay", "pricePerWeek", "pricePerYear", "primaryCosts", "additionalCosts", "size", "floorSpace", "propertyArea", "rooms", "floor", "available", "construction"]):
                                        if (v is not None):
                                            insertDetailsKeys.append(k)
                                            insertDetails.append(v)

                                insertDetailsKeys = str(tuple(insertDetailsKeys)).replace("'", "")

                                insertDistances = []
                                insertDistancesKeys = []
                                for k, v in vars(listing).items():
                                    if (k in ["listingID", "motorway", "shops", "publicTransport", "kindergarten", "primarySchool", "secondarySchool"]):
                                        if (v is not None):
                                            insertDistancesKeys.append(k)
                                            insertDistances.append(v)
                                len(insertDistancesKeys)
                                if (len(insertDistancesKeys) > 1):
                                    insertDistancesKeys = str(tuple(insertDistancesKeys)).replace("'", "")

                                # INSERT listingDetails
                                listing.insertInfos(table="listingDetails",
                                                    columns=str(insertDetailsKeys),
                                                    listings=[tuple(insertDetails)])

                                # INSERT listingDistances
                                if (len(insertDistancesKeys) > 1):
                                    listing.insertInfos(table="listingDistances",
                                                        columns=str(insertDistancesKeys),
                                                        listings=[tuple(insertDistances)])

                                # CHECK IF ATTRIBUTES ARE AVAILABLE
                                attributesAvailable = sum([listing.elevator, listing.balconies, listing.minergie, listing.pets, listing.childFriendly, listing.cableTV, listing.newBuilding, listing.wheelchair, listing.parkingOutdoor, listing.parkingIndoor, listing.veranda, listing.pool])

                                if (attributesAvailable > 0):
                                    # INSERT listingAttributes
                                    listing.insertInfos(table="listingAttributes",
                                                        columns="(listingID, elevator, balconies, minergie, pets, childFriendly, cableTV, newBuilding, wheelchair, parkingIndoor, parkingOutdoor, veranda, pool)",
                                                        listings=[(listing.listingID, listing.elevator, listing.balconies, listing.minergie, listing.pets, listing.childFriendly, listing.cableTV, listing.newBuilding, listing.wheelchair, listing.parkingOutdoor, listing.parkingIndoor, listing.veranda, listing.pool)])

                                # INSERT listingDescription
                                if(descrCheck is True):
                                    listing.insertInfos(table="listingDescription",
                                                        columns="(listingID, description)",
                                                        listings=[(listing.listingID, listing.description)])

                            # UPDATE LISTING URL
                            if (checkedURL is True):
                                d = datetime.datetime.today()
                                urlsToScrape.updateUrl(date=d.strftime('%Y-%m-%d'), id=listing.listingID)

                except Exception as e:
                    print("THIS URL HAD AN ERROR")
                    print(traceback.format_exc())
                    print(e)

            urlsToScrape.markInProgress(0, urlsIDs)
            print("\n\n")

        except Exception as e:
            print("SCRAPING ERROR \n\n")
            print(traceback.format_exc())
            print(e)
