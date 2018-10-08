# -*- coding: utf-8 -*-

import numpy as np
import pickle
import sys
import os
#p = os.path.abspath('..')
#sys.path.append(p+"/")

import time
import datetime
import pandas as pd

import matplotlib.pyplot as plt
import pymongo
import matplotlib
import subprocess

import pprint as pp

import math
from matplotlib.patches import Patch
from matplotlib.lines import Line2D 
pp = pp.PrettyPrinter()

ticks_fontsize = 15
legend_fontsize = 15
ax_lab_fontsize = 18

colors_dict = {"max-parking" :"red", "rnd":"blue", "max-time":"black", 
               "avg-time":"purple", "Mean Random" :"Green", "Min Random" :"Brown"}

line_dict = {"FreeFloating":"-.", "Needed":":", "Hybrid":"--"}

markers_dict = {"max-parking" :"o", "rnd":"s", "max-time":"^", "avg-time":"*", 
                "Mean Random" :"d", "Min Random" :""}

metrics_dict = {"ReroutePerc":"Reroute [%]", "Deaths":"Battery run out [%]", 
                "AvgWalkedDistance":"Average walked distance [m]"}

markers_dict_policy = {"FreeFloating":"s", "Needed":"o", "Hybrid":"d"}

colors_dict_policy = {"FreeFloating":"brown", "Needed":"red"}

colors_dict_city ={ 
               "Torino": "blue",
               "Milano" : "red",
               "Berlino" : "orange",
               "Vancouver": "green"
        }
city_eng_names = { "Vancouver": "Vancouver",
               "Berlino" : "Berlin",
               "Milano" : "Milan",
               "Torino": "Turin"
        }

my_labels = {"Needed":"Will. p:0",
          "Hybrid":"Will.",
          "FreeFloating":"Free Floating",
          "Deaths":"Infeasible trips [%]",
          "Zones": "Zones [%]",
          "AvgWalkedDistance": "Avg walk dist. [km]",
          "TripDistance":"Distance",
          "duration":"Duration",
          "AvgSOC": "Average State of Charge [%]",
          "ReroutePerc":"Rerouting [%]",
          "AmountRechargePerc" : "Recharges [%]",
          "AmountRechargeForced":"Recharges",
          "max-parking":"Num parking",
          "avg-time":"Avg time",
          "max-time":"Tot time",
          "Min Random" : "Min Random",
          "Mean Random" : "Mean Random",
          "TravelWithPenlaty":"Weighted walked distance [m]",
          "mean-rnd":"Mean rnd", 
          "min-rnd":"Best rnd",
          "AvgStationOccupancy": "Average Station Occupancy",
          "AvgTimeInStation": 'Avg plug time [h]'
        }


y_lim = {
          "Deaths": (-5,80),
          "AvgStationOccupancy": (0,1),
          "AmountRechargePerc" : (0,80),
          "AvgSOC": (0,100),
          "ReroutePerc": (-5,60),
          "AvgWalkedDistance": (0,3),
          "TravelWithPenlaty":(0,1500),
        }

zoom_deaths = { "Vancouver": (7,11),
               "Milano" : (6,10),
               "Berlino" : (25, 31),
               "Torino": (4.5, 7.5)
        }

red_box = { "Vancouver": 8,
               "Milano" : 8,
               "Berlino" : 8,
               "Torino": 6
        }

