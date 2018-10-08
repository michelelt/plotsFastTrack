#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:14:26 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

def aggregateBookingsPerDay(save, path):
    grouepd_df = {}

    colors  = {"Vancouver":"green", "Berlino":"orange",  "Milano":"red", "Torino":"blue", }

    grouepd_df["Milano"] = pd.read_csv('../dataMilano/bookings_per_day_Milano.csv')
    grouepd_df["Torino"]= pd.read_csv('../dataTorino/bookings_per_day_Torino.csv')
    grouepd_df["Berlino"] = pd.read_csv('../dataBerlino/bookings_per_day_Berlino.csv')
    grouepd_df["Vancouver"] = pd.read_csv('../dataVancouver/bookings_per_day_Vancouver.csv')
    

    
    fig, ax = plt.subplots(1,1, figsize=(9,3))
    for city in colors_dict_city.keys():
        ax.plot(grouepd_df[city].dayYear, grouepd_df[city].BPD_count,
                color=colors_dict_city[city], label=city_eng_names[city])
        
    ax.grid()

    ax.set_xlabel("Day", fontsize=ax_lab_fontsize)
    ax.set_ylabel("Rentals per day", fontsize=ax_lab_fontsize)
    
    weeks_tikcs = [day for day in range(248, 305, 7) ]
    weeks_tikcs_labels = [(datetime.datetime(2017,1,1) +\
                          datetime.timedelta(days=day-1)
                          ).strftime("%d %b %y") for day in weeks_tikcs]
#                    
                    
    ax.set_xticks(weeks_tikcs)
    ax.set_xticklabels(weeks_tikcs_labels, rotation=15, ha='right')
    ax.set_xlim(247, 304)
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    ncol=4, mode="expand", borderaxespad=0., edgecolor="white",
    prop={'size': legend_fontsize})
    ax.tick_params(labelsize=ticks_fontsize)
    
    if save:
        plt.savefig(path+"bookings_per_day.pdf",  bbox_inches = 'tight', format='pdf')
        
    return grouepd_df