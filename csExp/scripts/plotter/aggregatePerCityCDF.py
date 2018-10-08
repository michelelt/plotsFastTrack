#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:58:16 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *


'''
Description:
    given ta ditc of cdf computed with the ad hoc function,
    creates the plot of that CDF for each city
    X: sorted data
    Y: yvals
    for each citty in cdfList
'''

def aggreatePerCityCDF(cdfList, dataType, save, path, ax): 

    title = "CDF_aggregate_"+dataType+".pdf"
    if ax == None:
        fig, ax = plt.subplots(1,1,figsize=(9,3))
    ax.grid()
    ax.set_ylabel("CDF",fontsize=ax_lab_fontsize)
    ax.set_ylim(0,1)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    xmax = 0
    for city in colors_dict_city.keys():
        x = cdfList[city][0]
        y = cdfList[city][1]
        
        if (max(x)) > xmax: xmax =max(x)
        
        
        ax.plot(x, y, label=city_eng_names[city] , color=colors_dict_city[city])
    
    if dataType == "RentalsDistance":
        ax.set_xlabel("Driving Distance",fontsize=ax_lab_fontsize)
        ax.set_xscale("log")
        ax.set_xlim(left=700, right=xmax)
        ax.set_xticks([700, 1000, 2000, 5000, 10000, 20000, xmax])
        ax.set_xticklabels(["0.7 km", "1 km", "2 km", "5 km", "10 km", "20 km",str(round(xmax/1000))+" km" ])
        
    elif dataType == "ParkingsDuration":
        ax.set_xlabel("Parkings Duration",fontsize=ax_lab_fontsize)
        ax.set_xscale("log")
        ax.set_xlim(0.083, 48)
        ax.set_xticks([0.083, 0.33, 1, 5, 12, 24, 48])
        ax.set_xticklabels(["5 min","20 min","1 h","5 h","12 h","1 d","2 d"])
        
    elif  dataType == "RentalsDuration":
        ax.set_xlabel("Rentals Duration [min]",fontsize=ax_lab_fontsize)
        ax.set_xticks([2,10,20,30,40,50,60])
        ax.set_xticklabels(["2","10",
                            "20","30","40",
                            "50","60"])
        ax.set_xlim(0, 60)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=4, mode="expand", borderaxespad=0., edgecolor="white",
        prop={'size': legend_fontsize})
        
        
    ax.tick_params(labelsize=ticks_fontsize)
        
    if save:
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
        
    return ax