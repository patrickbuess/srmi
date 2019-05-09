from bs4 import BeautifulSoup
import random
import requests
from fake_useragent import UserAgent
import datetime
import traceback
from scraper.functionScraper import *
from scraper.classListingObject import *
from scraper.classHelpClasses import *
from classes.classPostalData import *
from classes.SBBAPI import *

def babyScraper(url):

    print("--> Check URL: "+url)
    # CREATE LISTING OBJECT
    listing = listingObject(DBOperations("kezenihi_srmidb3"))

    # c = requests.get(url[1], proxies=proxies, headers={'user-agent': headers}).content
    c = None
    try:
        c = requests.get(url).content
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

        listing.address = soup.select('section.content-section .column .row.column .align-middle h3.text-green')[0].text.strip()
        # CONVERT ADDRESS VIA GOOGLE GEOLOCATION API
        print("RUN GEOLOCATION API")
        api_key = "AIzaSyDLpLwScHEHrVpIQOVjSj0RaCOwrkuViNI"
        query = (listing.address+",+Switzerland").replace(" ", "+")
        # query = "Berneggstrasse 54, 9000 St. Gallen, Switzerland"

        print(query)
        try:
            googleurl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&lang=de&key=' + api_key
            result = requests.get(googleurl)
            data = result.json()
            location = data['results'][0]
            listing.latitude = location['geometry']['location']['lat']
            listing.longitude = location['geometry']['location']['lng']
            for i in location['address_components']:
                for category in i['types']:
                    data[category] = {}
                    data[category] = i['long_name']

            listing.postalCode = data.get("postal_code", None)

        except Exception as e:
            print(e)
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

    else:
        "There was a problem with accessign the URL, please try again."

    postalObject = postalCodeData(DBOperations("kezenihi_srmidb3")).average(listing.postalCode, "price", "size")
    print("\nComparison for this listing\n")
    try:
        diffAvgPrice = int(listing.price) - int(postalObject['avgPrice'])
        if (diffAvgPrice > 0):
            print("The price for this property is "+str(diffAvgPrice)+" higher than the communal average\n")
        else:
            print("The price for this property is "+str(diffAvgPrice)+" lower than the communal average\n")
    except:
        print("Unfortunately no price could be found for this listing\n")
    try:
        diffAvgSize = int(listing.size) - int(postalObject['avgSize'])
        if (diffAvgSize > 0):
            print("The size of this property is "+str(diffAvgSize)+" larger than the communal average\n")
        else:
            print("The size of this property is "+str(diffAvgSize)+" smaller than the communal average\n")
    except:
        print("Unfortunately no size could be found for this listing\n")
    try:
        diffAvgMeterPrice = (int(listing.price)/int(listing.size)) - int(postalObject['avgMeterPrice'])
        if (diffAvgMeterPrice > 0):
            print("The price per square meter of this property is "+str(diffAvgMeterPrice)+" higher than the communal average\n")
        elif (diffAvgMeterPrice < 0):
            print("The price per square meter of this property is "+str(diffAvgMeterPrice)+" lower than the communal average\n")
    except:
        print("Unfortunately no price per square meter could be calculated for this property\n")

    print("Details about public transport availability for this property:\n")
    SBB(DBOperations("kezenihi_srmidb3")).getClosestStop(lat=listing.latitude, long=listing.longitude)
