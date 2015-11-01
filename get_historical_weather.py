# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:58:47 2015

@author: Joe
"""

import urllib.request
from bs4 import BeautifulSoup

api_key = '47f73d3372726706'
 

f = open('wunder-data.txt', 'w')
 
# Iterate through year, month, and day
for y in range(2014, 2015):
  for m in range(1, 13):
    for d in range(1, 32):
 
      # Check if leap year
      if y%400 == 0:
        leap = True
      elif y%100 == 0:
        leap = False
      elif y%4 == 0:
        leap = True
      else:
        leap = False
 
      # Check if already gone through month
      if (m == 2 and leap and d > 29):
        continue
      elif (m == 2 and d > 28):
        continue
      elif (m in [4, 6, 9, 10] and d > 30):
        continue
 
      # Open wunderground.com url
      url = "http://www.wunderground.com/history/airport/KOSU/"+str(y)+ "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
      page = urllib.request.urlopen(url)
 
      # Get temperature from page
      soup = BeautifulSoup(page)
      
      ###
      # This line is not correct, not sure how to fix
      # Trying to scrape daily temp data from html
      dayTemp = soup.find_all(attrs={"class":"nobr"})[4].span.string
      ###
 
      # Format month for timestamp
      if len(str(m)) < 2:
        mStamp = '0' + str(m)
      else:
        mStamp = str(m)
 
      # Format day for timestamp
      if len(str(d)) < 2:
        dStamp = '0' + str(d)
      else:
        dStamp = str(d)
 
      # Build timestamp
      timestamp = str(y) + mStamp + dStamp
 
      # Write timestamp and temperature to file
      f.write(timestamp + ',' + dayTemp + '\n')
 
# Done getting data! Close file.
f.close()
