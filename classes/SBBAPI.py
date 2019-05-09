import requests
from classes.classDBOperations import *

adresslat = ""
adresslon = ""


class SBB:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    #This function returns the closest public transportation stop, the distance to it and the number of stops within 500m
    def getClosestStop(self, lat, long):

        # if self.dbOperations is None:
        #     self.dbOperations = DBOperations().getDB()
        # self.dbOperations.getConnection()
        #
        # listingID = input("listingID: ")

        # selecting the latitude and longitude from the database
        # try:
        #     with DBOperations.connection.cursor() as cursor:
        #         sql = "SELECT * FROM `listingDetails` WHERE listingID like %s"
        #         cursor.execute(sql, listingID)
        #         codes = cursor.fetchall()
        #         for code in codes:
        #             a = code["address"]
        #             adresslat = code["latitude"]
        #             adresslon = code["longitude"]
        #         print(a)
        #
        # finally:
        #     cursor.close()

        adresslat = str(lat)
        adresslon = str(long)

        # API interaction with latitude and longitude
        r = requests.get('https://data.sbb.ch/api/records/1.0/search/?dataset=didok-liste&facet=abkuerzung&facet=tunummer&facet=tuabkuerzung&facet=betriebspunkttyp&facet=verkehrsmittel&facet=dst_abk&facet=didok&geofilter.distance=' + adresslat + '%2C+' + adresslon + '%2C+500')
        json_data = r.json()

        distance = str(json_data['records'][0]['fields']['dist'])
        stop_name = str(json_data['records'][0]['fields']['name'])
        number_stops = len(json_data['records'])

        print("Distance to closest stop is: " + distance + " meters.")
        print("Closest stop: "+ stop_name)
        print("There are "+ str(number_stops) +" stops for public transport within 500 meters.")
