#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 10:14:49 2018

@author: mc
"""
import pandas as pd
import subprocess


def GeneticParser():
    city = 'Torino'
    all_files_in_dir = subprocess.check_output(['ls', '../data'+city]).decode("utf-8").split('\n')
    fnames = []
    files_log = []
    pure_elitists = []
    zones = []
    policies=[]
    for file in all_files_in_dir:
        if 'genetico_best' in file:
            fnames.append(file)
            file = file.split('_')
            if 'FORCED' in file: 
                policies.append("Forced")
                pure_elitists.append(file[3])
                zones.append(file[4])
            else:
                policies.append("Hybrid")
                pure_elitists.append(file[2])
                zones.append(file[3])
        elif 'genetico_log' in file:
            files_log.append(file)
            file = file.split('_')
            if 'FORCED' in file: 
                policies.append("Forced")
                pure_elitists.append(file[3])
                zones.append(file[4])
            else:
                policies.append("Hybrid")
                pure_elitists.append(file[2])
                zones.append(file[3])
        else:
            continue
            
    dir_path = '../data%s/'%city
    
    
    conf_dict = {}
    
    for fname, pe, zone, policy in zip(files_log, pure_elitists, zones, policies):
        
        file_pt = open(dir_path+fname, 'r')
        sol = file_pt.read().strip().replace('[', '').replace(']', '').split('\n')
        

                 
        i=0# prima risultati (0) e poi configurazione (1)         
        for config in sol:
            if "Generazione:" not in config and "solution" not in config: #sono righe di risultati
                
                config = config.replace(',', '').split(' ')
                if i==0: #riga di risultati
                    PercDeath = float(config[0])
                    WeightedWalkedDistance = float(config[1])
                    MeanMeterEnd = float(config[2])
                    PercRerouteEnd = float(config[3])
                    PercRecharge =  float(config[4])
                                        
                    i+=1
                else:  #i=1 riga di configurazioni
                    
                    configuration=[]
                    for i in range(0, len(config)):
                        configuration.append(int(config[i]))
                    conf_dict[policy+str(zone)+" "+str(pe)+" "+str(configuration)]=[PercDeath,WeightedWalkedDistance,MeanMeterEnd,PercRerouteEnd,PercRecharge]    
                    #print(str(zone)+" "+str(pe)+" "+str(configuration))
                    i=0
                    
                    
    df = pd.DataFrame()
    
    for fname, pe, zone, policy in zip(fnames, pure_elitists, zones, policies):
        file_pt = open(dir_path+fname, 'r')
        sol = file_pt.read().strip()
        sol = sol.strip().replace('[', '').replace(']', '').split('\n')
        

        
        my_dict = {}
        #my_dict['Deaths'] = []
        #my_dict['TravelWithPenlaty'] = []
        #my_dict['AvgWalkedDistance'] = []
        #my_dict['AmountRechargePerc'] = []
        #my_dict['ReroutePerc'] = []
        #my_dict['CS_placement'] = []
        my_dict['zones']=int(zone)
        my_dict['pure_elitist']    = int(pe)   
        my_dict["generation"]=0
        my_dict['Policy'] = policy
              
        for config in sol:
            #my_dict = {}
            config = config.split(',')
            my_dict['Deaths']=( float(config[0]))
            my_dict['TravelWithPenlaty']=(float(config[1]))
            my_dict['CS_placement']=([])
            for i in range(2, len(config)):
                my_dict['CS_placement'].append(int(config[i]))
            
            #look up in config_dict for the remaining values
            
            my_dict['AvgWalkedDistance']=conf_dict[policy+str(zone)+" "+str(pe)+" "+str(my_dict['CS_placement'])][2]
            my_dict['ReroutePerc']=conf_dict[policy+str(zone)+" "+str(pe)+" "+str(my_dict['CS_placement'])][3]
            my_dict['AmountRechargePerc']=conf_dict[policy+str(zone)+" "+str(pe)+" "+str(my_dict['CS_placement'])][4]
            my_dict["generation"]+=1
            my_dict["fitness"]=1e7*my_dict['Deaths']+my_dict['TravelWithPenlaty']
            #print("Trovato", conf_dict[str(zone)+" "+str(pe)+" "+str(my_dict['CS_placement'][-1])][4])
        
    
            df = df.append(pd.Series(my_dict), ignore_index=True)

        
        #df = df.append(pd.Series(my_dict), ignore_index=True)

    return df

