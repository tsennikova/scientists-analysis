'''
Created on May 28, 2016

@author: Tania
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
seed_dir = os.path.join(data_dir, 'baseline')
neighbors_dir = os.path.join(data_dir, 'neighbors')


def load_simple_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti == 1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts))
    

def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

topic_dict={}

def revisions_extraction(lang, title):
    timestamp = ""
    site = wiki.Wiki(language+".wikipedia.org/w/api.php")
    params = {'action':'query', 'titles':title, 'prop':'revisions', 'rvdir':'newer','rvlimit':1}
    req = api.APIRequest(site, params)
    result = req.query()
    for pidkey in result['query']['pages']:
        #print  result['query']['pages'][pidkey]
        if 'revisions' in result['query']['pages'][pidkey]:
            for key in result['query']['pages'][pidkey]['revisions']:
                timestamp=key['timestamp']
    return timestamp


url="https://en.wikipedia.org/wiki/Help:Page_history"
language, title=parse_url(url)
timestamp=revisions_extraction(language, title)
#url_list=clean_list(links)
count = 0
filename =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json')    
pages = load_simple_json(filename)
for link, topic_list in pages.iteritems():
    count+=1
    print count
    print link
#     link = link.encode("utf-8")
#     link = urllib2.unquote(link).decode("utf-8")
#     language, title=parse_url(link)
    for topic in topic_list:
        timestamp=revisions_extraction("en", topic)
        topic_dict.update({topic:timestamp})
print topic_dict

output_path =  os.path.join(neighbors_dir, 'baseline_topic_creation_date.json')    
with open(output_path, 'w') as out:
        json.dump(topic_dict, out, indent=4, sort_keys=True)  