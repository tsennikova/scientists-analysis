'''
Created on 23 Jun 2016

@author: sennikta
'''
from wikitools import wiki, api
import wikipedia
import pprint
import json
import re, urlparse
import urllib2
import os
from datetime import datetime
import collections


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
edits_dir = os.path.join(data_dir, 'edits')
scientisis_dir = os.path.join(edits_dir, 'scientists')

    
def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

def revisions_extraction(lang, title):
    timestamp = ""
    timestamp_list = []
    username_list = []
    site = wiki.Wiki("http://" +lang+".wikipedia.org/w/api.php")
    params = {'action':'query', 'titles':title, 'prop':'revisions', 'rvdir':'newer'}
    req = api.APIRequest(site, params)
    for result in req.queryGen():
        for pidkey in result['query']['pages']:
            for key in result['query']['pages'][pidkey]['revisions']:
                timestamp = key['timestamp']
                username = key['user']
                bot_detected = bot_detection(username)
                timestamp = timestamp.rstrip().split('T')[0]
                if bot_detected != True:
                    if timestamp_list == [] and username_list ==[]: 
                        timestamp_list.append(timestamp)
                        username_list.append(username)
                    elif timestamp != timestamp_list[-1] and username != username_list[-1]:
                        timestamp_list.append(timestamp)
                        username_list.append(username)
    return timestamp_list

def bot_detection(username):
    status = False
    username=username.lower()
    if "bot" in username:
        status = True
    return status

filename =  os.path.join(neighbors_dir, 'scientists_list-1.txt')    
result_list = []
timestamp_list = []
count = 0
time_array = [0]
time_dict = {}

with open(filename) as f:
    link_list = f.read().splitlines()
    
for link in link_list:
    count +=1
    original_link = link
    link = link.encode("utf-8")
    link = urllib2.unquote(link).decode("utf-8")
    #language, title=parse_url(link)
    link = link.replace('_', ' ')
    timestamp_list = revisions_extraction('en', link)
    # Go through the list of timestamps tha was returned by API
    for timestamp in timestamp_list:
        # Convert to the data format
        #timestamp = timestamp.rstrip().split('T')[0]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d')
        # Get the number of the day in the year
        index = int(timestamp.strftime('%j'))
        year = int(timestamp.year)
        # Create a dictionary with the key - year, value - list of edit dates and counts
        if year==time_array[0]: # if its repeating year
            time_array[index] +=1
        else:       
            time_array = [year]
            if year != 2008 and year != 2012:
                listofzeros = [0] * 365
                listofzeros [index-1] = 1
                time_array = time_array + listofzeros
            else:
                listofzeros = [0] * 366
                listofzeros [index-1] = 1
                time_array = time_array + listofzeros
        time_dict.update({time_array[0]:time_array})   
    time_dict = collections.OrderedDict(sorted(time_dict.items()))
     
    output_path =  os.path.join(scientisis_dir, original_link+'.txt')    
    text_file = open(output_path, "w")
    
    for key in time_dict:
        text_file.write(",".join(map(lambda x: str(x), time_dict[key])))
        text_file.write("\n")
    text_file.close()   
    
