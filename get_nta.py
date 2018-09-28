

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import geopandas as gpd

# https://towardsdatascience.com/lets-make-a-map-using-geopandas-pandas-and-matplotlib-to-make-a-chloropleth-map-dddc31c1983d
# https://data.cityofnewyork.us/City-Government/NTA-map/d3qk-pfyz
map_df = gpd.read_file("./geo_export_ed304d49-3aaf-4cbd-9c75-28380a34d7c6.shp")
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe

df = pd.read_csv('./nta-metadata-3.csv')
df = df.iloc[1:]
df = df.reset_index(drop=True)

df = df[['NTA_Code','PreventHosp']]
merged = map_df.set_index('ntacode').join(df.set_index('NTA_Code'))
merged =merged.replace(np.nan, 0)
merged = merged.loc[merged['PreventHosp'] != 0]
merged = merged.reset_index()
merged['centroid'] = merged['geometry'].centroid

from shapely.geometry import Point, Polygon
import geopandas

# https://stackoverflow.com/questions/48097742/geopandas-point-in-polygon
def coord_to_ntacode(lat, long, polys):
    pnt = Point(long, lat)
    for i in range(len(polys)):
        if pnt.within(polys['geometry'][i]):
            return polys.loc[i, 'ntacode']
    else:
        return 'null'

def min_dist(lat, long, gpd2):
    point = Point(long, lat)
    gpd2['Dist'] = gpd2.apply(lambda row:  point.distance(row.geometry),axis=1)
    geoseries = gpd2.iloc[gpd2['Dist'].argmin()]
    return geoseries['ntacode']

print(min_dist(40.63, -73.93, merged))


service_requests_df = pd.read_csv('./Materials/311_service_requests.csv')
service_requests_df['ntacode'] = ''
service_requests_df.shape

for i in range(len(service_requests_df)):
    print(i)
    service_requests_df.loc[i, 'ntacode'] = min_dist(service_requests_df.loc[i, 'latitude'], service_requests_df.loc[i, 'longitude'], merged)
service_requests_df.to_csv('service_requests_df.csv')
