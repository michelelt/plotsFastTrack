#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:26:56 2018

@author: mc
"""

import pandas as pd
import pickle
import sys
import json
import subprocess


def LocalSearchParser():
    city = 'Torino'
    columns_conv={
        'TravelWithPenlaty':'New_wwd',
        'Deaths': 'New_Deaths',
        'AvgWalkedDistance': 'New_MeanMeterEnd',
        'AmountRechargePerc':'PercRecharge',
        'ReroutePerc':'PercRerouteEnd'
        
        }

    all_files_in_dir = subprocess.check_output(['ls', '../data'+city]).decode("utf-8").split('\n')
    fnames = []
    for file in all_files_in_dir:
        if 'best_solutions_' in file:
            fnames.append(file)
    dir_path = '../data%s/'%city
    
    df = pd.DataFrame()
    for fname in fnames:
    
        file_pt = open(dir_path+fname, 'r')
        sol = file_pt.read()
        
        sol_unique = ""
        for line in sol:
            if len(line) > 0:
                sol_unique+=line
        
        solutions = sol_unique.split('***')
        #solutions = solutions[0:3]
        
        for i in range(len(solutions)):
            if len(solutions[i])==0:
                continue
            
            element = solutions[i].strip().split('\n')
            
            my_dict = {}
            my_dict['Policy'] = 'Hybrid'
            if '__' in fname: my_dict['Policy'] = 'Forced'
    
            for metric in element:
                metric = metric.split('=')
                if metric[0] == 'CS_placement':
                    metric[1] = metric[1].replace('[', '').replace(']', '').split(',')
                    zid= []
                    for i in range(len(metric[1])):
                        zid.append(int(metric[1][i]))
                    my_dict[metric[0]] = metric[1]
        
        
                elif '{' in metric[0] :
                    metric[0] = metric[0].replace("\'", "\"")
                    performances = json.loads(metric[0])
                    my_dict['AvgWalkedDistance'] = performances['MeanMeterEnd']
                    my_dict['AmountRechargePerc'] = performances['PercRecharge']
                    my_dict['ReroutePerc'] = performances['PercRerouteEnd']
                    my_dict['TravelWithPenlaty'] = performances['WeightedWalkedDistance']

                    
                else:
                    if metric[0]=='New_Deaths': 
                        metric[0] ='Deaths'
                    my_dict[metric[0]] = float(metric[1])
            if 'TravelWithPenlaty' not in my_dict.keys():
                my_dict['TravelWithPenlaty'] = 1e7
            my_dict['fitness'] = 1e7 * my_dict['Deaths'] + my_dict['TravelWithPenlaty']
            my_dict['zones'] = int(fname.split('_')[3])
            df = df.append(pd.Series(my_dict), ignore_index=True)
    return df
            

