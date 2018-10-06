#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 20:18:12 2018

@author: mc
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from math import *
from shapely.geometry import MultiPoint, Polygon, Point
import mplleaflet



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

'''
Upload the data (zones & solutions)
'''
zones = pd.read_csv('data/Torino_car2go_ValidZones.csv')
fp = open('data/CS_placement.txt')
solutions = fp.read()[1:-1].replace(' ', '').split(',')
for i in range(len(solutions)):
    solutions[i] = int(solutions[i])

step_lon, step_lat, step = find_steps(zones.iloc[132]['Lon'],
                                      zones.iloc[132]['Lat'],
                                      501,
                                     0.00001)
'''
from pandas -> GeoPandas, and isolation of CS
'''
zones['geometry']=zones.apply(
        lambda x: squareize(x.Lon, x.Lat, step_lon, step_lat),
        axis=1)
zones=gpd.GeoDataFrame(zones,
                    geometry = zones.geometry,
                    crs={'init':'epsg4832'})
CS_in_sol = zones[zones.id.isin(solutions)]


fig,ax= plt.subplots(1,1,figsize=(10,10))

'''Plot all zones in red'''
zones.plot(ax=ax, color='red')

'''Plot the CS in green'''
CS_in_sol.plot(ax=ax, color='green')

'''Labels each zone with its ID'''
for i, txt in enumerate(zones.id):
    ax.annotate(txt, (zones.Lon[i]-0.003, zones.Lat[i]-0.002), size=6,
                      color='black')

'''
Add in backgrpund the map
Another library form cool_mapping.py
Labeling does not work with this library
comment to have the map without cartography in background
'''
mplleaflet.show(fig=ax.figure)







