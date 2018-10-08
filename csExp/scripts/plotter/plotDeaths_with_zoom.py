#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:28:23 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X: zones percentace
    Y: given metric
    for each policy & pThreshold
    given acs, tt
'''

def plotDeaths_with_zoom(init_df, acs, tt,
                             metric, save=False, 
                             city="", path="", ax=""):
    
    title = 'Torino_H_N_FF_deaths_probs.pdf'
    
    df = init_df[init_df["Acs"] == acs]
    df = df[df['Algorithm'] == 'max-parking']


    x = df.Zones.unique()   
    nz = numeberOfZones(city)
    x = x / float(nz)*100
    x2 =df.Zones.unique() * acs

#    fig = plt.subplots(1,1,figsize=(6,4))
    fig, ax = plt.subplots(1,1,figsize=(9,3))
#    ax = fig.add_axes([0.1, 0.11, 0.7, 0.7])
    ax.grid()
    ax.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
    ax.set_ylabel(my_labels[metric], fontsize=ax_lab_fontsize+5)

    if metric != 'Deaths' : ax.set_xlim([5,31])
    else : ax.set_xlim([0,31])
    

    

    i = 0
    
    for policy in df.Policy.sort_values(ascending=False).unique():
        print (policy)
        if "Hybrid" in policy :
            tmp = df[(df["TankThreshold"] == tt) 
                     & (df["Policy"] == policy) 
                     & (df["pThreshold"] == 0)
                     ]

        elif "Needed" in policy:
            tmp = df[  (df["Policy"] == policy) 
                     & (df['TankThreshold'] == tt) 
                     & (df["pThreshold"] == 0)]
        else :
            tmp = df[(df["Policy"] == policy)]

                
                
        y = tmp[metric]
        y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
    
        if policy == "Needed" : p_legend = ""
        else: p_legend = " p:" +str(100)
        
        ax.plot(x,y, label= my_labels[policy] + p_legend, 
        linestyle=line_dict[policy], 
        marker = markers_dict[list(markers_dict.keys())[i]],
        color=colors_dict[list(colors_dict.keys())[i]]
        )
        if metric == "Deaths" :
#                    continue
            
            left, bottom, width, height = [0.40, 0.40, 0.45, 0.35]
            ax2 = fig.add_axes([left, bottom, width, height])
            
            ax2.set_xlim(3,6)
            if city != 'Berlino':
                ax2.set_ylim(bottom=10e-6, top=10e-2)
            
            ax2.set_ylabel("[%]", fontsize=ax_lab_fontsize)
            ax2.set_yscale("log")
            ax2.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
            ax2.plot(x,y, 
                     linestyle=line_dict[policy], 
                     marker = markers_dict[list(markers_dict.keys())[i]],
                     color=colors_dict[list(colors_dict.keys())[i]]
                     )
#                    ax2.tick_params(labelsize=ticks_fontsize)
            
        i=i+1

    ax.set_ylim(y_lim[metric])


    ymin, ymax = ax.get_ylim()
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    

    
    ax.legend( ncol=5,loc=9, bbox_to_anchor=(0.5,1.45),
                  prop={'size': legend_fontsize-1}, edgecolor="white")
    
    
    if save :   
        plt.savefig(path+title, format='pdf', bbox_inches = 'tight')
    plt.show()
    
    return ax

