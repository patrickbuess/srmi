import pymysql
from classes.classDBOperations import *
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import numpy
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import geopandas as gpd
from shapely.geometry import Point

"""Cantonal Level: This file allows to draw some graphic conclusions about our data to give a visual overview of the Swiss rental market index (SRMI)
to our customers."""

# -------------------------------

# Get the name of the city for each postal code (in order to then format charts and add dynamic titles to objects' output).


class cantonal:
    def __init__(self, dbOperations = None):
        self.dbOperations = dbOperations

    def cantonName(self, canton):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        postalCodeList = []
        canton = canton

        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT postalCode FROM `postalCodes` WHERE canton = '{}'".format(canton)
                cursor.execute(sql)
                list = cursor.fetchall()
                for p in list:
                    if p['postalCode'] is not None:
                        c = p['postalCode']
                        postalCodeList.append(c)
                postalCodeList = tuple(postalCodeList)

        finally:
            return postalCodeList
        # cityName being the name of the city attached to the postal code entered
        # postalCodeList being the list of postal codes included in the same city as the city of the entered postal code.
        # citydict is a dictionary including both cityName and postalCodeList, in this order.



# Get average price of the postal code entered


class cantonalData:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    # Get the average numerical value for the price of properties in the postal code area entered by the customer
    def averageCanton(self, canton, varx, varx2):
        list = []
        postalCodeList = cantonal(DBOperations("kezenihi_srmidb3")).cantonName(canton)
        if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT {} FROM listingDetails WHERE postalCode IN {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(varx, postalCodeList)
                cursor.execute(sql)
                list = cursor.fetchall()
                list = [x[varx] for x in list if x[varx] is not None]

                #Take away the most extreme elements of the data collected, with the help of standard deviations (sd)
                elements = numpy.array(list)
                mean = numpy.mean(elements, axis=0)
                sd = numpy.std(elements, axis=0)
                listy = [x for x in list if (x > mean - 2 * sd)]
                list = [x for x in listy if (x < mean + 2 * sd)]

                #Calculate the variable average price for the zone
                priceavg = statistics.mean(list)

                #Calculate the variable 'average surface' (size) of the flats there in meter
                sql = "SELECT {} FROM listingDetails WHERE postalCode IN {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(varx2, postalCodeList)
                cursor.execute(sql)
                list = cursor.fetchall()
                list2 = [x[varx2] for x in list if x[varx2] is not None]

                elements = numpy.array(list2)
                mean = numpy.mean(elements, axis=0)
                sd = numpy.std(elements, axis=0)
                listy = [x for x in list2 if (x > mean - 2 * sd)]
                list2 = [x for x in listy if (x < mean + 2 * sd)]

                averageSize = statistics.mean(list2)

                #Calculate the average price per square meter in the postal code chosen
                averageMeterPrice = priceavg/averageSize

                #Get the city name to format a nice name of the string or Chart
                townName= canton

        finally:
            cursor.close()
            print('Report for statistics regarding the SRMI in '+townName)
            print('')

            print('Average price in '+townName+': '+str(priceavg))
            print('Average size of properties in square meters: ' + str(averageSize))
            print('Average square meter price in ' + townName + ': ' + str(averageMeterPrice))

    # Get the price of all the properties in the postal code area to make a distribution graph with it.
    def distribCanton(self, canton, varx):
        list = []
        postalCodeList = cantonal(DBOperations("kezenihi_srmidb3")).cantonName(canton)
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
            self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:

                #Select from SQL the desired data
                sql = "SELECT {} FROM listingDetails WHERE postalCode IN {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(varx, postalCodeList)
                cursor.execute(sql)
                data = cursor.fetchall()
                for p in data:
                    if p[varx] is not None and p[varx] not in [0,1]:
                        c = p[varx]
                        list.append(c)

                #Take away the most extreme elements of the data collected, with the help of standard deviations (sd)
                elements=numpy.array(list)
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                listy = [x for x in list if (x > mean -2*sd)]
                list = [x for x in listy if (x < mean + 2 * sd)]

                # Get the city name to format a nice name of the string or Chart
                townName = canton


        finally:
            cursor.close()

            #Plot the prepared data
            plt.hist(list, color='#2d85cb', edgecolor='black', bins=int(180 / 5))
            plt.title("Distribution of " + varx+ " in "+townName)
            plt.xlabel(varx)
            plt.ylabel("Number of properties for such "+varx)
            return (plt.show())
            return list
            return len(list)

    # Get the price and size of the flat in a certain postal code and plot it in a two dimensional graph.
    def priceMeterCanton(self, canton, varx, varx2, varx3 = None):
        dataAll = []
        scatterData = []
        townName = canton
        postalCodeList = cantonal(DBOperations("kezenihi_srmidb3")).cantonName(canton)
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        #FIRST, collect the data from the varx (which can be defined as a variable for replicability of the code). This will correspond to one of the axis in our 2-dimensional chart.
        try:
            with DBOperations.connection.cursor() as cursor:
                #Select now from the Database the desired data
                sql = "SELECT {},{},{} FROM listingDetails WHERE postalCode IN {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(varx, varx2, varx3, postalCodeList)
                cursor.execute(sql)
                data = cursor.fetchall()

                # Creating 2 lists which define the two axis of the chart
                for p in data:
                    if p[varx] is not None and p[varx2] is not None and p[varx3] is not None:
                        dataAll.append({"varx":p[varx],"varx2": p[varx2],"varx3": p[varx3]})

                #Defining the standard deviation for both sets of data  we have at hand (sd for axis1 and sda for axis2)
                scatterData = pd.DataFrame(dataAll, columns = ['varx', 'varx2',"varx3"])
                # Defining the standard deviation for both sets of data we have at hand (sd for axis1 and sda for axis2)

                elements=numpy.array(scatterData['varx'])
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                scatterData = scatterData.loc[scatterData['varx'] > (mean - 2 * sd)]
                scatterData = scatterData.loc[scatterData['varx'] < (mean + 2 * sd)]

                elements=numpy.array(scatterData['varx2'])
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                scatterData = scatterData.loc[scatterData['varx2'] > (mean - 2 * sd)]
                scatterData = scatterData.loc[scatterData['varx2'] < (mean + 2 * sd)]

                elements=numpy.array(scatterData['varx3'])
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                scatterData = scatterData.loc[scatterData['varx3'] > (mean - 2 * sd)]
                scatterData = scatterData.loc[scatterData['varx3'] < (mean + 2 * sd)]

                # Get the city name to format a nice name of the string or Chart
                townName = canton

        finally:
           cursor.close()
           print('There are '+str(len(scatterData.varx))+' observations in Canton '+townName)

           #Plot the prepared data
           cmap = mpl.cm.get_cmap('RdYlBu')
           plot = plt.scatter(scatterData.varx, scatterData.varx2, s=15, c=scatterData.varx3, cmap=cmap)
           plt.colorbar(plot)
           plt.suptitle(varx + " in relation to " + varx2+" in "+ townName)
           plt.title("The colorbar refers to " + str(varx3), fontsize=9)
           plt.xlabel(varx)
           plt.ylabel(varx2)

           return (plt.show())

    def weatherCanton(self,canton):
        axis1 = []
        axis2 = []
        postalCode = cantonal(DBOperations("kezenihi_srmidb3")).cantonName(canton)[1]

        #Define the columns that contains the data for each of the Max and Min temperatures in °C for the postal code entered by the customer.
        maxTemp = ['maxtempJan',  'maxtempFeb',  'maxtempMar',  'maxtempApr',  'maxtempMai', 'maxtempJun', 'maxtempJul', 'maxtempAug', 'maxtempSep', 'maxtempOct', 'maxtempNov', 'maxtempDec']
        minTemp = ['mintempJan', 'mintempFeb', 'mintempMar', 'mintempApr', 'mintempMai', 'mintempJun', 'mintempJul', 'mintempAug','mintempSep', 'mintempOct', 'mintempNov', 'mintempDec']

        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()

        try:
            with DBOperations.connection.cursor() as cursor:
                # Select from sql the list of postal codes that are from the same city of the one we would like to look at, because some big cities are divided in more postal codes while being the same city.
                sql = "SELECT * FROM `weatherData` WHERE postalCode = {}".format(postalCode)
                cursor.execute(sql)
                data = cursor.fetchall()
                for p in data:
                    for x in maxTemp:
                        if p[x] is not None:
                            c = p[x]
                            axis1.append(c)
                    for x in minTemp:
                        if p[x] is not None:
                            c = p[x]
                            axis2.append(c)
                # Axis 1 being the name of the max temperatures for the postal code in the period of 1 year (12 values, 1 per month)
                #  Axis 2 being the name of the min temperatures for the postal code in the period of 1 year (12 values, 1 per month)

                # Get the city name to format a nice name of the string or Chart
                townName = canton

        finally:
            cursor.close()

            #Plot the prepared data
            plt.plot(axis1, label= 'Max temperatures', color= 'r')
            plt.plot(axis2, label= 'Min temperatures', color='#2d85cb')
            plt.title('Yearly temperature per month in ' + townName)
            plt.xlabel('Month')
            plt.ylabel('Temperature in °C')
            plt.legend()
            plt.axhline(y=0, color='k')

            return (plt.show())


    def mapAllListingsCanton(self, canton=None, shapefile=gpd.GeoDataFrame.from_file('datasets/PLZO_SHP_LV03/PLZO_PLZ.shp')):
        locations = []
        postalCodeList = cantonal(DBOperations("kezenihi_srmidb3")).cantonName(canton)
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `listingDetails` WHERE (latitude <= 47.829906 AND latitude >= 45.795286 AND longitude >= 5.855986 AND longitude <= 10.584407 AND postalCode IN {})".format(postalCodeList)  # WE ONLY COMPARE NEWLY SCRAPED URLS WITH URLS FROM THE LAST 6 MONTHS, AFTER THAT CHANCE IS SMALL THAT A LISTING IS STILL ONLINE
                cursor.execute(sql)
                items = cursor.fetchall()
                for item in items:
                    if item["latitude"] is not None:
                        lat = float(item["latitude"])
                        long = float(item["longitude"])
                        if item['price'] is not None and item['size'] is not None:
                            price = float(item["price"])
                            size = int(item['size'])
                            locations.append({"latitude":lat,"longitude":long,"price":price,"size":size})

                canton = shapefile[shapefile.PLZ.isin(postalCodeList)]

                df = pd.DataFrame(locations, columns = ['latitude', 'longitude',"price","size"])
                df['pricePerSq'] = df.apply(lambda row: (row.price / row.size) ** 0.5, axis=1)

                # CONVERT SHAPEFILE
                canton = canton.to_crs(epsg=4326)

                # CREATE GEO DATAFRAME
                geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
                df = df.drop(['longitude', 'latitude'], axis=1)
                gdf = gpd.GeoDataFrame(df, geometry=geometry)

                # TAKE OUT EXTREME VALUES FROM SET
                elements=numpy.array(gdf['pricePerSq'])
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                gdf = gdf.loc[gdf['pricePerSq'] > (mean - 2 * sd)]
                gdf = gdf.loc[gdf['pricePerSq'] < (mean + 2 * sd)]

                # CREATE plot
                vmin, vmax = gdf['pricePerSq'].min(), gdf['pricePerSq'].max()
                cmap = mpl.cm.get_cmap('RdYlBu')
                base = canton.plot(figsize=(40, 20), linewidth=1, edgecolor='#999999', color='#ffffff')
                points = gdf.plot(markersize=20, column='pricePerSq', s='pricePerSq', k=100, cmap=cmap, legend=True, alpha=0.5, vmin=vmin, vmax=vmax, ax=base)
                fig = points.get_figure()
                cax = fig.add_axes([0, 5, 10, 20])
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
                sm._A = []
                fig.colorbar(sm, cax=cax)
                # sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=plt.Normalize(vmin=vmin, vmax=vmax))
                # set_axis_off(points)
                # colorbar(points)
                # points.legend(title="legend")

        finally:
            print("create mapAllListingsCanton SUCCESS")
            cursor.close()
            plt.show()
