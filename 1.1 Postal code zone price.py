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
# Get average price of the postal code entered
class avgPc:
   def __init__(self, dbOperations=None):
       self.dbOperations = dbOperations

#Get the average numerical value
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
               print(priceavg)

               #Calculate the variable average surface (size) of the flats there in meter
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {}".format(varx2, postalCode)
               cursor.execute(sql)
               list = cursor.fetchall()
               list2 = [x[varx2] for x in list if x[varx2] is not None]
               averageSize = statistics.mean(list2)
               print(averageSize)

               #Calculate the average price per square meter in the postal code chosen
               averageMeterPrice = priceavg/averageSize
               print(averageMeterPrice)

       finally:
           cursor.close()
           return priceavg
           return averageSize
           return averageMeterPrice


#Get the price of all the properties in the postal code area to make a distribution graph with it.
   def distrib(self, postalCode, varx):
       list = []
       postalCode = postalCode
       varx= varx
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       try:
           with DBOperations.connection.cursor() as cursor:
               #Select from sql
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(varx, postalCode)
               print(sql)
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


       finally:
           cursor.close()
           plt.hist(list, color='#2d85cb', edgecolor='black', bins=int(180 / 5))
           return (plt.show())
           return list
           return len(list)

# Get the price and size of the flat in a certain postal code and plot it in a two dimensional graph.
   def priceMeter(self, postalCode):
       list = []
       lista = []
       postalCode = postalCode
       varx = 'price'
       varx2= 'size'
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       #FIRST, collect the data from the varx (which can be defined as a variable for replicability of the code). This will correspond to one of the axis in our 2-dimensional chart.
       try:
           with DBOperations.connection.cursor() as cursor:
               sql = "SELECT {},{} FROM listingDetails WHERE postalCode = {} AND category IN ('Apartment','Furnished apartment','Attic apartment','Maisonette','Loft','Penthouse','Terraced Apartment','Terraced condo')".format(
                   varx, varx2, postalCode)
               print(sql)
               cursor.execute(sql)
               data = cursor.fetchall()
               print(data)
               #Creating 2 lists which define the two axis of the chart
               for p in data:
                   if p[varx] is not None and p[varx] not in [0, 1] and p[varx2] is not None and p[varx2] not in [0, 1]:
                       c = p[varx]
                       list.append(c)
                       d = p[varx2]
                       lista.append(d)
               print(lista)
               elements = numpy.array(list)
               mean = numpy.mean(elements, axis=0)
               sd = numpy.std(elements, axis=0)
               listy = [x for x in list if (x > mean - 2 * sd)]
               axis1 = [x for x in listy if (x < mean + 2 * sd)]
               print(axis1)
               #axis1 is the first axis we define with the varx variable

               elements = numpy.array(lista)
               mean = numpy.mean(elements, axis=0)
               sd = numpy.std(elements, axis=0)
               listo = [x for x in lista if (x > mean - 2 * sd)]
               axis2 = [x for x in listo if (x < mean + 2 * sd)]
               print(axis2)
               # axis2 is the first axis we define with the varx variable

       finally:
           cursor.close()
           plt.scatter(axis1, axis2, s=10, color='#2d85cb')
           return (plt.show())

#postalCodes = avgPc(DBOperations("kezenihi_srmidb"))
#postalCodes.distrib(1000, 'size')

#postalCodes = avgPc(DBOperations("kezenihi_srmidb"))

#pc = postalCodes.average(9000, 'price', 'size')
#pc = postalCodes.priceMeter(1000)

# --------------------------------------------------
# In this section we create all the geographical map visualization that are necessary to satisfy our customers' needs.
# For that, we use visuals of maps with colours.

class map:
    def __init__(self):
        postalCodes=1000

    def property(self):
        kanton_map = folium.Map(location=[46.8, 8.33],
                                tiles='Mapbox Bright', zoom_start=7)
        return(kanton_map)
        kanton_map.choropleth(geo_path='switzerland.geojson')
        kanton_map.render()


        #  df = []
        # edit path

        # locs = df[['lat', 'long']]
        #loc_list = locs.values.tolist()

        # To display all data use the following two lines, but, since your data has
        # so many points, this process will be time-consuming.
        #for point in range(0, len(loc_list)):
            #folium.Marker(loc_list[point]).add_to(map_)

kanton_map = folium.Map(location=[46.8, 8.33],
                                tiles='Mapbox Bright', zoom_start=7)
kanton_map.render()