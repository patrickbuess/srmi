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
import matplotlib.pyplot
import statistics

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
   def average(self):
       list = []
       postalCode= 1000
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       try:
           with DBOperations.connection.cursor() as cursor:
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {}".format('price', postalCode)
               cursor.execute(sql)
               list = cursor.fetchall()
               numeric_types = [int, float, complex]
               list = [x for x in list if type(x) in numeric_types]
               #price = statistics.mean(list)

       finally:
           cursor.close()
           return list

#Get the price of all the properties in the postal code area to make a distribution graph with it
       # Get the price of all the properties in the postal code area to make a distribution graph with it
   def distrib(self):
       list = []
       postalCode = 1000
       if self.dbOperations is None:
           self.dbOperations = DBOperations.getDB()
       self.dbOperations.getConnection()
       try:
           with DBOperations.connection.cursor() as cursor:
               sql = "SELECT {} FROM listingDetails WHERE postalCode = {} AND category NOT IN ('Parking space','Parking space')".format('price', postalCode)
               print(sql)
               cursor.execute(sql)
               data = cursor.fetchall()
               for p in data:
                   if p['price'] is not None and p['price']<10000 and p['price']>100:
                      c = p['price']
                      list.append(c)

       finally:
           cursor.close()
           plt.hist(list, color='#2d85cb', edgecolor='black', bins=int(180 / 5))
           return (plt.show())
           return list
           return len(list)

postalCodes = avgPc(DBOperations("kezenihi_srmidb"))
postalCodes.distrib()
postalCodes = avgPc(DBOperations("kezenihi_srmidb"))
pc = postalCodes.average()
print(pc)

# --------------------------------------------------
