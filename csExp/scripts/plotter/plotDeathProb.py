#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:39:12 2018

@author: mc
"""
from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X axis: zones in parentage
    Y axis: Infeasible trips (Deaths)
    for each placing algorithm
    given city, tt, acs
    for only free floating
'''

def plotDeathProb(init_df, city, tt, acs, save=False, onlyFF=True, path=""):
    if onlyFF == True :
        l = ['FreeFloating']
    else:
        l= ['FreeFloating', 'Hybrid', 'Needed']
            
    for policy in l:
        df = init_df[init_df["Policy"] == policy]
        df = df[df["pThreshold"] ==  0]
        df = df[df["upperTankThreshold"] ==  100]
        
        x = df.Zones.unique()
        x = x / numeberOfZones(city)*100

        
        fig, ax = plt.subplots(1,1,figsize=(9,3))
        ax.grid()
        title = city+"_FF_deaths_probs.pdf"
        ax.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
        ax.set_ylabel(my_labels["Deaths"],fontsize=ax_lab_fontsize)
        ax.set_xlim(0,31)
        ax.set_ylim(bottom = -5, top=100)
        
        
        if "Free" not in policy:
            df = df[df["TankThreshold"] == tt]
        
#        for algorithm in ['avg-time', 'max-time', 'max-parking', 'Mean Random']:
        for algorithm in ['avg-time', 'max-parking', 'Mean Random']:

            print (algorithm)
            a = df[df["Algorithm"] == algorithm]
            print (len(a))
            

            a = a[a["Acs"] == acs]
            
            print (len(a))
            y = a.Deaths.div(a.iloc[0]["TypeS"]).mul(100)
            
            if algorithm in ["max-parking"]:

                ax.plot(x,
                        y, 
                        color=colors_dict[algorithm],
                        label=my_labels[algorithm], 
                        marker=markers_dict[algorithm],
                        )
            else :
                ax.plot(x,
                        y, 
                        color=colors_dict[algorithm],
                        label=my_labels[algorithm], 
                        marker=markers_dict[algorithm])
                
                
        ax3 = ax.twiny()
        ax3.set_xlabel("Number of charging stations", fontsize=ax_lab_fontsize)
        myX3ticks = ax.get_xticks()
        myX3ticksB = []
        for i in range(len(myX3ticks)):
            myX3ticksB.append(int(myX3ticks[i].astype(int) / 100 * numeberOfZones(city)))
        myX3ticksB[-1:] = ""
        ax3.set_xticks([0,5,10,15,20,25,30,31])
        ax3.set_xticklabels(myX3ticksB)
        ax3.tick_params(labelsize=ticks_fontsize)
            
            
#        ax.legend(bbox_to_anchor=(0.5,1.45), loc=9,
#           ncol=4, borderaxespad=0., edgecolor="white",
#           handletextpad=0.1, prop={'size': legend_fontsize})
        ax.legend(prop={'size': legend_fontsize})
        
        ax.tick_params(labelsize=ticks_fontsize)
    


    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')

    plt.show()

    return
