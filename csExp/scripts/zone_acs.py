#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 12:15:42 2018

@author: mc
"""

numberOfCharginStations = 156
def organizeCS(numberOfCharginStations):
    config = {}
    #print("zones\tacs\tacs_plus")
    for zones in range(1,numberOfCharginStations):
        
        if zones not in config.keys(): config[zones]=[]
        
        if numberOfCharginStations % zones == 0:
            acs = int(numberOfCharginStations / zones)
            acs_plus = 0
            if zones not in config.keys(): config[zones]=[]
            config[zones].append( {"acs":acs, "acs_min":acs_plus})
    #        print (str(zones) +"\t"+ str(acs)+"\t"+str(acs_plus))
    
        else:
            acs = int(numberOfCharginStations / zones)
            acs_plus = numberOfCharginStations % zones
            if zones not in config.keys(): config[zones]=[]
            config[zones].append( {"acs":acs, "acs_min":acs_plus} )
    #        print (str(zones) +"\t"+ str(acs)+"\t"+str(acs_plus))
    return config

mydict = organizeCS(numberOfCharginStations)
for zones in mydict.keys():
    listOfCondif= mydict[zones]
    
    if len(listOfCondif) == 0: continue

    for configElement in listOfCondif:
        
#        print("Run sim with")
#        print("Zones:",zones)
#        print("Acs:", configElement['acs'])
#        print("Last change in acs:", configElement['acs_min'])
        if configElement['acs_min'] == 0:
            print('check', zones*configElement['acs'])
        else:
            print('check', (zones)*configElement['acs'] + configElement['acs_min'])
