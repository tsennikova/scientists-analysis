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
seed_dir = os.path.join(data_dir, 'seed')

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

def revisions_extraction(lang, title):
    timestamp = ""
    site = wiki.Wiki(language+".wikipedia.org/w/api.php")
    params = {'action':'query', 'titles':title, 'prop':'revisions', 'rvdir':'newer','rvlimit':1}
    req = api.APIRequest(site, params)
    result = req.query()
    for pidkey in result['query']['pages']:
        print  result['query']['pages'][pidkey]
        for key in result['query']['pages'][pidkey]['revisions']:
            timestamp=key['timestamp']
    return timestamp


url="https://en.wikipedia.org/wiki/Help:Page_history"
language, title=parse_url(url)
timestamp=revisions_extraction(language, title)
#url_list=clean_list(links)
print timestamp

filename =  os.path.join(seed_dir, 'seed_data.json')    
pages = load_simple_json(filename)
for link, param_list in pages.iteritems():
#   link = link.decode("utf-8").encode('latin-1')
    link = link.encode("utf-8")
    link = urllib2.unquote(link).decode("utf-8")
    language, title=parse_url(link)
    timestamp=revisions_extraction(language, title)
    param_list.update({'Page_created':timestamp})
    print param_list

output_path =  os.path.join(seed_dir, 'creation_date.json')    
with open(output_path, 'w') as out:
        json.dump(pages, out, indent=4, sort_keys=True)  