# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:20:48 2015

@author: plattenburg.2
"""

api_key = '47f73d3372726706'
city = 'OH/Columbus'

url1 = 'http://api.wunderground.com/api/'
url2 = '/geolookup/conditions/q/'
url3 = '.json'

full_url = url1 + api_key + url2 + city + url3

import urllib.request
import json
f = urllib.request.urlopen(full_url)
json_string = f.read()


parsed_json = json.loads(json_string.decode())

location = parsed_json['location']['city']

temp_f = parsed_json['current_observation']['temp_f']
wind = parsed_json['current_observation']['wind_mph']

print("Current temperature in ", location, "is:", temp_f, 'deg F and the windspeed is', wind, ' mph')

f.close()