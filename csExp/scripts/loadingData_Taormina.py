# -*- coding: utf-8 -*-
import numpy as np
import pickle
import sys
import os

p = os.path.abspath('..')
sys.path.append(p+"/")

import time
import datetime
import pandas as pd

import matplotlib.pyplot as plt
from plotter.header import *

from plotter.aggregateFleetPerDay import *         
from plotter.pdfChargingTimeVsAlgorithm import * 
from plotter.aggregatePerCityCDF import *           
from plotter.plotCDF import * 
from plotter.aggregateUtilizationPerHour import * 
from plotter.plotDeathProb import * 
from plotter.checkStartEndsAlternates import * 
from plotter.plotDeathsProb_policy import * 
from plotter.computeCDF import * 
from plotter.plotMetricVsTT_policy import * 
from plotter.aggregateMetricVsZones_city import * 
from plotter.maxTripCoordinates import * 
from plotter.plotMetricVsZones_policy import * 
from plotter.metricVaryingZonesAndACs_city import * 
from plotter.plotMetricVsZones_policy_p import *
from plotter.aggregateBookingsPerDay import *
from plotter.plotDeaths_with_zoom import *

from DownloadFiles import *
import subprocess
from DownloadFiles import Downloader

#from hdfs import InsecureClient


'''
rnd dld
'''

def computeTravelWithPenlaty(df):
    k=150
    y = df["AvgWalkedDistance"]
    y = y.mul(df["ReroutePerc"])
    y = y + (df["AmountRechargePerc"] -  df["ReroutePerc"])*k
    y = y.div(100)
    return y
        
        
def downloadAllStuff(c2id,rnd2id) :
    
    dict_df={}
    log_df = {}
    dld = Downloader("Berlino")
    cdfList_bdst = {}
    cdfList_bdur = {}
    cdfList_pdur = {}
    
    for city in c2id.keys():
        print (city)
       
        dld.changeDstHome(city)
        path = dld.dst_home
        plt_home = dld.plt_home
        mytt = 25
        
#        if city == "Berlino":
#            mytt=50

        dld.changeDstHome(city)
        lastS, outFileName =dld.dowloadOutAnalysis(c2id[city])

#        if c2id[city] <41: 
#            lastS, outFileName =dld.dowloadOutAnalysis(c2id[city])
#        else : 
#            lastS = c2id[city]
#            outFileName = "out_analysis_%s_cr.txt"%lastS

        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
#       
        if city in rnd2id.keys():
            rndDf = pd.DataFrame()
            for lastS_rnd in rnd2id[city]:
                lastS_rnd, outFileName_rnd =dld.dowloadOutAnalysis(lastS_rnd)
                tmp_rnd = pd.read_csv(path+outFileName_rnd, sep=" ")
                tmp_rnd["TravelWithPenlaty"] = computeTravelWithPenlaty(tmp_rnd)
                rndDf = tmp_rnd.append(tmp_rnd)
                
            df_rnd = rndDf
            df_rnd = df_rnd[df_rnd["Policy"] == 'FreeFloating' ]
            
            
            dfMean = df_rnd.groupby("Zones").mean()
            dfMean["Provider"] = "car2go"
            dfMean["Policy"] = "FreeFloating"
            dfMean["Algorithm"] = "Mean Random"
            dfMean = dfMean.reset_index()
            dfMean = dfMean[dfMean.Zones.isin(dict_df[city].Zones)]
        
        print ("LS", lastS)
        ## FIX - ME dld here function



#        print (log0_name)
#        log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
#                                       skiprows=[0,1,2,3,4,5,6,7,8,9])
#        

    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, plt_home, path, mytt

