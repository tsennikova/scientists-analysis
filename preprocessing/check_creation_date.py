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

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')


    
def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

def revisions_extraction(lang, title):
    timestamp = ""
    timestamp_list = []
    site = wiki.Wiki("http://" +lang+".wikipedia.org/w/api.php")
    params = {'action':'query', 'titles':title, 'prop':'revisions', 'rvdir':'newer'}
    req = api.APIRequest(site, params)
    for result in req.queryGen():
        for pidkey in result['query']['pages']:
            for key in result['query']['pages'][pidkey]['revisions']:
                timestamp=key['timestamp']
                timestamp_list.append(timestamp)
    return timestamp_list

filename =  os.path.join(neighbors_dir, 'topics_list.txt')    
result_list = []
timestamp_list = []
count = 0
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
    for timestamp in timestamp_list:
        parse_timestamp = int(timestamp.rstrip().split('-'))
    
    if timestamp < 2016:
        result_list.append(original_link)
    print count
    
output_path =  os.path.join(neighbors_dir, 'topics_list_before2016.txt')    
text_file = open(output_path, "w")
for item in result_list:
    text_file.write("%s\n" % item)
text_file.close()   
