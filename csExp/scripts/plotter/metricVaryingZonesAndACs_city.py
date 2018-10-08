#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:37:42 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

def metricVaryingZonesAndAcs_city(dict_df, metric, save, path): 

    
    fig,ax = plt.subplots(1,1,figsize=(12,4))
    if metric in ['AvgWalkedDistance', 'AvgTimeInStation']:
        ax.grid(which="both")
    else: ax.grid()
    if metric == 'Deaths': 
        ax.set_yscale('log')

    for city in colors_dict_city.keys():
        tmp = dict_df[city]
        tmp = tmp[tmp['Policy'] == 'Hybrid']
        
        maxZones =  dict_df[city].Zones.max()
        Zones = list(tmp.Zones.mul(100/maxZones))

        if metric == 'Deaths': 
            mul= 100/tmp.iloc[0]['TypeE']
        elif metric == 'AvgWalkedDistance': 
            mul = 1/1000
            ax.set_yticks([1,2,3,4,5,10])
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            
        elif metric =='AvgTimeInStation' : 
            mul = 1/3600
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
            ax.set_yticks([1,2,3,4,5,10])
        else :mul=1
        
        ax.plot(Zones, tmp[metric].mul(mul),label=city_eng_names[city], 
                color=colors_dict_city[city])
        

    ax.set_xticks([1,5,10,25,50,100])
    ax.set_xlim([0,100])
    ax.tick_params(labelsize=ticks_fontsize)
    ax.set_xlabel("Pole spread [%]", fontsize=ax_lab_fontsize)
    
    if metric == 'AvgTimeInStation': ax.set_yticks([1,2,3,4,5,10])
        
    ax.set_ylabel(my_labels[metric], fontsize=ax_lab_fontsize-1)

    if metric == 'Deaths':
        ax.legend(prop={'size': legend_fontsize}, 
              loc='upper center', ncol=4,edgecolor="white",mode='expand',
              bbox_to_anchor=(0., 1.02, 1., .15)
              
              )
    
    if metric == 'AvgWalkedDistance' :
        ax.set_ylim([0,5])


    if save:
        title = "%s_vsZones_ACS.pdf" % (metric)
        plt.savefig(path+title,  bbox_inches = 'tight', format='pdf')

    return 
