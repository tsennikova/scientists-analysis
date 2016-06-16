'''
Created on 15 Jan. 2016

@author: Tania Sennikova
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


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
neighbors_dir = os.path.join(data_dir, 'neighbors')


def load_simple_json(filename):
    with open(filename, 'r') as f:
#        return json.load(f)
        return json.load(f)
    
def send_request(language, title): 
    k = 0            
    site = wiki.Wiki("http://" + language + ".wikipedia.org/w/api.php")
#    site.setUserAgent("Mozilla/5.0") 
    # Get the article text in wiki format
    params = {'action':'parse', 'page':title, 'prop':'wikitext'}
    req = api.APIRequest(site, params) 
    try:
        textdict = {}
        text = ''
        wikicode = ''
        linklist = []
        res = req.query(querycontinue=False)
        textdict = res['parse']['wikitext']
        text = textdict['*']
        wikicode = mwparserfromhell.parse(text)
        # print wikicode.encode("utf-8")
        filtered_code = wikicode.filter_wikilinks()
        for node in filtered_code: 
            link = node.title
            if ":" not in link:
                if link is not None:
                    strlink = link.encode("utf-8")
                    strlink = strlink.decode("utf-8")
#                     strlink = strlink.decode("utf-8").lower()
#                     strlink = strlink.replace(' ', '_')
                    #strlink = language + "/" + strlink
                    # strlink=urllib.quote(strlink.encode("utf-8"))
                    if strlink not in linklist:
                        linklist.append(strlink)
 
#         title = title.lower()
#         title = title.replace(' ', '_')
        #print title
        if title not in linklist:
            linklist.append(title)

        return linklist
    except:
        print 'Catched exeption'
        k+=1
        print title
        
def get_title(link):
    link = link.encode("utf-8")
    link = urllib2.unquote(link).decode("utf-8")
    title = link.rstrip().split('/')[-1]
    return title

Dump = {} 
errorlist = []
k = 0

filename =  os.path.join(seed_dir, 'creation_date.json')    
# Loading files with initial list of articles (Country+CulturalAspect) 
scientists = load_simple_json(filename) 
language = "en"
for link, params in scientists.iteritems():
    title = get_title(link)
    dumpValue = send_request(language, title)
    dumpKey = link
    if dumpValue != []:
        Dump.update({dumpKey:dumpValue})
    else:
        k += 1
        errorlist.append(dumpKey)
                
output_path =  os.path.join(neighbors_dir, 'neighbors_list_en.json')    
with open(output_path, 'w') as out:
    json.dump(Dump, out, indent=4, sort_keys=True)  
        
