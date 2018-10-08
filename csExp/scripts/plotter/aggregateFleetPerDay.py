#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:35:05 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *



def aggregateFleetPerDay(save, path):
    df_list = {}
    grouepd_df = {}


    df_list["Milano"] = pd.read_csv('../dataMilano/Milano_completeDataset.csv')
    df_list["Torino"]= pd.read_csv('../dataTorino/Torino_completeDataset.csv')
    df_list["Berlino"] = pd.read_csv('../dataBerlino/Berlino_completeDataset.csv')
    df_list["Vancouver"] = pd.read_csv('../dataVancouver/Vancouver_completeDataset.csv')
        
    
    for city in df_list.keys():
        df = df_list[city]
        df["dayYear"] = df.apply(lambda x :datetime.datetime.fromtimestamp(x.init_time).timetuple().tm_yday, axis=1 )
        grouepd_df[city] = df.groupby('dayYear').agg({"plate":pd.Series.nunique})
        


    
    fig, ax = plt.subplots(1,1, figsize=(9,3))
    for city in colors_dict_city.keys():
        ax.plot(grouepd_df[city], color=colors_dict_city[city], label=city_eng_names[city])
        
    ax.grid()

    ax.set_xlabel("Day", fontsize=ax_lab_fontsize)
    ax.set_ylabel("Average Fleet per day",fontsize=ax_lab_fontsize)
    
    weeks_tikcs = [day for day in range(248, 305, 7) ]
    weeks_tikcs_labels = [(datetime.datetime(2017,1,1) +\
                          datetime.timedelta(days=day)
                          ).strftime("%d %b %y") for day in weeks_tikcs]
                    
                    
    ax.set_xticks(weeks_tikcs)
    ax.set_xticklabels(weeks_tikcs_labels, rotation=15, ha='right')
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    ncol=4, mode="expand", borderaxespad=0., edgecolor="white",
    prop={'size': legend_fontsize})
    ax.tick_params(labelsize=ticks_fontsize)
    
    if save:
        plt.savefig(path+"fleet_per_day.pdf",  bbox_inches = 'tight', format='pdf')
        
    return grouepd_df