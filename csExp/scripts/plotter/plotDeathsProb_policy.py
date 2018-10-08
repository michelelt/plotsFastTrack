#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:03:09 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X: zones percentage, 
    Y: deaths probs
    at varing of the policy
    given city, acs, utt, placement algorithm
'''

def plotDeathsProb_policy(init_df, city, acs, utt, algorithm, save=False, path=""):
    title = "DeathsVsZones_Policy_acs-"+str(acs) +"_algorithm-"+algorithm+".pdf"
    df = init_df[init_df["Acs"] == acs]
    df = df[df["Algorithm"] == algorithm]
    df = df[df["pThreshold"] == 0]
    
    x = df.Zones.unique()
    x = x *100 / float(numeberOfZones(city))
    mylists ={"Needed": [2,4,6,8,12,14,16,18], 
              "Hybrid":[1,3,5,7,9,11,13,15,17,19]}
    
    
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
    ax.set_ylabel(my_labels["Deaths"],fontsize=ax_lab_fontsize)
    ax.set_xlim(0,28)
    
    left, bottom, width, height = [0.40, 0.45, 0.45, 0.35]
    ax2 = fig.add_axes([left, bottom, width, height])
    
    ax2.set_xlim(left=3, right=6)
    ax2.set_ylim(bottom=0.0001, top=5)
    ax2.set_yscale("log")
    ax2.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
    dpVsP_colors = {"Hybrid" :"blue", "Needed":"red", "FreeFloating":"brown"}
    dpVsP_markers = {"Hybrid" :"s", "Needed":"o", "FreeFloating":"^"}
    i = 0
    for policy in ["Needed", "Hybrid",  "FreeFloating"]:

        tmp = df[df["Policy"] ==  policy]
        tmp = tmp[tmp["upperTankThreshold"] == utt]

        if policy in ["Needed", "Hybrid"]:
            tmp = tmp[tmp["TankThreshold"] == 25]
        
        y = tmp["Deaths"]
            
        y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
#        if i==2:
#            return [x,y,tmp]
        print (policy)
        print ("len y", len(y))

        print ()
        if "Free" not in policy:
            ax.plot(x,y, 
                    label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = dpVsP_markers[policy],
                    color = dpVsP_colors[policy],
                    markevery=mylists[policy]
                    )
#                    
        else: 
            ax.plot(x,y, 
                    label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = dpVsP_markers[policy],
                    color = dpVsP_colors[policy],
                    )
            
        ax2.plot(x,y, 
                linestyle=line_dict[policy], 
                marker = dpVsP_markers[policy],
#                color=colors_dict[list(colors_dict.keys())[i]])
                color = dpVsP_colors[policy])
        i = i + 1
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return
