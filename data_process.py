# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 08:01:41 2015

@author: Joe
"""


import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime as dt
import time
import re
from csv import reader
from collections import Counter
from matplotlib.pyplot import gca


tnrfont = {'fontname':'Helvetica'}


# This function turns a time stamp to several values
def timestamp2vals(entry):
    # Get date info
    just_date = entry[0:10]
    three_nums_date = just_date.split('/')
    year = int(three_nums_date[2])
    mon = int(three_nums_date[0])
    day = int(three_nums_date[1])
    
    # Get time info
    just_time = entry[11:19]
    three_nums_time = just_time.split(':')
    second = int(three_nums_time[2])
    minute = int(three_nums_time[1])
    hour = int(three_nums_time[0])

    ampm = entry[20:]
    if ampm is 'PM':
        hour = hour+12
    # Get seconds since epoch
    try:
        time_stamp = dt.datetime(year, mon, day, hour, minute, second)
        secs_since_epoch = time.mktime(time_stamp.timetuple())
    except:
        secs_since_epoch = 0
    
    out_var = (year, mon, day, hour, minute, second, secs_since_epoch)
    return out_var
    
    

#%% Read data

# Open the data file
f = open('Seattle_Collision_Data.csv')
# Get the header lines
headers = f.readline()
headers = headers.rstrip()
header_list = headers.split(',')
    
# Get the column indices of importance from header line
headers_of_interest = ['Shape','FATALITIES','INCDATE','INJURIES','ROADCOND','SEVERITYCODE','WEATHER']
indices = []
for name in headers_of_interest:
    indices.append(header_list.index(name))
    
# Get several lists of data from the file
time_list = []
loc_list = []
severity_list = []
weather_list = []

info = reader(f,delimiter=',',quotechar='"')
for row in info:
    # Row is a list of all info for the nth incident
    # Extract info for the location, date/time, severity, and weather
    loc_list.append(row[indices[0]])
    time_list.append(row[indices[2]])
    
    # Some of these are not integers
    try:
        severity_list.append(int(row[indices[5]]))
    except:
        item_to_add = int(row[indices[5]][0]) +.5
        severity_list.append(item_to_add)
    weather_list.append(row[indices[6]])    
    
    
#%% Sort the data from past to future

time_info=[]
hours=[]
days=[]
mons=[]
blanks = []

counter = 0
for item in time_list:
    # Each element is a tuple with year, mon, day, hour, min, sec, secs since epoch
    counter = counter+1 
    # Most of the entries are good, a few are blank
    try:    
        time_info.append(timestamp2vals(item))
    except:
        blanks.append(counter-1)


for item in time_info:
    hours.append(item[3])
    days.append(item[2])
    mons.append(item[1])

#%% Get rid of the info for bad dates
for kk in range(len(blanks)-1,-1,-1):
    del(loc_list[kk])
    del(severity_list[kk])
    del(weather_list[kk])
       
counter = 0
zerolist= []
secs = []
for item in time_info:
    counter = counter+1
    # Some items may be before the epoch, throw these out
    if item[6] == 0:
        zerolist.append(counter-1)
    else:
        secs.append(item[6])
    
# Get rid of the info for more bad dates
for kk in range(len(zerolist)-1,-1,-1):
    del(loc_list[kk])
    del(severity_list[kk])
    del(weather_list[kk])
    
# Sort the events from past to future (the first couple data points seem weird, throw these out)
secs = np.array(secs)
sort_index=np.argsort(secs)
secs = secs[sort_index[2:]]
secs = secs - secs[0]

# Sort the other info
loc_list = [loc_list[i] for i in sort_index[2:]]
severity_list = [severity_list[i] for i in sort_index[2:]]
weather_list = [weather_list[i] for i in sort_index[2:]]


plt.figure(0)
plt.plot(secs)
plt.xlabel('Event', **tnrfont)
plt.ylabel('Time [s]', **tnrfont)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.savefig('Fig0.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')

# Convert seconds into the associated day
days1 = []
for sec in secs:
    days1.append(int(sec)//(60*60*24))
    

plt.figure(1)
plt.plot(days1)
plt.xlabel('Event', **tnrfont)
plt.ylabel('Time [days]', **tnrfont)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.savefig('Fig1.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')

#%% Total number of incidents associated with a particular weather condition

names=[]
com_weather_total = Counter(weather_list).most_common()
for name in com_weather_total:
    if name[0] == '':
        names.append('None')
    else:
        names.append(name[0])
vals = [x[1] for x in com_weather_total]

plt.figure(2)
plt.bar(range(0,len(names[0:7])),vals[0:7])
plt.xticks( np.arange(len(names[0:7])), names[0:7], rotation=45, **tnrfont)
plt.ylabel('Number of Occurances', **tnrfont)
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.savefig('Fig2.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')


#%% Figure out how many events in a given day

start_val = 0
day_list = []
day_dict = dict()
for day in range(0,max(days1)+1):
    num_events = days1.count(day)
    if num_events>0:
        start_val = days1.index(day)
        stop_val = start_val+num_events
        weather = Counter(weather_list[start_val:stop_val]).most_common()[0][0]
        weather_consistency = Counter(weather_list[start_val:stop_val]).most_common()[0][1]/num_events
        severity = np.mean(severity_list[start_val:stop_val])
    else:
        weather = ''
        severity = 0
        weather_consistency = 0
    day_list.append((day,num_events,weather,severity,weather_consistency))
    
        
# Now day list is a list of tuples containing the elapsed day from the start day,
# the number of incidents on that day, and the most common weather
        
# Sorry the variable names get a little weird here
# Day index
x_val = [x[0] for x in day_list]
# Number of incidents
y_val = [x[1] for x in day_list]
# Weather condition on that day
z_val = [x[2] for x in day_list]
# Average severity for that day
w_val = [x[3] for x in day_list]
# Weather consistency (i.e. what fraction of events agree with most common)
c_val = [x[4] for x in day_list]

# Number and severity of incidents per day
plt.figure(3)
plt.plot(x_val,y_val)
plt.xlabel('Day', **tnrfont)
plt.ylabel('Number of Events', **tnrfont)
plt.savefig('Fig3.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')

plt.figure(4)
plt.plot(x_val,w_val)
plt.xlabel('Day', **tnrfont)
plt.ylabel('Average Severity of Events', **tnrfont)
plt.savefig('Fig4.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')

    
#%% How many days are most associated with a given weather condition
   
   
com_weather = Counter(z_val).most_common()
com_weather_states = [x[0] for x in com_weather]
com_weather_nums = [x[1] for x in com_weather]
for kk in range(0,len(com_weather)):
    if com_weather[kk][0] == 'Raining':
        index1 = kk
    if com_weather[kk][0] == '':
        com_weather_states[kk] = 'None'

#%% How many incidents (and average severity) are associated with a given weather condition

clear_incs = [y_val[i] for i in range(0,len(y_val)) if z_val[i] == com_weather_states[0]]
clear_sev = [w_val[i] for i in range(0,len(w_val)) if z_val[i] == com_weather_states[0]]
clear_cons = [c_val[i] for i in range(0,len(c_val)) if z_val[i] == com_weather_states[0]]
rain_incs = [y_val[i] for i in range(0,len(y_val)) if z_val[i] == com_weather_states[2]]
rain_sev = [w_val[i] for i in range(0,len(w_val)) if z_val[i] == com_weather_states[2]]
rain_cons = [c_val[i] for i in range(0,len(c_val)) if z_val[i] == com_weather_states[2]]
    
print('Mean number of incidents for: \n')
print('Clear Days (', 100*np.mean(clear_cons), '%): ', np.mean(clear_incs), ' with mean severity of ', np.mean(clear_sev))
print('Rainy Days (', 100*np.mean(rain_cons), '%): ', np.mean(rain_incs), ' with mean severity of ', np.mean(rain_sev))

plt.figure(5)
plt.bar(range(0,len(com_weather_states)),com_weather_nums)
plt.xticks( np.arange(len(com_weather_states)), com_weather_states, rotation=45, **tnrfont)
plt.ylabel('Number of Occurances', **tnrfont)
plt.savefig('Fig5.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')


#%% Check days that have particularly many incidents

y_val_mean = np.mean(y_val)
y_val_std = np.std(y_val)
extreme_cases = []
counter = 0
for event in y_val:
    # Check events with more than 1 std greater than the mean number of incidents
    if event > y_val_mean+y_val_std:
        extreme_cases.append((z_val[counter], c_val[counter]))
    counter = counter+1

extreme_weather = [x[0] for x in extreme_cases]

counter_object = (Counter(extreme_weather).most_common())
for kk in range(0,len(counter_object)):
    if counter_object[kk][0] == 'Raining':
        index = kk

fraction = (Counter(extreme_weather).most_common()[index][1])/len(extreme_cases)
fraction1 = (com_weather[index1][1])/len(x_val)
#extreme_cons = [x[1] for x in extreme_cases]
print('On days with particularly many incidents, ', fraction*100, '% of those days were rainy')
print('Overall, ', fraction1*100, '% of days were rainy')
    
#%% Plots
    
    
plt.figure(6)
plt.hist(hours)
plt.xlabel('Hour', **tnrfont)
plt.ylabel('Number of Events', **tnrfont)
plt.savefig('Fig6.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')


plt.figure(7)
plt.hist(days, bins=31)
plt.xlabel('Day', **tnrfont)
plt.ylabel('Number of Events', **tnrfont)
plt.savefig('Fig7.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')

plt.figure(8)
plt.hist(mons, bins=12)
plt.xlabel('Month', **tnrfont)
plt.ylabel('Percentange of Events', **tnrfont)
plt.savefig('Fig8.jpeg', format='jpeg', dpi=1000, bbox_inches='tight')