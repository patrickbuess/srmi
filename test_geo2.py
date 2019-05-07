import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import geopandas as gpd
import pysal as ps
from pyproj import Proj, transform
from shapely.geometry import Point
import pandas as pd
from pysal.contrib.viz import mapping as maps
from classDBOperations import *
from shapely.ops import transform
from functools import partial
import pyproj
#
# lsoas_link = "PLZO_SHP_LV03/PLZO_OS.shp"
# lsoas = gpd.read_file(lsoas_link)
#
# f, ax = plt.subplots(1, figsize=(12, 12))
# ax = lsoas.plot(axes=ax)
# plt.show()


class createMaps:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    def getAllGeoData(self):
        locations = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `listingDetails` WHERE (latitude >= 40 AND latitude <= 50 AND longitude >= 4 AND longitude <= 8) "  # WE ONLY COMPARE NEWLY SCRAPED URLS WITH URLS FROM THE LAST 6 MONTHS, AFTER THAT CHANCE IS SMALL THAT A LISTING IS STILL ONLINE
                cursor.execute(sql)
                items = cursor.fetchall()
                for item in items:
                    if item["latitude"] is not None:
                        lat = float(item["latitude"])
                        long = float(item["longitude"])
                        locations.append({"latitude":lat,"longitude":long})
        finally:
            print("getAllLocations SUCCESS")
            cursor.close()
            return locations


locations = createMaps(DBOperations('kezenihi_srmidb3'))
locations = locations.getAllGeoData()
lats = [x['latitude'] for x in locations]
long = [x['longitude'] for x in locations]
df = pd.DataFrame(locations, columns = ['latitude', 'longitude'])
# df = df.head(100)
lats = []
long = []
for i in range(100):
    lats.append(locations[i]['latitude'])
    long.append(locations[i]['longitude'])
print(lats)
print(long)



shp = gpd.GeoDataFrame.from_file('PLZO_SHP_LV03/PLZO_OS.shp')
shp.crs  # {'init': 'epsg:21781'}

#
# shp.crs = {'init': 'epsg:4326'}
# shp = shp.to_crs({'init': 'epsg:4326'})

project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:21781'), # source coordinate system
    pyproj.Proj(init='epsg:4326')) # destination coordinate system

shp2 = transform(project, shp)
# shp.plot()
# plt.show()


geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
df = df.drop(['longitude', 'latitude'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(df, geometry=geometry)
gdf.crs
gdf = gdf.to_crs(epsg=4326)
gdf.crs = {'init': 'epsg:4326'}
gdf_2 = gdf.to_crs({'init': 'epsg:4326'})




base = shp.plot(linewidth=0.25, edgecolor='white', color='lightgrey')
points = gdf.plot(markersize=10, color='pink', alpha=0.5, ax=base)

plt.show()
