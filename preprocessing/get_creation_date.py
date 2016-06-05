'''
Created on May 28, 2016

@author: Tania
'''
from wikitools import wiki, api
import wikipedia
import pprint

def parse_url(link):
    language = link.rstrip().split('.')[0]
    title= link.rstrip().split('/')
    return language, title[-1]   

def revisions_extraction(lang, title):
    timestamp = ""
    site = wiki.Wiki(language+".wikipedia.org/w/api.php")
    #urllib2.quote(title.encode("utf8"))
    #title = title.encode("utf-8")
    params = {'action':'query', 'titles':title, 'prop':'revisions', 'rvdir':'newer','rvlimit':1}
    req = api.APIRequest(site, params)
    result = req.query()
    for pidkey in result['query']['pages']:
        for key in result['query']['pages'][pidkey]['revisions']:
            timestamp=key['timestamp']
    return timestamp


url="https://en.wikipedia.org/wiki/Help:Page_history"
language, title=parse_url(url)
timestamp=revisions_extraction(language, title)
#url_list=clean_list(links)
print timestamp