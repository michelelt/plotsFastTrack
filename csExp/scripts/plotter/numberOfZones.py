#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:59:31 2018

@author: mc
"""

from plotter.header import *


def numeberOfZones(city):
    c2id={"Vancouver":510, "Torino":261, "Berlino":833, "Milano":549}
    if city in c2id.keys():
        return c2id[city]
    

    command = 'ssh -t d046373@polito.it@tlcdocker1.polito.it wc -l %s_sim3.0/input/car2go_ValidZones.csv' % city
#    command = 'ssh -t d046373@polito.it@tlcdocker1.polito.it cd %s_sim3.0/ | ls '

    zones = int(str(subprocess.check_output(command, shell=True)).split(" ")[0][2:5]) - 1
#    zones = str(subprocess.check_output(command, shell=True)).split("\n")

    return zones
#