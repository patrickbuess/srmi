from classes.DBOperations import *
import unidecode
import requests
from collections import OrderedDict

postalcodedict = {}


class weather:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    # simple function that returns a key for a given value from a dict
    def get_key(self, val):
        for key, value in postalcodedict.items():
             if val in value:
                 return key
        return "key doesn't exist"

    # this function interacts with the weather API and updates a single line according to the postalcode given
    def insertWeatherData(self, city, pcLocation):
        if self.dbOperations is None:
            self.dbOperations = DBOperations().getDB()
        self.dbOperations.getConnection()

        while True:
            # takes away all accents in a word to avoid errors
            city = unidecode.unidecode(city)

            # giving the city name to the API
            r = requests.get(
                'http://api.worldweatheronline.com/premium/v1/weather.ashx?key=54e2762b58214c3e833145855190705&q=' + city + ',Switzerland&format=json')
            json_data = r.json()

            # extracting targeted data on json file (location found by API, max temp and min temp per month)
            location = json_data['data']['request'][0]['query']

            maxtempJan = json_data['data']['ClimateAverages'][0]['month'][0]['absMaxTemp']
            maxtempFeb = json_data['data']['ClimateAverages'][0]['month'][1]['absMaxTemp']
            maxtempMar = json_data['data']['ClimateAverages'][0]['month'][2]['absMaxTemp']
            maxtempApr = json_data['data']['ClimateAverages'][0]['month'][3]['absMaxTemp']
            maxtempMai = json_data['data']['ClimateAverages'][0]['month'][4]['absMaxTemp']
            maxtempJun = json_data['data']['ClimateAverages'][0]['month'][5]['absMaxTemp']
            maxtempJul = json_data['data']['ClimateAverages'][0]['month'][6]['absMaxTemp']
            maxtempAug = json_data['data']['ClimateAverages'][0]['month'][7]['absMaxTemp']
            maxtempSep = json_data['data']['ClimateAverages'][0]['month'][8]['absMaxTemp']
            maxtempOct = json_data['data']['ClimateAverages'][0]['month'][9]['absMaxTemp']
            maxtempNov = json_data['data']['ClimateAverages'][0]['month'][10]['absMaxTemp']
            maxtempDec = json_data['data']['ClimateAverages'][0]['month'][11]['absMaxTemp']

            mintempJan = json_data['data']['ClimateAverages'][0]['month'][0]['avgMinTemp']
            mintempFeb = json_data['data']['ClimateAverages'][0]['month'][1]['avgMinTemp']
            mintempMar = json_data['data']['ClimateAverages'][0]['month'][2]['avgMinTemp']
            mintempApr = json_data['data']['ClimateAverages'][0]['month'][3]['avgMinTemp']
            mintempMai = json_data['data']['ClimateAverages'][0]['month'][4]['avgMinTemp']
            mintempJun = json_data['data']['ClimateAverages'][0]['month'][5]['avgMinTemp']
            mintempJul = json_data['data']['ClimateAverages'][0]['month'][6]['avgMinTemp']
            mintempAug = json_data['data']['ClimateAverages'][0]['month'][7]['avgMinTemp']
            mintempSep = json_data['data']['ClimateAverages'][0]['month'][8]['avgMinTemp']
            mintempOct = json_data['data']['ClimateAverages'][0]['month'][9]['avgMinTemp']
            mintempNov = json_data['data']['ClimateAverages'][0]['month'][10]['avgMinTemp']
            mintempDec = json_data['data']['ClimateAverages'][0]['month'][11]['avgMinTemp']

            # when the weather API doesn't recognise the location in Switzerland,
            # this part redirects the city to the city right before in the postalcodedict and goes back to the beginning of the loop
            if "Switzerland" not in location or "USA" in location:
                print(city)
                ordered = OrderedDict(postalcodedict)
                keys = list(ordered.keys())
                index = keys.index(city)-1
                print(ordered[keys[index]])
                closest_pc = int(ordered[keys[index]][0])
                print(closest_pc)
                city = weather.get_key(closest_pc)
                print("Closest city: "+ city)

            # when the weather API does recognise the location in Switzerland, this part updates the database
            # once updated, the while loop breaks
            else:
                print("Successful")

                with DBOperations.connection.cursor() as cursor:
                    sql = "UPDATE `weatherData` SET `maxtempJan`= %s, `maxtempFeb`= %s, `maxtempMar`= %s, " \
                          "`maxtempApr`= %s, `maxtempMai`= %s, `maxtempJun`= %s, `maxtempJul`= %s, `maxtempAug`= %s, " \
                          "`maxtempSep`= %s, `maxtempOct`= %s, `maxtempNov`= %s, `maxtempDec`= %s, `mintempJan`= %s, " \
                          "`mintempFeb`= %s, `mintempMar`= %s, `mintempApr`= %s, `mintempMai`= %s, `mintempJun`= %s, " \
                          "`mintempJul`= %s, `mintempAug`= %s, `mintempSep`= %s, `mintempOct`= %s, `mintempNov`= %s, " \
                          "`mintempDec`= %s WHERE `postalCode` = %s;"
                    cursor.execute(sql, (maxtempJan, maxtempFeb, maxtempMar, maxtempApr, maxtempMai, maxtempJun, maxtempJul,
                                         maxtempAug, maxtempSep, maxtempOct, maxtempNov, maxtempDec, mintempJan, mintempFeb,
                                         mintempMar, mintempApr, mintempMai, mintempJun, mintempJul, mintempAug, mintempSep,
                                         mintempOct, mintempNov, mintempDec, pcLocation))
                    break

        self.dbOperations.connection.commit()


    # this function updates the whole table with weather data
    def updatewholetable(self):
        if self.dbOperations is None:
            self.dbOperations = DBOperations().getDB()
        self.dbOperations.getConnection()

        # this part selects all the lines in the table
        with DBOperations.connection.cursor() as cursor:
            sql = "SELECT * FROM `weatherData`"
            cursor.execute(sql)
            codes = cursor.fetchall()
            x = 0

            # after selecting all lines in the database, each line is filled with the weather data here
            for code in codes:
                city = code["city"]
                pc = code["postalCode"]
                weather.insertWeatherData(city, pc)
                x += 1
                print(x)
        cursor.close()

postalCodes = postalCodes(DBOperations("kezenihi_srmidb3"))
postalCodes.getPostalCodesDict()

weather = weather(DBOperations("kezenihi_srmidb3"))
weather.updatewholetable()
