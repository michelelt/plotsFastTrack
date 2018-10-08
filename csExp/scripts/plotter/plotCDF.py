#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:00:23 2018

@author: mc
"""
from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    given df as dataset composed by only one city, return the CDF
    X: sorted data
    Y: yvals
'''


def plotCDF(dataset, metric, save=False, city="", path="" ):
    title = "CDF_" +city+ "_" + metric+".pdf"
    fig, ax = plt.subplots(1,1,figsize=(9,3))
    ax.grid()
    
    ax.set_title(city)
    ax.set_ylabel("CDF",fontsize=ax_lab_fontsize)
    ax.set_ylim(0,1)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    
    yvals = dataset[1]
    sorted_data = dataset[0]
    xmax = max(sorted_data)
    ax.tick_params()
    
    if metric == "RentalsDistance":
        print(1)
        ax.set_xlabel("Rentals Distance", fontsize=ax_lab_fontsize)
        ax.set_xscale("log")
        ax.set_xlim(left=700, right=xmax)
        ax.set_xticks([700, 1000, 5000, 10000, xmax])
        ax.set_xticklabels(["0.7 km", "1 km", "5 km", "10 km", str(round(xmax/1000))+" km" ])
        
    elif metric == "ParkingsDuration":
        print(2)
        ax.set_xlabel("Parkings Duration", fontsize=ax_lab_fontsize)
        ax.set_xscale("log")
        ax.set_xticks([0.083,0.33,1,5,12,24,48])
        ax.set_xticklabels(["5 min","20 min","1 h","5 h","12 h","1 d","2 d"])
        ax.set_xlim(0.083, 48)
        
    elif  metric == "RentalsDuration":
        print(3)
        ax.set_xlabel("Rentals Duration", fontsize=ax_lab_fontsize)
#        ax.set_xscale("log")
        ax.set_xticks([2,10,20,30,40,50,60])
        ax.set_xticklabels(["2 min","10 min",
                            "20 min","30 min","40 min",
                            "50 min","1h"])
        ax.set_xlim(0, 60)
    else:
        return
    
    ax.plot(sorted_data, yvals)

#    plt.legend(loc=4, fontsize=fontsize)
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return [sorted_data, yvals]