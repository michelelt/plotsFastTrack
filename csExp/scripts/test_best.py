#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def validSimulation(BestEffort, tankThreshold_valid, pThresholdCheck) :

   '''
   :param BestEffort: True -> car goes to park if ends trip in a CS
   :param tankThreshold_valid: percentage of battery below with a car can recharge
   :param pThresholdCheck: 0-> people charge only needed, 1 -> charge every time
   :return:
   '''

  #Station Based and IMP2
   if tankThreshold_valid == 100:
       return False

   #IMP1
   if BestEffort==False and\
       tankThreshold_valid==-1 :
       return False

   #Needed only p=0
   if BestEffort == False \
       and tankThreshold_valid >= 0 \
       and tankThreshold_valid < 100 \
       and pThresholdCheck != 0 :
       #print(BestEffort, tankThreshold, p)
       return False

   ##free Floating only and p=100
   if BestEffort == True \
       and tankThreshold_valid == -1 \
       and pThresholdCheck != 100 :
       #print(BestEffort, tankThreshold, p)
       return False
   
   ## Hybrid dont have p==0
   if BestEffort == True \
	 and tankThreshold_valid >0 \
     and pThresholdCheck == 0:
      return False

   return True




be =False
tt = 25
pt = 0.2

bes = [True,False]
pts = [0, .25]

for be in bes:
    for pt in pts:
        if(be == True):
            policy="Hybrid"
        else:
            policy="Needed"
        
        print(be, pt)
        print (policy)
        print(validSimulation(BestEffort=be, 
                              tankThreshold_valid=tt,
                              pThresholdCheck=pt))
        print()













