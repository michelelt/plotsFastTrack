#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:59:31 2018

@author: mc
"""


from plotter.header import *
from plotter.numberOfZones import *
    
def metricVsZones_kwhSupplied(df, city, algorithm, policy, metric, p=50, save=False, path='./'):
    x = df.Zones.unique()
    x = x / numeberOfZones(city)*100
    
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    styleCounter = 0
    
    mulfactor =1
    if metric == 'Deaths' : mulfactor = 100/df.iloc[0]['TypeE']
    if metric == 'AvgStationOccupancy' : mulfactor = 100
    
    for kwh_supp in [2,20, 100]:
        kwh = df
        kwh = kwh[
                (kwh["Algorithm"] == algorithm)
               &(kwh["Policy"] == policy)
               &(kwh["kwh"] == kwh_supp )
                ]
        
        if policy == 'Hybrid' :
            kwh = kwh[kwh['pThreshold'] == p]
        ax.plot(x, kwh[metric].mul(mulfactor), 
                label=str(kwh_supp) + 'kWh',
                marker = markers_dict[list(markers_dict.keys())[styleCounter]],
                color =  colors_dict[list(colors_dict.keys())[styleCounter]]
                )
        styleCounter += 1
        ax.set_xlabel(my_labels['Zones'], fontsize=label_fontsize)
        ax.set_ylabel(my_labels[metric], fontsize=label_fontsize)
        ax.set_title(policy)
        ax.grid()
        ax.legend()
        
    if save:
        plt.savefig(path+"kwhSupplied_" + city+\
                    "_" + algorithm +\
                    "_" + policy +\
                    "_" + metric +\
                    ".pdf", bbox_inches = 'tight', format='pdf')
    return