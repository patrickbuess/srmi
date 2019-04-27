from classDBOperations import *


class UrlList:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    def getAllUrls(self):
        urlList = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `listingURL`"
                cursor.execute(sql)
                urls = cursor.fetchall()
                for url in urls:
                    u = url["url"]
                    urlList.append(u)
        finally:
            print("getAllUrls SUCCESS")
            cursor.close()
            return urlList

    def getUrlsID(self):
        urlList = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `listingURL` WHERE checked = 0 LIMIT 10"
                cursor.execute(sql)
                urls = cursor.fetchall()
                for url in urls:
                    u = url["url"]
                    id = url["listingID"]
                    street = url["street"]
                    postal = url["postalCode"]
                    urlList.append([id, u, street, postal])
        finally:
            cursor.close()
            return urlList
            print("getUrlsID SUCCESS")

    def insertNewUrls(self, urls):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            rows = urls
            values = ', '.join(map(str, rows))
            with DBOperations.connection.cursor() as cursor:
                sql = "INSERT INTO `listingURL`(url, street, postalCode, checked, dateScraped) VALUES {}".format(values)
                cursor.execute(sql)
        finally:
            self.dbOperations.connection.commit()
            print("insertNewUrls SUCCESS")

    def updateUrl(self, date, id):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "UPDATE `listingURL`SET checked = 1, dateChecked = '{}' WHERE listingID = {}".format(date, id)
                cursor.execute(sql)
        finally:
            self.dbOperations.connection.commit()
            print("updateUrl SUCCESS")


class postalCodes:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    def getAllPostalCodes(self):
        postalCodeList = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
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

    def updateLastChecked(self, postalCode, date):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "UPDATE `postalCodes` SET lastChecked = '{}' WHERE postalCode = {}".format(date, postalCode)
                cursor.execute(sql)
        finally:
            self.dbOperations.connection.commit()
            print("updateLastChecked SUCCESS")
