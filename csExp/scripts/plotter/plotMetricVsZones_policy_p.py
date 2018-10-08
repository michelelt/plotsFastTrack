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

def plotMetricVsZones_policy_p(init_df, acs, tt, plist,
                             metric, save=False, freeFloating=True, 
                             k=250, city="", path="", ax=""):
    
    title = city+ "_H_NN" + metric + ".pdf"
    print (title)
    
    df = init_df[init_df["Acs"] == acs]
#    df = df[df["Zones"] >= 4]
    df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]

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

            
    if metric != 'Deaths' : ax.set_xlim([0,31])
    else : ax.set_xlim([0,31])

    i = 0
    df = df[(df["TankThreshold"] == tt)]
    
    for policy in df.Policy.sort_values(ascending=False).unique():
        print (policy)
        for p in plist :
            if "Hybrid" in policy :
                tmp = df[(df["TankThreshold"] == tt) 
                         & (df["Policy"] == policy) 
                         & (df["pThreshold"] == 0)
                         ]

            elif "Needed" in policy and p == 0 :
                tmp = df[(df["Policy"] == policy) 
                         & (df["pThreshold"] == 0)
                            ]
            else :
                continue
    
            for algorithm in ["max-parking"]:
                tmp2 = tmp[tmp["Algorithm"] == algorithm]
                
                
                if metric == "Deaths" or metric == "AmountRechargeForced":
                    y = tmp2[metric]
                    y = y.div(init_df.iloc[0]["TypeE"]).mul(100)
                    
                elif metric == "TravelWithPenlaty":
                    y = tmp2["AvgWalkedDistance"]
                    y = y.mul(tmp2["ReroutePerc"])
                    y = y + (tmp2["AmountRechargePerc"] -  tmp2["ReroutePerc"])*k
#                    y = y.div(tmp2.iloc[0]["TypeE"])
                    y = y.div(100)
                    
                elif metric == "AvgWalkedDistance":
                    y = tmp2["AvgWalkedDistance"]
                    y = y.div(1000)
                    
                else:
                    y= tmp2[metric]
    
                print (policy, p, len(y))
                if policy == "Needed" : p_legend = ""
                else: p_legend = " p:" +str(p)
                
                ax.plot(x,y, label= my_labels[policy] + p_legend, 
                linestyle=line_dict[policy], 
                marker = markers_dict[list(markers_dict.keys())[i]],
                color=colors_dict[list(colors_dict.keys())[i]]
                )
                if metric == "Deaths" :
#                    continue
                    
                    left, bottom, width, height = [0.30, 0.40, 0.45, 0.35]
                    ax2 = fig.add_axes([left, bottom, width, height])
                    
                    ax2.set_xlim(3,6)
                    if city != 'Berlino':
                        ax2.set_ylim(bottom=10e-6, top=10e-2)
                    
                    ax2.set_ylabel("[%]", fontsize=ax_lab_fontsize)
                    ax2.set_yscale("log")
                    ax2.set_xlabel(my_labels["Zones"], fontsize=ax_lab_fontsize)
                    ax2.plot(x,y, label= my_labels[policy] + " p:" +str(p), 
                    linestyle=line_dict[policy], 
                    marker = markers_dict[list(markers_dict.keys())[i]],
                    color=colors_dict[list(colors_dict.keys())[i]])
#                    ax2.tick_params(labelsize=ticks_fontsize)
                    
                i=i+1

    ax.set_ylim(y_lim[metric])

    if metric == 'TravelWithPenlaty' and city == 'Vancouver': 
        ax.set_ylim([0,800])
        ax.set_yticklabels([0,0.2, 0.4, 0.6, 0.8])
        ax.set_ylabel('Weighted walked distance[km]')
    ax.tick_params(labelsize=ticks_fontsize + 5)

    ymin, ymax = ax.get_ylim()
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    if metric != 'Deaths':
        ax.fill_between(x,ymin, ymax, where= x<=red_box[city], 
                    color='red', alpha=0.2, label="Infeasible trips")
    
    ax.legend(bbox_to_anchor=(1, 1), loc=2, ncol=1, 
              mode="expand", borderaxespad=0., edgecolor="white")
    
    
    if metric == 'AmountRechargePerc' or metric == 'Deaths':
        ax.legend( ncol=5,loc=9, bbox_to_anchor=(0.5,1.45),
                  prop={'size': legend_fontsize-1}, edgecolor="white")
    
#    ax3 = ax.twiny()
#    ax3.set_xlabel("Number of charging stations", fontsize=ax_lab_fontsize)
#    myX3ticks = ax.get_xticks()
#    myX3ticksB = []
#    if metric != 'Deaths' : 
#        ax3.set_xlim([5,31])
#        ax.set_xticks([5,10,15,20,25,30])
#    else : ax3.set_xlim([0,31])
#    
#    for i in range(len(myX3ticks)):
#        myX3ticksB.append(int(myX3ticks[i] / 100 * nz ))
##    myX3ticksB[-1:] = ""
#
#    ax3.set_xticklabels(myX3ticksB)
#    ax3.tick_params(labelsize=ticks_fontsize)


    
    if save :   
        plt.savefig(path+title, format='pdf', bbox_inches = 'tight')
    plt.show()
    
    return ax

