from scraper.classDBOperations import *

class listingObject:
    def __init__(self,
                 dbOperations=None,
                 listingID=None,
                 category=None,
                 postalCode=None,
                 address=None,
                 latitude=None,
                 longitude=None,
                 price=None,
                 pricePerDay=None,
                 pricePerWeek=None,
                 pricePerYear=None,
                 primaryCosts=None,
                 additionalCosts=None,
                 size=None,
                 floorSpace=None,
                 propertyArea=None,
                 rooms=None,
                 floor=None,
                 available=None,
                 construction=None,
                 elevator=0,
                 balconies=0,
                 motorway=None,
                 shops=None,
                 publicTransport=None,
                 description=None,
                 kindergarten=None,
                 primarySchool=None,
                 secondarySchool=None,
                 minergie=0,
                 pets=0,
                 childFriendly=0,
                 cableTV=0,
                 newBuilding=0,
                 wheelchair=0,
                 parkingIndoor=0,
                 parkingOutdoor=0,
                 veranda=0,
                 pool=0
                 ):
        self.dbOperations = dbOperations
        self.listingID = listingID
        self.category = category
        self.postalCode = postalCode
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.price = price
        self.pricePerDay = pricePerDay
        self.pricePerWeek = pricePerWeek
        self.pricePerYear = pricePerYear
        self.primaryCosts = primaryCosts
        self.additionalCosts = additionalCosts
        self.size = size
        self.floorSpace = floorSpace
        self.propertyArea = propertyArea
        self.rooms = rooms
        self.floor = floor
        self.available = available
        self.construction = construction
        self.elevator = elevator
        self.balconies = balconies
        self.motorway = motorway
        self.shops = shops
        self.publicTransport = publicTransport
        self.description = description
        self.kindergarten = kindergarten
        self.primarySchool = primarySchool
        self.secondarySchool = secondarySchool
        self.minergie = minergie
        self.pets = pets
        self.childFriendly = childFriendly
        self.cableTV = cableTV
        self.newBuilding = newBuilding
        self.wheelchair = wheelchair
        self.parkingIndoor = parkingIndoor
        self.parkingOutdoor = parkingOutdoor
        self.veranda = veranda
        self.pool = pool

    def insertInfos(self, table, columns, listings):
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            rows = listings
            values = ', '.join(map(str, rows))
            with DBOperations.connection.cursor() as cursor:
                sql = "INSERT INTO `{}` {} VALUES {}".format(table, columns, values)
                cursor.execute(sql)
        finally:
            self.dbOperations.connection.commit()
            print("SUCCESS insertInfos")
