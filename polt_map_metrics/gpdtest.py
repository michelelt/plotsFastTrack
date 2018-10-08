#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:32:48 2018

@author: mc
"""

#import geopandas as gpd
import pandas as pd
import contextily as ctx
from shapely.geometry import Point, Polygon
from IPython.display import IFrame
import matplotlib.pyplot as plt
import folium
import seaborn as sns
import numpy as np
import pprint
from math import *

import json
from shapely.geometry import shape, mapping
import branca.colormap as cm

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return int(km*1000)

def find_steps(min_lon,min_lat, side_length, epsilon):
    step_lon = 0.01
    epsilon = epsilon
    dist = 1000
    step = 0
    while 1:
        if dist >= side_length-epsilon and dist <=side_length + epsilon:
            break
        
        elif dist < 500-epsilon:
            step_lon += step_lon*0.5
        else:
            step_lon -= step_lon*0.5
            
        dist = haversine(min_lon, min_lat, min_lon+step_lon, min_lat)
        
    step_lat = 0.01
    epsilon = epsilon
    dist = 1000
    step = 0
    while 1:
        if dist >= side_length-epsilon and dist <=side_length + epsilon:
            break
        
        elif dist < 500-epsilon:
            step_lat += step_lat*0.5
        else:
            step_lat -= step_lat*0.5
            
        dist = haversine(min_lon, min_lat, min_lon, min_lat+step_lat)
#         

    return step_lon, step_lat, step

def squareize(lon_c, lat_c, step_lon, step_lat):
    A = (lon_c - step_lon/2, lat_c + step_lat/2)
    B = (lon_c + step_lon/2, lat_c + step_lat/2)
    C = (lon_c + step_lon/2, lat_c - step_lat/2)
    D = (lon_c - step_lon/2, lat_c - step_lat/2)
    
    return Polygon([A,B,C,D])


def createGeoJson(row, metric):
    
    areaID = row["id"]
    polygon = row["geometry"]
    lon, lat = polygon.exterior.coords.xy

    mysquare = [[lon[0],lat[0]],
                [lon[1],lat[1]],
                [lon[2],lat[2]],
                [lon[3],lat[3]],
                [lon[0],lat[0]]
                ]
    zoneid = str(int(row["id"]))
    centroid = [row["Lat"], row["Lon"]]
    nop = int(row[metric])
    
    return zoneid, nop,centroid, mysquare

city = "Torino"
metric = "AvgTime"

'''
Upload the data (zones & solutions)
'''
df = pd.read_csv("./data/Torino_car2go_ValidZones.csv")

'''
find the step in degrees for 500m
'''
step_lon, step_lat, step = find_steps(df.iloc[132]['Lon'],
                                      df.iloc[132]['Lat'],
                                      501,
                                      0.00001)

'''
creation of square from centroids
'''
df['geometry']=df.apply(
        lambda x: squareize(x.Lon, x.Lat, step_lon, step_lat),
        axis=1)



outGeoJson = {"type": "FeatureCollection",
              "features":[]
        }
f = open("./data/"+city+"squares.json", 'w')

for i in range(len(df)):
    if df.iloc[i]['id'] < 0: continue
    a,b,c,d = createGeoJson(df.iloc[i], metric)
    geoZone = {}
    geoZone["type"] = "Feature"
    geoZone["zone"] = float(a)
    geoZone["properties"] = {metric:b}
    geoZone["geometry"] = {}
    geoZone["geometry"]["type"] = "Polygon"
    geoZone["geometry"]["coordinates"] = []
    geoZone["geometry"]["coordinates"].append(d)
    outGeoJson["features"].append(geoZone)
    
linear = cm.LinearColormap(
    ['b', 'c', 'g', 'y', 'r'],
    vmin=df[metric].quantile(0.01), 
    vmax=df[metric].quantile(0.95),
    caption = 'Number of Parkings'
)
maxparking_dict = df.set_index("id")[metric]

lat = df.loc[136]["Lat"]
lon = df.loc[136]["Lon"]
map_5 = folium.Map(location=[lat,lon], zoom_start=12.25, )
folium.GeoJson(
    outGeoJson,
    style_function=lambda feature: {
        'fillColor': linear(maxparking_dict[ feature['zone'] ]),
        'color': 'black',
        'fillOpacity':0.7,
        'weight': 1,
#        'dashArray': '5, 5'
    }
).add_to(map_5)
#map_5.add_child(linear)


m = map_5
m.save("./images/"+city+"_"+metric+".html")
m
#










