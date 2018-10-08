#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:27:02 2018

@author: mc
"""

def maxTripCoordinates(dataset):
    max_carID = dataset[dataset.TripDistance == dataset.TripDistance.max()]["ID"].iloc[0]
    zz = dataset[dataset.ID == max_carID]
    zz = zz.reset_index()
    id_max = zz.TripDistance.idxmax()
    zz = zz.loc[id_max-1 : id_max]
    start = zz.iloc[0]["EventCoords"].replace("[", "").replace("]", "").split(",")
    print(start[1] + ",", start[0])
    end = zz.iloc[1]["EventCoords"].replace("[", "").replace("]", "").split(",")
    print(end[1] + ",", end[0])
    return dataset[dataset.TripDistance == zz.TripDistance.max()]["ID"].index