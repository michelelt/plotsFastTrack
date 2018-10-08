#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:26:12 2018

@author: mc
"""

from plotter.header import *
from plotter.numberOfZones import *
import subprocess
import pandas as pd





def pdfChargingTimeVsAlgorithm(dataset, save=False, cdf=True):
    
    algorithms = ["avg-time", "max-parking"]
    title = "CDF_parking_time_per_algorithm"+".pdf"
    dataset_d = {}
    city='Torino'
    

    try:
        log0_name = 'car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt'
        dataset_mp = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                       skiprows=[0,1,2,3,4,5,6,7,8,9])
        dataset_d['max-parking'] = dataset_mp
        
        log0_name = 'car2go_Hybrid_avg-time_21_4_25_1000000_100_0.txt'
        dataset_at = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                       skiprows=[0,1,2,3,4,5,6,7,8,9])
        dataset_d['avg-time'] = dataset_at
    except:
        bashCommand = "ssh cocca@bigdatadb "+\
              "hdfs dfs -cat "+\
              "Simulator/output/Simulation_"+ str(6) +"/"+\
              'car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        strOutput =  output.decode("utf-8") 
        fp1 = open('../../dataTorino/car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt', 'w')
        fp1.write(strOutput) 
        f.close()
        
        
        bashCommand = "ssh cocca@bigdatadb "+\
                      "hdfs dfs -cat "+\
                      "Simulator/output/Simulation_"+ str(6) +"/"+\
                      'car2go_Hybrid_avg-time_21_4_25_1000000_100_0.txt'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        strOutput =  output.decode("utf-8") 
        fp1 = open('../../dataTorino/car2go_Hybrid_avg-time_21_4_25_1000000_100_0.txt', 'w')
        fp1.write(strOutput) 
        
        log0_name = 'car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt'
        dataset_mp = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                       skiprows=[0,1,2,3,4,5,6,7,8,9])
        dataset_d['max-parking'] = dataset_mp
        
        log0_name = 'car2go_Hybrid_avg-time_21_4_25_1000000_100_0.txt'
        dataset_at = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                       skiprows=[0,1,2,3,4,5,6,7,8,9])
        dataset_d['avg-time'] = dataset_at
    
    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.set_xlabel("Plugged time [h]", fontsize=ax_lab_fontsize)
    ax.set_ylabel("CDF", fontsize=ax_lab_fontsize)
    ax.set_ylim([0,1])
    ax.set_xlim([0,30])
    mymarker = {"avg-time":"*", 
                "max-parking":"o"}
    mylists ={"avg-time": [i * 1480 for i in range(1,6)], 
              "max-parking":[i * 9520 for i in range(1,6)]}
    
    ax.grid()
    
    for a in algorithms :
        dataset = dataset_d[a]
        test = dataset[dataset["StartRecharge"] > 0]
        test["parkingTime"] = test["Stamp"] - test["StartRecharge"]

        
        values = test["parkingTime"].div (3600)
#        values = test["Recharge"]
        values = values[values < values.quantile(0.99)]
        values.tolist()
        print (len(values),a)
        sorted_data = np.sort(values)    
        yvals=np.arange(len(values))/float(len(values)-1)
        ax.plot(sorted_data,yvals,
                label=my_labels[a], 
                color=colors_dict[a], 
                linewidth=2, 
#                markevery=mylists[a],
                marker=mymarker[a])
        print("aaa")
        
        print ("sorted data", len(sorted_data))
        print ("sorted data", len(yvals))

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0., edgecolor="white")
    
    if save :   
        plt.savefig(path+title, bbox_inches = 'tight', format='pdf')
    plt.show()
    return