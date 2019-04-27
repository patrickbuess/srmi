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


def getAllPostalCodes(self):
    postalCodeList = []
    if self.DBOperations is None:
        self.DBOperations = DBOperations.getDB()
    self.DBOperations.getConnection()
    try:
        with DBOperations.connection.cursor() as cursor:
            sql = "SELECT * FROM `postalCodes` ORDER BY lastChecked, postalCode ASC"
            cursor.execute(sql)
            codes = cursor.fetchall()
            for code in codes:
                c = code["postalCode"]
                postalCodeList.append(c)
    finally:
        cursor.close()
        return postalCodeList
        print("getAllPostalCodes SUCCESS")

postalCodes = getAllPostalCodes(DBOperations("kezenihi_srmidb"))
postalCodesList = postalCodes.getAllPostalCodes()
pc = postalCodesList[2]
print(pc)
