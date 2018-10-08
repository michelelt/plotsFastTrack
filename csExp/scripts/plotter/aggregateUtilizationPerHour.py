#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:32:26 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Default:
    given the cities passed as aprameter
    plot the bookings per day of each booking dataset
'''

def aggregateUtilizastionPerHour(cities, save, path):
    colors  = {"Vancouver":"green", "Berlino":"orange",  "Milano":"red", "Torino":"blue", }
    tmp = pd.DataFrame()
    df = pd.DataFrame()
    i=0
    for city in cities:
        tmp = pd.read_csv("../data"+city+"/bookings_per_hour_"+city+".csv")
        df = df.append(tmp)
                
    fig, ax = plt.subplots(1,1,figsize=(9,3))
    ax.grid()
    ax.set_xlabel("Hour", fontsize=ax_lab_fontsize)
    ax.set_ylabel("Avg rentals per hour", fontsize=ax_lab_fontsize)
    
    i=0
    qqq = []
    legend_elements = []
    for city in colors_dict_city.keys():
        tmp = df[df["city"].str.contains(city[0:4])]
        print("len", len(tmp))

        ax.plot(tmp.dayHour, tmp.WD_BPH_mean, label=city_eng_names[city] + "WD", color=colors[city])
        ax.plot(tmp.dayHour, tmp.WE_BPH_mean, label=city_eng_names[city] + "WE", color=colors[city], linestyle='--')
        legend_elements.append(Line2D([0], [0], marker='o', markerfacecolor=colors_dict_city[city], 
                                      label=city_eng_names[city], color='w', markersize=10))
        
    ax.set_xticks(df.dayHour.unique())
    ax.set_xticklabels([str(hour) for hour in list(df.dayHour)], rotation=45)
    
    ax.tick_params(labelsize=ticks_fontsize)
    legend_elements2=[]
    legend_elements2.append(Line2D([0], [0], color='black', lw=2, label='WD'))
    legend_elements2.append(Line2D([0], [0], color='black', lw=2, ls='--', label='WE'))
    
    city_legend = plt.legend(handles=legend_elements, 
                             prop={'size': legend_fontsize}, ncol =4,
                             bbox_to_anchor=(0., 1.02, 1,0),
                             mode="expand", borderaxespad=0., edgecolor="white"
                             )
    ax.add_artist(city_legend)
    
    ax.legend(handles=legend_elements2, prop={'size': legend_fontsize}, ncol=4,loc='center',
              bbox_to_anchor=(0., 1.02, 0.9, 0.4), borderaxespad=0., edgecolor="white"
              )
    
    ax.set_xlim([0,23])
    if save:
        
        plt.savefig(path+"aggBookginfsPerHour.pdf", 
                    bbox_inches = 'tight', format='pdf')
    return df