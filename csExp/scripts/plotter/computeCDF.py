#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:54:21 2018

@author: mc
"""
from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    given two logs file, passed as df return
    the cdf in terms of list on to plot on x and y data
    X: sorted data
    Y: yvals
'''


def computeCDF(df, metric, city):
    
    if metric == "RentalsDistance":
        df = df[df.Type == "e"]
        metric = "TripDistance"
        y_set = df[metric]
        max_ticks = df[metric].max()
        print (max_ticks, "[m]")
        y_set = df[metric]
        
        
    elif metric == "ParkingsDuration":
        cars_id = df.ID.unique()
        dur = pd.Series()
        for ID in cars_id:
            tmp = df[df["ID"]== ID]
            tmp = tmp.reset_index()
            a_start = tmp.loc[2::2, "Stamp"].reset_index()["Stamp"]
            a_end = tmp.loc[1::2, "Stamp"].reset_index()["Stamp"]
            dur = dur.append(a_start-a_end)
            
            if len(dur[dur < 0 ]) > 0:
                print ("Algorithm wrong")
        y_set = dur.dropna()
        y_set = y_set.div(3600)
        y_set = y_set[y_set >= 0.083]

    
    elif  metric == "RentalsDuration":
        df.ID.astype(int)
        df = df.sort_values(by=["ID", "Stamp"])
        starts = df[df["Type"] == 's'].reset_index()
        ends = df[df["Type"] == 'e'].reset_index()
        y_set = ends["Stamp"].div(60) - starts["Stamp"].div(60)


    else:
        return
    
    values = y_set
    sorted_data = np.sort(values)
    yvals=np.arange(len(values))/float(len(values)-1)
    print("Sorted data len:", len(sorted_data))
    
    return [sorted_data, yvals]