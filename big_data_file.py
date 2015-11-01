# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

f = open('nyc311calls.csv')

line1 = f.readline()
line1.rstrip
line1_words = line1.split(',')

lat_index = line1_words.index('Latitude')
for n in range(1,len(line1_words)):
    print(line1_words[n])

lat_list=[]
for n in range(1,10000):
    next_line = f.readline()
    next_line_entries = next_line.split(',')   
    
    try:    
        val = float(next_line_entries[lat_index])
    except:
        val = 0
    lat_list.append(val)

plt.hist(lat_list)