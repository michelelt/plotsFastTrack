#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 12:50:47 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *

'''
Description:
    X axis: tank thresholds
    Y axis: metric passed as paramtter
    for each policy
    given city, tt, acs, utt, placing algorithm, Z
    for only free floating
'''

def plotMetricVsTT_policy(init_df, z, acs, algorithm, metric, save=False, path=""):
    
    title = "Torino_"+metric+"_vs_TT.pdf"    
    df = init_df[init_df["Acs"] == acs]
    df = df[df["Zones"] == 15]
    df = df[df["Algorithm"] == algorithm]
    df = df[(df["Policy"] == "Needed") | (df["Policy"] == "Hybrid")]
    df = df[df['pThreshold'] == 0]
    
    x = df.TankThreshold.unique()
    
    xticks = df.TankThreshold
    xticks[len(xticks)] = 0
    xticks = xticks.sort_values().unique()

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.grid()
    ax.set_xlabel(r'$\alpha$' +' [%]', fontsize=ax_lab_fontsize)
    ax.set_ylabel(my_labels[metric], fontsize=ax_lab_fontsize)
    ax.set_xticks(xticks)
    ax.set_xlim(0,55)
    i=0
    for policy in df.Policy.sort_values(ascending=False).unique():
        y=df[df["Policy"] == policy][metric]
        ax.plot(x,y, label= my_labels[policy], 
                    linestyle=line_dict[policy], 
                    marker = markers_dict[list(markers_dict.keys())[i]],
                    color=colors_dict[list(colors_dict.keys())[i]])
        i=i+1
        
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(bottom =0, top=ymax)
    x = x.tolist()
    x.insert(0,0)
    x = np.array(x)
    ax.fill_between(x,0, ymax, where= x<=15, color='red', alpha=0.2, label="Infeasible trips")
        

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    return