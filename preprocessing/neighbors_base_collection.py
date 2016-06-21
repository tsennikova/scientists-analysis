'''
Created on 21 Jun 2016

@author: sennikta
'''

from wikitools import wiki, api
import wikipedia
import urllib, json
import re, urlparse
import pprint
import mwparserfromhell
from mwparserfromhell.nodes import Wikilink
import os
from networkx.classes.function import neighbors
import urllib2
import ast


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')

def load_simple_json(filename):
    with open(filename, 'r') as f:
#        return json.load(f)
        return json.load(f)

def get_name(link):
    link = link.encode("utf-8")
    link = urllib2.unquote(link).decode("utf-8")
    title = link.rstrip().split('/')[-1]
    return title
    
def get_title(name):
    
    name = urllib.quote_plus(name.encode("utf-8"))
    site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&indexpageids=1&redirects=1&converttitles=1&titles=%s" %name
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    res = page.read()    
    res = ast.literal_eval(res)
    for pidkey in  res['query']['pages']:  
        return res['query']['pages'][pidkey]['title']
       
         

filename1 =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json')
filename2 =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json')
scientists_seed = load_simple_json(filename1) 
scientists_baseline = load_simple_json(filename2)
scientists = scientists_seed.copy()
scientists.update(scientists_baseline) 
scientist_list = []
neighbors_list = []
for scientist, neighbors in scientists.iteritems():
    scientist_name = get_name(scientist)
    scientist_title = get_title(scientist_name)
    if scientist_title not in scientist_list:
        scientist_list.append(scientist_title)
        print len(scientist_list)
    for neighbor in neighbors:
        #neighbor_name = get_name(neighbor)
        neighbor_title = get_title(neighbor)
        if neighbor_title not in neighbors_list:
            neighbors_list.append(neighbor_title)
        
        


scientists_output_path =  os.path.join(neighbors_dir, 'scientists_list.txt')  
text_file = open(scientists_output_path, "w")
for item in scientist_list:
    text_file.write("%s\n" % item)
text_file.close()   


neighbors_output_path =  os.path.join(neighbors_dir, 'topics_list.txt')  
text_file = open(neighbors_output_path, "w")
for item in neighbors_list:
    text_file.write("%s\n" % item)
text_file.close()   