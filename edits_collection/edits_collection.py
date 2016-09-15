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
import ast
import urllib

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
edits_dir = os.path.join(data_dir, 'edits')
scientits_dir = os.path.join(edits_dir, 'scientists')
topics_dir = os.path.join(edits_dir, 'topics')
    
def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

def revisions_extraction(username_list, timestamp_list,lang, name, rvcontinue):
    timestamp = "" 
   # title = 'Main_Page'
    title = name.replace('_', ' ')
    title = urllib.quote_plus(title.encode("utf-8"))
    
    if rvcontinue != 0:
        # if there are more than 500 edits - recoursive call
        site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles=%s" %title + "&rvcontinue=%s" %rvcontinue
    else:
        site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles=%s" %title
    
    hdr = {'User-Agent': 'Mozilla/5.0'} 
    req = urllib2.Request(site,headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    result = page.read()    
    prefix = result.rstrip().split(',')[0]
    # convert string to dict 
    result = ast.literal_eval(result)
    for pidkey in result['query']['pages']:
        for key in result['query']['pages'][pidkey]['revisions']:
            timestamp = key['timestamp']
            if 'user'  in key:
                username = key['user']
                bot_detected = bot_detection(username, bots_list)
            else:
                username = 'hidden'
            timestamp = timestamp.rstrip().split('T')[0]
            if bot_detected != True:
                if timestamp_list == [] and username_list ==[]: 
                    # we save timestamp and username in the lists in order to check if one user changed the article several times per day
                    timestamp_list.append(timestamp)
                    username_list.append(username)
                elif timestamp != timestamp_list[-1] or username != username_list[-1]:
                    timestamp_list.append(timestamp)
                    username_list.append(username)
    # check if there are more than 500 edits
    if "rvcontinue" in prefix:
        rvcontinue = prefix.rstrip().split('\"')[5]
        return revisions_extraction(username_list, timestamp_list, lang, name, rvcontinue)
    else:
        return timestamp_list

def bot_detection(username, bots_list):
    status = False
    if username in bots_list:
        status = True
    return status


txt_filename =  os.path.join(edits_dir, "TOTAL_unique_bots.txt")
text_file = open(txt_filename, "r")
bots_list = text_file.read().splitlines()



filename =  os.path.join(neighbors_dir, 'topics_list-1.txt')    
result_list = []
count = 0
time_array = [0]
time_dict = {}

with open(filename) as f:
    link_list = f.read().splitlines()

link_list = ['Main_Page']  
for link in link_list:
    print count
    print link
    count +=1
    timestamp_list = []
    username_list = []
    original_link = link
    link = link.encode("utf-8")
    link = urllib2.unquote(link).decode("utf-8")
    #language, title=parse_url(link)
    link = link.replace('_', ' ')
    timestamp_list = revisions_extraction(username_list, timestamp_list,'en', link,0)
    # Go through the list of timestamps that was returned by API
    for timestamp in timestamp_list:
        # Convert str to the data format
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d')
        # Get the number of the day in the year
        index = int(timestamp.strftime('%j'))
        year = int(timestamp.year)
        # Create a dictionary with the key - year, value - list of edit dates and counts
        if year==time_array[0]: 
            # if its repeating year (year is the first element of the list), than increase the ' of edits in a particular day
            time_array[index] +=1 
        else:       
            time_array = [year] # year is the first element of the list
            if year != 2008 and year != 2012 and year != 2004 and year != 2016:
                listofzeros = [0] * 365
                listofzeros [index-1] = 1 # add a new array with the first edit
                time_array = time_array + listofzeros      
            else:
                listofzeros = [0] * 366
                listofzeros [index-1] = 1
                time_array = time_array + listofzeros

        time_dict.update({time_array[0]:time_array})
    year_list = range(min(list(time_dict.keys())), 2016)   
    for year in year_list:
        if year not in time_dict:
            if year != 2008 and year != 2012 and year != 2004 and year != 2016:
                listofzeros = [0] * 365
            else:
                listofzeros = [0] * 366
            listofzeros = [year] + listofzeros
            time_dict.update({year:listofzeros})
    time_dict = collections.OrderedDict(sorted(time_dict.items()))
    original_link = original_link.translate(None, ':*') 
 #   original_link = original_link.rstrip().split('/')[-1]
    output_path =  os.path.join(topics_dir, original_link+'.txt')    
    text_file = open(output_path, "w")
    
    for key in time_dict:
        text_file.write(",".join(map(lambda x: str(x), time_dict[key])))
        text_file.write("\n")
    text_file.close()  
    time_dict = {} 
    break
    
