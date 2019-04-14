import DBOperationsrb


class testDB:
    def __init__(self, dbOperationsrb=None):
        self.dbOperationsrb = dbOperationsrb

    def insertTestTable(self, name):
        if self.dbOperationsrb is None:
            self.dbOperationsrb = DBOperationsrb.getDB()
        self.dbOperationsrb.getConnection()
        try:
            # enter tinder credentials
            with DBOperationsrb.connection.cursor() as cursor:
                params = ['?' for i in list]
                sql = "INSERT INTO `testTable`(name, col2,col3,col4) VALUES (%s)" % ','.join(params)
                cursor.execute(sql, list)

        finally:
            self.dbOperationsrb.connection.commit()
            print("SUCCESS")

# def nameInsert(name):
#     try:
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO `testTable` (name) VALUES (%s)"
#             cursor.execute(sql, [name])
#     finally:
#         connection.commit()
#
# nameInsert("Oslo")


db = DBOperationsrb("srmidb")
test = testDB(db)
test.insertTestTable("Ruben Test 1, 2,3,4")
