#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:32:48 2018

@author: mc
"""

#import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import folium
from math import radians, sin, cos, asin, sqrt

link_install_folium = 'https://www.kdnuggets.com/2018/09/visualising-geospatial-data-python-folium.html'

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
#    nop = int(row[metric])
    
    return zoneid, centroid, mysquare


city = "Torino"
metric = "max-parking"

'''
Upload the data (zones & solutions)
'''
zones = pd.read_csv("./data/Torino_car2go_ValidZones.csv")
fp = open('data/CS_placement.txt')
solutions = fp.read()[1:-1].replace(' ', '').split(',')
for i in range(len(solutions)):
    solutions[i] = int(solutions[i])

'''
find the step in degrees for 500m
'''
step_lon, step_lat, step = find_steps(zones.iloc[132]['Lon'],
                                      zones.iloc[132]['Lat'],
                                      501,
                                      0.00001)
'''
creation of square from centroids
Zones with CS
'''
zones['geometry']=zones.apply(
        lambda x: squareize(x.Lon, x.Lat, step_lon, step_lat),
        axis=1)
CS_in_sol = zones[zones.id.isin(solutions)]

'''
Covert the zones DF into an GeoJson file
'''
outGeoJson = {"type": "FeatureCollection",
              "features":[]
        }
f = open("./data/"+city+"squares.json", 'w')
for i in range(len(zones)):
    a,b,c = createGeoJson(zones.iloc[i], metric)
    geoZone = {}
    geoZone["type"] = "Feature"
    geoZone["zone"] = float(a)
    geoZone["geometry"] = {}
    geoZone["geometry"]["type"] = "Polygon"
    geoZone["geometry"]["coordinates"] = []
    geoZone["geometry"]["coordinates"].append(c)
    outGeoJson["features"].append(geoZone)

'''
Draw on the map a gray square
'''
lat = zones.loc[136]["Lat"]
lon = zones.loc[136]["Lon"]
map_5 = folium.Map(location=[lat,lon], zoom_start=12.25, )
folium.GeoJson(
    outGeoJson,
    style_function=lambda feature: {
        'fillColor': 'gray' ,
        'color': 'black',
        'fillOpacity':0.2,
        'weight': 1,
    }
).add_to(map_5)


'''
Covertion of CS df into GeoJson
'''
outGeoJson = {"type": "FeatureCollection",
              "features":[]
        }
f = open("./data/"+city+"squares_CS.json", 'w')
for i in range(len(CS_in_sol)):
    a,b,c = createGeoJson(CS_in_sol.iloc[i], metric)
    geoZone = {}
    geoZone["type"] = "Feature"
    geoZone["zone"] = float(a)
    geoZone["geometry"] = {}
    geoZone["geometry"]["type"] = "Polygon"
    geoZone["geometry"]["coordinates"] = []
    geoZone["geometry"]["coordinates"].append(c)
    
    outGeoJson["features"].append(geoZone)

'''
Draw on the map the CS coloring the zone with green
'''
folium.GeoJson(
    outGeoJson,
    style_function=lambda feature: {
        'fillColor': 'green' ,
        'color': 'black',
        'fillOpacity':0.9,
        'weight': 1,
    }
).add_to(map_5)


map_5.save("./images/"+city+"_placement.html")










