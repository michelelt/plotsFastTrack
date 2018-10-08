#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:23:46 2018

@author: mc
"""

'''
Descritpion:
    service function, validates the construction of parkigns from bookings dataset
'''

def checkStartEndsAlternates(df):

    cars_id = df.ID.unique()
    for ID in cars_id:
        tmp = df[df["ID"]== ID]
        for i in range(len(tmp)-1):
            currentType = tmp.iloc[i]["Type"]
            if currentType == tmp.iloc[i+1]["Type"]:
                print ("errore")
    return