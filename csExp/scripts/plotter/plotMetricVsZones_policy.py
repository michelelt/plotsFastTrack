#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:43:43 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X axis: zones in parentage
    Y axis: metric passed as apramteri
    for each policy
    given city, tt, acs, utt, 
    for only free floating
'''

def plotMetricVsZones_policy(init_df, city, acs, tt,  p,
                             metric, save=False, freeFloating=True, k=250, path=""):
    title = "%s_%s_VsZones_Policy_tt-%d_p-%d.pdf"%(city, metric, tt, p)
    
    df = init_df[init_df["Acs"] == acs]
#    df = df[df["Zones"] >= 4]
    if freeFloating == False:
        df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]
    else :
        df = df[(df["Policy"] == "Needed") | 
                (df["Policy"] == "FreeFloating") |
                (df["Policy"] == "Hybrid")
                ]
    x = df.Zones.unique()
    x = x*100 / float(numeberOfZones(city))

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(my_labels["Zones"],fontsize=ax_lab_fontsize)
    ax.set_ylabel(my_labels[metric],fontsize=ax_lab_fontsize)
    
    print (x)
    
    ax.set_xlim([0,max(x)+1])

    i = 0
    for policy in df.Policy.sort_values(ascending=False).unique():
        if "Free" not in policy:
            tmp = df[(df["TankThreshold"] == tt) & 
                     (df["Policy"] == policy)]

        elif "Hybrid" in policy :
            tmp = df[df["Policy"] == policy]
            tmp = df[df["pThreshold"]==0]
        else: 
            tmp = df[df["Policy"] == policy]
            tmp = df[df["pThreshold"]==1]

        for algorithm in ["max-parking"]:
            tmp2 = tmp[tmp["Algorithm"] == algorithm]
            
            
            if metric == "Deaths" or metric == "AmountRechargeForced":
                y = tmp2[metric]
                y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
                
            elif metric == "TravelWithPenlaty":
                y = tmp2["AvgWalkedDistance"]
                y = y.mul(tmp2["ReroutePerc"])
                y = y + (tmp2["AmountRechargePerc"] -  tmp2["ReroutePerc"])*k
                y = y.div(100)
                
            else:
                y= tmp2[metric]

            if policy == 'FreeFloating': color='brown'
            else : color=colors_dict[list(colors_dict.keys())[i]]
            ax.plot(x,y, label= my_labels[policy], 
            linestyle=line_dict[policy], 
            marker = markers_dict[list(markers_dict.keys())[i]],
            color=color
            )
            i=i+1
    
    if metric == "AvgSOC":
        ax.set_ylim(0,100)
        ax.plot(x,[25 for i in range(len(x))], linestyle ="--", color ="black")

    if metric == "AvgWalkedDistance":
        l = [i for i in range(0,2600,200)]
        ax.set_yticks(l)
    
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(top=ymax)
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    if metric in ["AmountRechargePerc", "AvgSOC", "TravelWithPenlaty"]:
        ax.set_ylim(bottom=0)
        ymin = 0
            
    ax.legend()
    
    plt.show()
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    
    return