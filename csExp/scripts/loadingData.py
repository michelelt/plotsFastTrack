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
from LocalSearchParser import LocalSearchParser
from GeneticParser import GeneticParser
from plotter.header import *
import numpy as np

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
from plotter.numberOfZones import numeberOfZones

from DownloadFiles import *
import subprocess
from DownloadFiles import Downloader

#from hdfs import InsecureClient


def computeTravelWithPenlaty(df):
    k=150
    y = df["AvgWalkedDistance"]
    y = y.mul(df["ReroutePerc"])
    y = y + (df["AmountRechargePerc"] -  df["ReroutePerc"])*k
    y = y.div(100)
    return y
        
        
def downloadAllStuff(c2id,rnd2id, fileroot_name) :
    
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

        dld.changeDstHome(city)
        lastS, outFileName =dld.dowloadOutAnalysis(c2id[city])
        dld.downloadOptLogs(city, 'genetico_best')

#        dld.downloadOptLogs(city, 'best_solution')

        df = pd.read_csv(path+outFileName, sep=" ")
        dict_df[city] = df
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

        
        df = pd.read_csv(path+outFileName, sep=" ")
        df = df[
                ((df.Policy == 'Hybrid') & (df.pThreshold == 100)) |
                ((df.Policy == 'Needed') & (df.pThreshold == 0))
                ]
        df["TravelWithPenlaty"] = computeTravelWithPenlaty(df)
        
        dict_df[city] = df
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
c2id = {"Vancouver":8, "Berlino":7,"Milano":9, "Torino":6}
rnd2id = {"Torino":[11,12,13,14,15],
          "Vancouver":[17,18,19,20,21], 
          "Berlino":[22,23,24,25,26], 
          "Milano":[27,28,29,30,31]
          }
rnd2id = {}


c2id = {"Torino":47}


#cdfList_bdst, cdfList_bdur, cdfList_pdur, dict_df, log_df,\
#plt_home, path, mytt =  downloadAllStuff(c2id, rnd2id, '')


'''UPLOAD data da SSD'''
cdfList_bdst, cdfList_bdur, cdfList_pdur,\
dict_df2, log_df, mytt = uploadFromSSDallStuff(c2id, rnd2id)

'''parsing dei file di opt'''
df_localSearch = LocalSearchParser()

df_genetic = GeneticParser()
df_genetic =  df_genetic[df_genetic.zones <= 30]



'''aggiungere altre metriche se serve'''
metrics=[
        ('Deaths',[0,0]),
        ('TravelWithPenlaty',[0,1]),
        ('AvgWalkedDistance',[0,2]),
        ('AmountRechargePerc',[1,0]),
        ('ReroutePerc',[1,1]),
]


df_std = dict_df2['Torino']

'''
Grouping per zones, selecting for each column the minimum vaule
'''
best_fit_genetic = df_genetic\
            .dropna()\
            .groupby(['zones','Policy'])\
            .idxmin()\
            .reset_index()
          
best_fit_ls = df_localSearch\
            .dropna()\
            .groupby(['zones','Policy'])\
            .idxmin()\
            .reset_index()


df_ls_forced = best_fit_ls[best_fit_ls.Policy == 'Forced']
best_ls_f = df_localSearch.loc[df_ls_forced.fitness]

df_ls_forced = best_fit_ls[best_fit_ls.Policy == 'Hybrid']
best_ls_h = df_localSearch.loc[df_ls_forced.fitness]

''' '''
df_g_forced = best_fit_genetic[best_fit_genetic.Policy == 'Forced']
best_gn_f = df_genetic.loc[df_g_forced.fitness]

df_g_hybrid = best_fit_genetic[best_fit_genetic.Policy == 'Hybrid']
best_gn_h = df_genetic.loc[df_g_hybrid.fitness]

Policies = [
        ('Hybrid', best_gn_h, best_ls_h),
        ('Needed', best_gn_f, best_ls_f)
        ]

for pol in Policies:
    policy = pol [0]
    best_gn = pol[1]
    best_ls = pol[2]
    
    fig, ax = plt.subplots(2,3, figsize=(30,20))
    for comb in metrics:
        metric = comb[0]
        r = comb[1][0]
        c = comb[1][1]
        
        mul_fact = 1
        if metric == 'Deaths':
            mul_fact = 100/df_std.iloc[0]['TypeS']
            df_std['Deahts'] = df_std['Deaths'].mul(mul_fact) 

         
        '''
        Chose the column having the as index, the same index and the same zone
        of the row having the minumum fitness vaue
        '''    
        
        l1 = ax[r,c].plot(df_std.Zones.unique(),
            df_std[df_std.Policy ==policy][metric].mul(mul_fact),
            label='Heuristic %s'%policy)

        l2 = ax[r,c].plot(best_ls.zones,
            best_ls[metric],
            label='LS %s'%policy )
     
        l3 = ax[r,c].plot(best_gn.zones,
            best_gn[metric],
            label='Genetic %s'%policy)

        ax[r,c].legend()
        ax[r,c].grid()
        ax[r,c].set_xlabel(my_labels['Zones'])
        ax[r,c].set_ylabel(my_labels[metric])
        ax[r,c].set_xticks([6,10,15,20,25,30])
        ax[r,c].set_xticklabels([2.3,3.8,5.7,7.7,9.6,11.5])
        ax[r,c].set_xticklabels(round(best_gn.zones * 100 / 261,1))
        ax[r,c].set_xlim(6,30)
        if metric == 'Deaths':
            ax[r,c].set_yscale('log')
        else:
            ymin, ymax = ax[r,c].get_ylim()
            x = best_gn.zones.unique()
            ax[r,c].fill_between(x,ymin,ymax, where= x<12 ,
                        color='red', alpha=0.2, label="Infeasible trips")
            ax[r,c].set_ylim(ymin, ymax)
            
        '''
        Data dumps
        '''
        df_std[df_std.Policy ==policy].to_csv('../xy/not_opt_%s.csv'%policy,
                                             index_label='id')
        best_ls.to_csv('../xy/ls_%s'%policy, index_label='id')
        best_gn.to_csv('../xy/gn_%s'%policy, index_label='id')
    
    
    plt.savefig('../plots/global_%s.pdf'%(policy))
#
    








    

    
    
    
    
    
    
    
    
    




