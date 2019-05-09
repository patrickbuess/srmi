import pymysql
import MySQLdb
from selenium import webdriver
# chrome_path = r"C:\Users\Ruben\Documents\Python packages\chromedriver_win32\chromedriver.exe"
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import random
import requests
import time
import re
import datetime
# from functionScraper import *
from classDBOperations import *
from classListingObject import *
from classHelpClasses import *
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import statistics
import numpy

#For the map part
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import folium

"""This file allows to draw some graphic conclusions about our data to give a visual overview of the Swiss rental market index
to our customers."""

class DBOperations:
   def __init__(self, DB_NAME, DB_USER='kezenihi_srmidb', DB_PASSWORD='FJgc69L3', connection=None):
       self.DB_NAME = DB_NAME
       self.DB_USER = DB_USER
       self.DB_PASSWORD = DB_PASSWORD
       DBOperations.DB_Flag = False
       DBOperations.connection = connection

   def getConnection(self):
       if not DBOperations.DB_Flag:
           DBOperations.connection = DBOperations.openDBConnection(self)
       return DBOperations.connection

   def openDBConnection(self):
       if not DBOperations.DB_Flag:
           DBOperations.connection = pymysql.connect(
                                       host='kezenihi.mysql.db.hostpoint.ch',
                                       user=self.DB_USER,
                                       password=self.DB_PASSWORD,
                                       db=self.DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
           DBOperations.DB_Flag = True
       return DBOperations.connection

   def closeDBConnection(self):
       if DBOperations.DB_Flag:
           DBOperations.connection.close()
           DBOperations.DB_Flag = False

   def getDB(self):
       if DBOperations.DB_Flag:
           return self
       else:
           self.getConnection()
           return self

#-------------------------------

#Get the name of the city for each postal code (in order to then format charts and add dynamic titles to objects' output).
class city:
    def __init__(self, dbOperations = None):
        self.dbOperations = dbOperations
    def cityName(self, postalCode):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        postalCodeList = []

        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT city FROM `postalCodes` WHERE postalCode = {}".format(postalCode)
                cursor.execute(sql)
                list = cursor.fetchall()
                cityName = [x['city'] for x in list if x['city'] is not None]

                # Select from sql the list of postal codes that are from the same city of the one we would like to look at, because some big cities are divided in more postal codes while being the same city.
                sql = "SELECT postalCode FROM `postalCodes` WHERE city IN (SELECT city FROM `postalCodes` WHERE postalCode = {})".format(
                    postalCode)
                cursor.execute(sql)
                data = cursor.fetchall()
                for p in data:
                    if p['postalCode'] is not None:
                        c = p['postalCode']
                        postalCodeList.append(c)
                citydict= dict({'cityName':cityName ,'postalCodeList':postalCodeList})

        finally:
            return cityName[0]
            return postalCodeList
            return citydict
        #cityName being the name of the city attached to the postal code entered
        #postalCodeList being the list of postal codes included in the same city as the city of the entered postal code.
        #citydict is a dictionary including both cityName and postalCodeList, in this order.

# Get average price of the postal code entered
class avgPc:
   def __init__(self, dbOperations=None):
       self.dbOperations = dbOperations

#Get the average numerical value for the price of properties in the postal code area entered by the customer
   def average(self, postalCode, varx, varx2):
       list = []
       postalCode= postalCode
       varx = varx
       varx2= varx2
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       try:
           with DBOperations.connection.cursor() as cursor:
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {}".format(varx, postalCode)
               cursor.execute(sql)
               list = cursor.fetchall()
               list = [x[varx] for x in list if x[varx] is not None]

               #Calculate the variable average price for the zone
               priceavg = statistics.mean(list)

               #Calculate the variable 'average surface' (size) of the flats there in meter
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {}".format(varx2, postalCode)
               cursor.execute(sql)
               list = cursor.fetchall()
               list2 = [x[varx2] for x in list if x[varx2] is not None]
               averageSize = statistics.mean(list2)

               #Calculate the average price per square meter in the postal code chosen
               averageMeterPrice = priceavg/averageSize

               #Get the city name to format a nice name of the string or Chart
               townName= city(DBOperations("kezenihi_srmidb3")).cityName(postalCode)

       finally:
           cursor.close()
           print('Report for statistics regarding the SRMI in '+townName)
           print('')

           print('Average price in '+townName+': '+str(priceavg))
           print('Average size of properties in square meters: ' + str(averageSize))
           print('Average square meter price in ' + townName + ': ' + str(averageMeterPrice))

           return priceavg
           return averageSize
           return averageMeterPrice


#Get the price of all the properties in the postal code area to make a distribution graph with it.
   def distrib(self, postalCode, varx):
       list = []
       postalCodeList = []
       postalCode = postalCode
       varx= varx
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       try:
           with DBOperations.connection.cursor() as cursor:
               #Select from sql the list of postal codes that are from the same city of the one we would like to look at, because some big cities are divided in more postal codes while being the same city.
               sql = "SELECT postalCode FROM `postalCodes` WHERE city IN (SELECT city FROM `postalCodes` WHERE postalCode = {})".format(postalCode)
               cursor.execute(sql)
               data = cursor.fetchall()
               for p in data:
                   if p['postalCode'] is not None:
                      c = p['postalCode']
                      postalCodeList.append(c)

               #Transform the list of postal codes in tuples so that the next SQL query is ready to work
               postalCodeList = tuple(postalCodeList)

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
               townName = city(DBOperations("kezenihi_srmidb3")).cityName(postalCode)


       finally:
           cursor.close()
           print('Postal codes taken into account for the city of ' + townName + ': ' +str(postalCodeList))

           #Plot the prepared data
           plt.hist(list, color='#2d85cb', edgecolor='black', bins=int(180 / 5))
           plt.title("Distribution of " + varx+ " in "+townName)
           plt.xlabel(varx)
           plt.ylabel("Number of properties for such "+varx)
           return (plt.show())
           return list
           return len(list)

# Get the price and size of the flat in a certain postal code and plot it in a two dimensional graph.
   def priceMeter(self, postalCode):
       list = []
       lista = []
       siza= []
       postalCodeList = []
       postalCode = postalCode
       varx = 'price'
       varx2= 'size'
       varx3= 'rooms'
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       #FIRST, collect the data from the varx (which can be defined as a variable for replicability of the code). This will correspond to one of the axis in our 2-dimensional chart.
       try:
           with DBOperations.connection.cursor() as cursor:
               # Select from sql the list of postal codes that are from the same city of the one we would like to look at, because some big cities are divided in more postal codes while being the same city.
               sql = "SELECT postalCode FROM `postalCodes` WHERE city IN (SELECT city FROM `postalCodes` WHERE postalCode = {})".format(
                   postalCode)
               cursor.execute(sql)
               data = cursor.fetchall()
               for p in data:
                   if p['postalCode'] is not None:
                       c = p['postalCode']
                       postalCodeList.append(c)

               #Determine if there are one or many postal codes that are in the same city or the city targeted by the user has only 1 postal code attributed.
               if len(postalCodeList) is 1:
                   # Select now from the Database the desired data in the case there is only one postal code for the targeted city (because the SQL query syntax changes if there are one or many)
                   postalCodeList = postalCode
                   sql = "SELECT {},{},{} FROM listingDetails WHERE postalCode = {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(
                       varx, varx2, varx3, postalCodeList)
                   cursor.execute(sql)
                   data = cursor.fetchall()

               else:
                   #Select now from the Database the desired data
                   # Transform the list of postal codes in tuples so that the next SQL query is ready to work
                   postalCodeList = tuple(postalCodeList)
                   sql = "SELECT {},{},{} FROM listingDetails WHERE postalCode IN {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(
                       varx, varx2, varx3, postalCodeList)
                   cursor.execute(sql)
                   data = cursor.fetchall()

               #Creating 2 lists which define the two axis of the chart
               for p in data:
                   if p[varx] is not None and p[varx] not in [0, 1] and p[varx2] is not None and p[varx2] not in [0, 1]:
                       c = p[varx]
                       list.append(c)
                       d = p[varx2]
                       lista.append(d)
                       e = p[varx3]
                       siza.append(e)

               #Create the 2 list that we will fill with some extreme-values-filtered data so that our plots are representing the reality of the average market and not the extreme cases (that we want to exclude here from our data)
               axis1 = []
               axis2 = []
               size = []
               #Defining the standard deviation for both sets of data we have at hand (sd for axis1 and sda for axis2)
               elements = numpy.array(list)
               mean = numpy.mean(elements, axis=0)
               sd = numpy.std(elements, axis=0)

               elements = numpy.array(lista)
               mean = numpy.mean(elements, axis=0)
               sda = numpy.std(elements, axis=0)

               # Let's define the 2 axis and filter the extreme values from the axis1 and then the extreme values from the axis 2 to obtain a bidimentional coherent plot.
               #Here we want to exclude outlyers from the dataset by using standard deviations (2 standard deviations here)
               for x in range(1,len(list)):
                   if list[x]> (mean - 2 * sd) and list[x]< mean + 2 * sd:
                       if lista[x]> (mean - 2 * sda) and lista[x]< mean + 2 * sda:
                           axis1.append(list[x])
                           axis2.append(lista[x])
                           if siza[x] is None:
                               size.append(10)
                           else:
                               size.append(siza[x]*10)
               # axis1 is the first axis we define with the varx variable
               # axis2 is the first axis we define with the varx variable
               # size is the size of the data points in the graph

               # Get the city name to format a nice name of the string or Chart
               townName = city(DBOperations("kezenihi_srmidb3")).cityName(postalCode)

       finally:
           cursor.close()
           print('Postal codes taken into account for the city of ' + townName + ': ' + str(postalCodeList))
           print('There are '+str(len(axis1))+' observations in '+townName)

           #Plot the prepared data
           plt.scatter(axis1, axis2, s=size, color='#2d85cb')
           plt.suptitle(varx + " in relation to " + varx2+" in "+ townName)
           plt.title("The size of the points is the number of "+str(varx3), fontsize= 9)
           plt.xlabel(varx)
           plt.ylabel(varx2)

           return (plt.show())


   def weather(self,postalCode):
       axis1 = []
       axis2 = []
       postalCode = postalCode

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
               townName = city(DBOperations("kezenihi_srmidb3")).cityName(postalCode)

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



postalCodes = avgPc(DBOperations("kezenihi_srmidb3"))
postalCodes.average(1000, 'price', 'size')

postalCodes.distrib(1000, 'price')
postalCodes.priceMeter(1000)
postalCodes.weather(1000)

city(DBOperations("kezenihi_srmidb3")).cityName(1000)

# --------------------------------------------------
# In this section we create all the geographical map visualization that are necessary to satisfy our customers' needs.
# For that, we use visuals of maps with colours.

