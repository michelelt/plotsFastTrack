#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 16:51:52 2018

@author: mc
"""

from BestSolParser import BestSolParser
from loadingData import uploadFromSSDallStuff

df1 = BestSolParser()

cdfList_bdst, cdfList_bdur, cdfList_pdur,\
dict_df2, log_df, mytt = uploadFromSSDallStuff({"Torino":46}, {})


