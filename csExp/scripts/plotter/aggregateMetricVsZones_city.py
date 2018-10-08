#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:08:44 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X: zones percentage, 
    Y: deaths
    for each city, for each policy in [FF, Needed== hybridW=0]
'''

def aggregateMetricVsZones_city(init_df, save, path):
    
    title = "DeathsVsZones_city.pdf"
    
    fig,ax = plt.subplots(1,1,figsize=(9,3))
    ax.grid()
    legend_elements = []
    
    outList = []
    for city in colors_dict_city.keys():
        if city not in init_df.keys(): continue
        df = init_df[city] 
        df = df[df["Acs"] == 4]
        df = df[df["Algorithm"] == 'max-parking']
        df = df[df["pThreshold"] == 0]
        df = df[df["Policy"] == 'Needed']
        df = df[df["TankThreshold"] ==  25]
        df['ZonesPerc'] = df['Zones'].mul(100).div(numeberOfZones(city))
        outList.append(df)
#        
        NoB = df.iloc[0]["TypeE"]
#        
#        ax.plot(df["ZonesPerc"], df["Deaths"].mul(100).div(NoB), 
#                color = colors_dict_city[city], label=city_eng_names[city]+ " W:0")
        ax.plot(df["ZonesPerc"], df["Deaths"].mul(100).div(NoB), 
                color = colors_dict_city[city], label="Forced")
        
        df = init_df[city] 
        df = df[df["Acs"] == 4]
        df = df[df["Algorithm"] == 'max-parking']
        df = df[df["pThreshold"] == 0]
        df = df[df["Policy"] == 'FreeFloating']
        df['ZonesPerc'] = df['Zones'].mul(100).div(numeberOfZones(city))
        outList.append(df)
                
#        ax.plot(df["ZonesPerc"], df["Deaths"].mul(100).div(NoB), 
#                color=colors_dict_city[city], linestyle="--")
        ax.plot(df["ZonesPerc"], df["Deaths"].mul(100).div(NoB), 
                color=colors_dict_city[city], linestyle="--", label='Free Floating')
        
        legend_elements.append(Line2D([0], [0], marker='o', markerfacecolor=colors_dict_city[city], 
                                      label=city_eng_names[city], color='w', markersize=10))
    
    legend_elements2=[]
    legend_elements2.append(Line2D([0], [0], color='black', lw=2, ls='--', label='Free Floating'))
    legend_elements2.append(Line2D([0], [0], color='black', lw=2, label='Forced'))
    
#    city_legend = plt.legend(handles=legend_elements, 
#                             prop={'size': legend_fontsize}, ncol =4,
#                             bbox_to_anchor=(0., 1.02, 1, 1.02),
#                             mode="expand", borderaxespad=0., edgecolor="white"
#                             )
#    ax.add_artist(city_legend)
#    ax.legend(handles=legend_elements2, prop={'size': legend_fontsize}, ncol=4,loc='center',
#              bbox_to_anchor=(0., 1.02, 0.9, 0.3), borderaxespad=0., edgecolor="white"
#              )
    ax.legend(prop={'size': legend_fontsize})
        
    ax.tick_params(labelsize=ticks_fontsize)
    
    ax.set_xlim(0,20)
    ax.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
    
    ax.set_ylim(-1,40)
    ax.set_ylabel(my_labels["Deaths"], fontsize=ax_lab_fontsize)
        
    if save:
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
        
    return outList