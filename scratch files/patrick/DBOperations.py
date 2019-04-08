import pymysql


class DBOperations:
    def __init__(self, DB_NAME, DB_USER='srmidbuser', DB_PASSWORD='ykXo4q2pAKaPsj7Ag', connection=None):
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
                                        host='80.74.128.5',
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
