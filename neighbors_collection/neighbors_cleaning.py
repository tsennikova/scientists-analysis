'''
Created on 14 Jun 2016

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
import urllib

# TODO: fix encoding


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)
def iriToUri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti == 1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

def load_simple_json(filename):
    with open(filename, 'r') as f:
#        return json.load(f)
        return json.load(f)
    
# def send_request(language, neighbor): 
#     cat_list = []
#     neighbor = neighbor.encode("utf-8")
#     neighbor = urllib2.unquote(neighbor).decode("utf-8")
#     site = wiki.Wiki("http://" + language + ".wikipedia.org/w/api.php")
#     params = {'action':'query', 'titles':neighbor, 'prop':'categories'}
#     req = api.APIRequest(site, params)
#     for res in req.queryGen(): 
#         print res
#         for pidkey  in res['query']['pages']:
#             if 'categories' in res['query']['pages'][pidkey]:
#                 for key in res['query']['pages'][pidkey]['categories']:
#                     cat = key["title"]
#                     cat = cat.rstrip().split(':')[-1]
#                     cat_list.append(cat)
#     print cat_list
#     return cat_list


def send_request(language, neighbor): 
    cat_list = []
#    neighbor = neighbor.encode("utf-8")
#    neighbor = urllib2.unquote(neighbor).decode("utf-8")
    neighbor = neighbor.replace('_', ' ')
    neighbor = neighbor.title()
    neighbor = neighbor.replace(' ', '_')
    site= "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&list=&indexpageids=1&titles=%s" %neighbor
    site = iriToUri(site)
# TODO: Strange redirect
    print site
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    res = page.read()    
    print res
    res = ast.literal_eval(res)
     
    
    for pidkey in res['pages']:
        
        if 'categories' in res['query']['pages'][pidkey]:
            for key in res['query']['pages'][pidkey]['categories']:
                cat = key["title"]
                cat = cat.rstrip().split(':')[-1]
                cat_list.append(cat)
    print cat_list
    return cat_list
    

def clean_up(cat_list, stop_list):
    print "in cleaning function"
    state = False
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

language = "en"
Dump = {}
filename =  os.path.join(neighbors_dir, 'test.json')
scientists = load_simple_json(filename)
for link, neighbors_list in scientists.iteritems():
    clean_list = [] 
    for neighbor in neighbors_list:
        cat_list= send_request(language, neighbor)
        state = clean_up(cat_list, stop_list)
        if state == False:
            clean_list.append(neighbor)
    Dump.update({link:clean_list})

output_path =  os.path.join(neighbors_dir, 'neighbors_list_clean_en.json')    
with open(output_path, 'w') as out:
    json.dump(Dump, out, indent=4, sort_keys=True)  