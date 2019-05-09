import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import geopandas as gpd
# import pysal as ps
import seaborn as sns
from pyproj import Proj, transform
from shapely.geometry import Point
import pandas as pd
import numpy
# from pysal.contrib.viz import mapping as maps
from classes.classDBOperations import DBOperations
# from shapely.ops import transform
# from functools import partial
# import pyproj


class createMaps:
    def __init__(self, dbOperations=None):
        self.dbOperations = dbOperations

    def mapAllListingsCH(self, shapefile=gpd.GeoDataFrame.from_file('datasets/PLZO_SHP_LV03/PLZO_OS.shp')):
        locations = []
        if self.dbOperations is None:
            self.dbOperations = DBOperations.getDB()
        self.dbOperations.getConnection()
        try:
            with DBOperations.connection.cursor() as cursor:
                sql = "SELECT * FROM `listingDetails` WHERE (latitude <= 47.829906 AND latitude >= 45.795286 AND longitude >= 5.855986 AND longitude <= 10.584407) "  # WE ONLY COMPARE NEWLY SCRAPED URLS WITH URLS FROM THE LAST 6 MONTHS, AFTER THAT CHANCE IS SMALL THAT A LISTING IS STILL ONLINE
                cursor.execute(sql)
                items = cursor.fetchall()
                for item in items:
                    if item["latitude"] is not None:
                        lat = float(item["latitude"])
                        long = float(item["longitude"])
                        if item['price'] is not None and item['size'] is not None:
                            price = float(item["price"])
                            size = int(item['size'])
                            locations.append({"latitude":lat,"longitude":long,"price":price,"size":size})

                df = pd.DataFrame(locations, columns = ['latitude', 'longitude',"price","size"])
                df['pricePerSq'] = df.apply(lambda row: (row.price / row.size) ** 0.5, axis=1)

                # CONVERT SHAPEFILE
                shp = shapefile.to_crs(epsg=4326)

                # CREATE GEO DATAFRAME
                geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
                df = df.drop(['longitude', 'latitude'], axis=1)
                gdf = gpd.GeoDataFrame(df, geometry=geometry)

                # TAKE OUT EXTREME VALUES FROM SET
                elements=numpy.array(gdf['pricePerSq'])
                mean= numpy.mean(elements, axis=0)
                sd=numpy.std(elements, axis=0)
                gdf = gdf.loc[gdf['pricePerSq'] > (mean - 2 * sd)]
                gdf = gdf.loc[gdf['pricePerSq'] < (mean + 2 * sd)]

                # CREATE plot
                vmin, vmax = gdf['pricePerSq'].min(), gdf['pricePerSq'].max()
                print(gdf['pricePerSq'].max())
                cmap = sns.cubehelix_palette(as_cmap=True)
                base = shp.plot(figsize=(40, 20), linewidth=0.25, edgecolor='#999999', color='#ffffff')
                points = gdf.plot(markersize=20, column='pricePerSq', s='pricePerSq', k=100, cmap=cmap, legend=True, alpha=0.5, vmin=vmin, vmax=vmax, ax=base)
                fig = points.get_figure()
                cax = fig.add_axes([0, 5, 10, 20])
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
                sm._A = []
                fig.colorbar(sm, cax=cax)
                # sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=plt.Normalize(vmin=vmin, vmax=vmax))
                # set_axis_off(points)
                # colorbar(points)
                # points.legend(title="legend")

        finally:
            print("create mapAllListingsCH SUCCESS")
            cursor.close()
            plt.show()
