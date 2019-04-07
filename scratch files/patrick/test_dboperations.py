from DBOperations import DBOperations
import pymysql

class testDB:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations


    def insertTestTable(self,name):
        if self.dbOperations == None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            # enter tinder credentials
            with DBOperations.connection.cursor() as cursor:
                sql = "INSERT INTO `testTable`(name) VALUES (%s)"
                cursor.execute(sql, [name])

        finally:
            self.dbOperations.connection.commit()
            print("SUCCESS")



# def nameInsert(name):
#     try:
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO `testTable` (name) VALUES (%s)"
#             cursor.execute(sql, [name])
#     finally:
#         connection.commit()
#
#
# nameInsert("Oslo")

db = DBOperations("srmidb")
test = testDB(db)
test.insertTestTable("Oslo 2")
