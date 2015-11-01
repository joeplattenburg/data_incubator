# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:20:48 2015

@author: plattenburg.2
"""

# This code gets weather forecast data from Weather Underground

# Personal api key for Weather Underground
api_key = '47f73d3372726706'
# Four cities to get weather forecasts
city = ['OH/Columbus', 'MA/Boston', 'CA/San_Francisco', 'WA/Seattle']

# url pieces for hourly forecast
url1 = 'http://api.wunderground.com/api/'
url2 = '/hourly/q/'
url3 = '.json'

# Import libraries
import urllib.request
#from bs4 import BeautifulSoup
import json
#import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

# Initialize variables, temperature in F, rainfall in inches, number of hours (from now), and total hours to forecast
temp_f = []
rain = []
hour = []
num_hours = []

# Loop through all cities
for kk in range(0,len(city)):
    # Concatenate url
    full_url = url1 + api_key + url2 + city[kk] + url3
    # Request api from WU
    f = urllib.request.urlopen(full_url)
    # Read as json
    json_string = f.read()
    # Parse json
    parsed_json = json.loads(json_string.decode())
    # Number of hours to forecast for the kkth city
    num_hours.append(len(parsed_json['hourly_forecast']))
    
    # Loop through each hour
    for n in range(0,num_hours[kk]):
        # Temperature
        temp_f.append(parsed_json['hourly_forecast'][n]['temp']['english'])
        # Rain
        rain.append(parsed_json['hourly_forecast'][n]['qpf']['english'])
        # How many hours
        hour.append(n+1)

# Plot Temp
for kk in range(0,len(city)):
    plt.plot(hour[num_hours[kk]*kk:num_hours[kk]*(kk+1)-1],temp_f[num_hours[kk]*kk:num_hours[kk]*(kk+1)-1],label = city[kk][3:]+', '+city[kk][0:2])
plt.xlabel('Hour')
plt.ylabel('Temperature [F]')
plt.legend(loc = 'lower right')

plt.show()

# Plot Rain    
for kk in range(0,len(city)):
    plt.plot(hour[num_hours[kk]*kk:num_hours[kk]*(kk+1)-1],rain[num_hours[kk]*kk:num_hours[kk]*(kk+1)-1],label = city[kk][3:]+', '+city[kk][0:2])
plt.xlabel('Hour')
plt.ylabel('Rain [in]')
plt.legend()
plt.show()
