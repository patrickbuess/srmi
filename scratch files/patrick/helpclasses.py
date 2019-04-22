from DBOperations import DBOperations


class UrlList:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    def getAllUrls(self):
        urlList = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            # enter tinder credentials
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `UrlList`"
                cursor.execute(sql)
                urls = cursor.fetchall()
                for url in urls:
                    u = url["url"]
                    urlList.append(u)
        finally:
            print("SUCCESS")
            cursor.close()
            return urlList

    def insertNewUrls(self, urls):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            rows = urls
            values = ', '.join(map(str, rows))

            with DBOperations.connection.cursor() as cursor:
                sql = "INSERT INTO `UrlList`(url, checked, date) VALUES {}".format(values)
                cursor.execute(sql)
        finally:
            self.dbOperations.connection.commit()