def uploadFromSSDallStuff(c2id, rnd2id):
    dict_df={}
    log_df = {}
    cdfList_bdst = {}
    cdfList_bdur = {}
    cdfList_pdur = {}
    
    log0_name_dict={
            'Torino':    'car2go_Hybrid_max-parking_21_4_25_1000000_100_0.txt',
            'Berlino':   'car2go_Hybrid_max-parking_20_4_25_1000000_100_0.txt',
            'Milano':    'car2go_Hybrid_max-parking_20_4_25_1000000_100_0.txt',
            'Vancouver': 'car2go_Hybrid_max-parking_22_4_25_1000000_100_0.txt'
            }
    
    for city in c2id.keys():
        print (city)
        lastS = c2id[city]
        path='../data%s/'%city
        outFileName = "out_analysis_%s_cr.txt"%lastS

        dict_df[city] = pd.read_csv(path+outFileName, sep=" ")
        dict_df[city]["TravelWithPenlaty"] = computeTravelWithPenlaty(dict_df[city])
#       
        if city in rnd2id.keys():
            rndDf = pd.DataFrame()
            for lastS_rnd in rnd2id[city]:
                print('mount_rnd')
                outFileName_rnd = "out_analysis_%s_cr.txt"%lastS_rnd
                tmp_rnd = pd.read_csv(path+outFileName_rnd, sep=" ")
                tmp_rnd["TravelWithPenlaty"] = computeTravelWithPenlaty(tmp_rnd)
                rndDf = tmp_rnd.append(tmp_rnd)
                
            df_rnd = rndDf
            df_rnd = df_rnd[df_rnd["Policy"] == 'FreeFloating' ]
            
            
            dfMean = df_rnd.groupby("Zones").mean()
            dfMean["Provider"] = "car2go"
            dfMean["Policy"] = "FreeFloating"
            dfMean["Algorithm"] = "Mean Random"
            dfMean = dfMean.reset_index()
            dfMean = dfMean[dfMean.Zones.isin(dict_df[city].Zones)]
            
            dict_df[city] = dict_df[city].append([dfMean], ignore_index=True)

            
        log0_name = log0_name_dict[city]
        
        log_df[city] = pd.read_csv("../data"+city+"/"+log0_name, sep=";", 
                                   skiprows=[0,1,2,3,4,5,6,7,8,9])
            
    mytt=25
            
    return cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df, mytt


#
c2id = {"Torino":6}
rnd2id = {"Torino":[11,12,13,14,15]}

metrics = ["AmountRechargePerc", "AvgSOC", 
           "ReroutePerc", "TravelWithPenlaty", 
          "AvgWalkedDistance"]


#
#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id)

cdfList_bdst, cdfList_bdur, cdfList_pdur,\
dict_df, log_df, mytt = uploadFromSSDallStuff(c2id, rnd2id)


for city in ['Torino']:
    
#    cdfList_bdst[city] = computeCDF(log_df[city], "RentalsDistance", city) 
#    cdfList_pdur[city] = computeCDF(log_df[city], "ParkingsDuration", city)
    
#    plotCDF(cdfList_bdst[city], 'RentalsDistance', save=True, city=city, path="../plots/" )
#    plotCDF(cdfList_pdur[city], 'ParkingsDuration', save=True, city=city, path="../plots/" )

##    
#    plotDeathProb(dict_df[city], city=city, tt=25, acs=4, save=True, onlyFF=True,
#                  path="../plots/")

    
#    pdfChargingTimeVsAlgorithm(log_df[city], save=False, cdf=True)



#    plotDeaths_with_zoom(init_df=dict_df[city], acs=4, tt=25,
#                                        metric='Deaths', city=city, save=True,
#                                        path="../plots/", ax="")
    
#    for m in metrics:
#        zzz=plotMetricVsZones_policy_p(init_df=dict_df[city], acs=4, tt=25,
#                                        plist=[0],metric=m, city=city, save=True,
#                                        freeFloating=True, path="../plots/", ax="")
        
    plotMetricVsTT_policy(init_df= dict_df[city], 
                   z=21,
                   acs=4, 
                   algorithm='max-parking', 
                   metric='ReroutePerc', 
                   save=True, 
                   path="../plots/")








        
        


    

    
    
    
    
    
    
    
    
    




