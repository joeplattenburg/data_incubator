# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime as dt
import time

f = open('nyc311calls.csv')

line1 = f.readline()
line1.rstrip
line1_words = line1.split(',')

lat_index = line1_words.index('Latitude')
long_index = line1_words.index('Longitude')
agency_index = line1_words.index('Agency')
agency_name_index = line1_words.index('Agency Name')
time_index = line1_words.index('Created Date')

for n in range(1,len(line1_words)):
    print(line1_words[n])


#%%

lat_list = []
long_list = []
name_list = []
time_list = []


#for kk in range(1,20):  # Use this to test a small set
for line in f:  # Use this to run on the whole dataset
    line = f.readline()
    next_line_entries = line.split(',')   
    # It seems like some of the entries are bad, replace these with zeros
    try:    
        val1 = float(next_line_entries[lat_index])
    except:
        val1 = 0
        
    try:    
        val2 = float(next_line_entries[long_index])
    except:
        val2 = 0
        
    try:    
        val3 = str(next_line_entries[agency_name_index])
    except:
        val3 = ''
        
    try:    
        val4 = str(next_line_entries[time_index])
    except:
        val4 = ''
        
    lat_list.append(val1)
    long_list.append(val2)
    name_list.append(val3)
    time_list.append(val4)

# Throw out the bad entries
lat_list[:] = (value for value in lat_list if value != 0)
long_list[:] = (value for value in long_list if value != 0)
name_list[:] = (value for value in name_list if value != '')
time_list[:] = (value for value in time_list if value != '')


#%% Count how many complaints per agency

counts = dict()

num_complaints = len(name_list)
for word in name_list:
    counts[word] = counts.get(word,0) + 1
#print("Counts: ", counts)

most_common = 0
second_most_common = 0
com_word= None
sec_com_word = None
for key,value in counts.items():
    if (value > most_common):
        most_common = value
        com_word = key
        second_most_common = most_common
        sec_com_word = com_word
        
print(sec_com_word, second_most_common)
perc_sec_most_com = float(second_most_common)/float(num_complaints)
print('Fraction of complaints associated with 2nd most popular agency is', perc_sec_most_com)

#%% 10 and 90 percentiles of latitude

#plt.hist(lat_list)
# Get the range between the 90% and 10% percentiles
lat_list.sort()
num_entries = len(lat_list)
deciles = [math.floor(.1*num_entries), math.floor(.9*num_entries)]
deg_dist = lat_list[deciles[1]] - lat_list[deciles[0]] 
print('Distance between 90% and 10% percentiles is', deg_dist)

#%% Area of ellipse

# The one-standard-deviation ellipse the the bivariate normal distribution has 
# A = pi*a*b where a and b are the ellipse axes. Assuming zero covariance between
# longitude and latitude (i.e. elliple axes are aligned with north-south and 
# east-west), then area A = pi * std(long)/2 * std(lat)/2

# One degree of latitude is approximately 111 km
axis1 = 111*np.std(lat_list)/2
# One degree of longitude's distance varies north to south, but just approximate
# at the mean of the latitudes
mean_lat = np.mean(lat_list)
radius_of_earth = 6371 #km
km_in_deg_long = (math.pi/180)*radius_of_earth*math.cos(mean_lat*math.pi/180)
axis2 = km_in_deg_long*np.std(long_list)/2

# I know this isnt quite right because both the number of km per degree lat and
# long both vary with long and lat, integral is probably required but I am running 
# out of time

area_of_ellipse = math.pi*(axis2)*(axis2)
print('Area of 1 std ellipse is', area_of_ellipse, 'km')

#%% Get time between calls


secs_since_epoch=[]
for entry in time_list:
    just_date = entry[0:10]
    three_nums_date = just_date.split('/')
    year = int(three_nums_date[2])
    mon = int(three_nums_date[1])
    if mon > 12 or mon < 1:
        continue
    day = int(three_nums_date[0])
    if day > 31 or day < 1:
        continue

    
    just_time = entry[11:19]
    three_nums_time = just_time.split(':')
    second = int(three_nums_time[2])
    if second > 60 or second < 1:
        continue
    minute = int(three_nums_time[1])
    if minute > 60 or minute < 1:
        continue
    hour = int(three_nums_time[0])
    if hour > 12 or hour < 1:
        continue
    ampm = entry[20:]
    if ampm is 'PM':
        hour = hour+12
        
    time_stamp = dt.datetime(year, mon, day, hour, minute, second)
    #print(time_stamp)
    secs_since_epoch.append(time.mktime(time_stamp.timetuple()))
        
    
diff_in_time = []
for kk in range(1,len(secs_since_epoch)):
    diff_in_time.append(secs_since_epoch[kk] - secs_since_epoch[kk-1])
    
diff_in_time_std = np.std(diff_in_time)
print('Standard dev. of delta t is', diff_in_time_std, 'seconds')
