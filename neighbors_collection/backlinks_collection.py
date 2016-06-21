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
seed_dir = os.path.join(data_dir, 'seed')
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
    
def get_backlinks(name):
    link_list = []
    name = urllib.quote_plus(name.encode("utf-8"))
    site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=&list=backlinks&indexpageids=1&titles=%s" %name + "&bllimit=500&blredirect=1&redirects=1&converttitles=1&bltitle=%s" %name
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    res = page.read()    
    res = ast.literal_eval(res)
    
    for key in res['query']['backlinks']:
        link = key["title"]
        link_list.append(link)
   # print link_list
    return link_list

def get_cat(neighbor): 
    cat_list = []
  
#    neighbor = neighbor.encode("utf-8")
#    neighbor = urllib2.unquote(neighbor).decode("utf-8")
   
#     neighbor = neighbor.replace('_', ' ')
#     neighbor = neighbor.title()
    
    neighbor = urllib.quote_plus(neighbor.encode("utf-8"))
 
    site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=&indexpageids=1&redirects=1&cllimit=500&titles=%s" %neighbor
    print site
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    res = page.read()    
#    print res
    res = ast.literal_eval(res)
    if 'pages' in res['query']:
        for pidkey in  res['query']['pages']:      
            if 'categories' in res['query']['pages'][pidkey]:
                for key in res['query']['pages'][pidkey]['categories']:
                    cat = key["title"]
                    cat = cat.rstrip().split(':')[-1]
                    cat_list.append(cat)
    #print cat_list
    return cat_list
       
def clean_up(cat_list, stop_list):
    print "in cleaning function"
    state = False
    print len(cat_list)
    if not cat_list:
        state = True
        return state
    for item in cat_list:
        print item
        word_list = item.rstrip().split(' ')
        for word in word_list:
            word = word.lower()
            if word in stop_list:
                print word
                state = True
                return state
    return state         

txt_filename =  os.path.join(neighbors_dir, "stop_list.txt")
text_file = open(txt_filename, "r")
stop_list = text_file.read().split(',')

filename =  os.path.join(seed_dir, 'creation_date.json')   
scientists = load_simple_json(filename) 
backlinks_list = []
clean_list = []
Dump = {}
count = 0
for scientist, params in scientists.iteritems():
    count+=1
    print count
    scientist_name = get_name(scientist)
    backlinks_list = get_backlinks(scientist_name)
#     for link in backlinks_list:
#         cat_list = get_cat(link)
#         state = clean_up(cat_list, stop_list)
#         if state == False:
#             clean_list.append(link)
    Dump.update({scientist:backlinks_list})


output_path =  os.path.join(neighbors_dir, 'seed_ backlinks_list_en.json')  
with open(output_path, 'w') as out:
    json.dump(Dump, out, indent=4, sort_keys=True)  