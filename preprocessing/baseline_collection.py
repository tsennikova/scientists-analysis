'''
Created on Jun 5, 2016

@author: Tania
'''
import os
import sys
'''
Created on May 28, 2016

@author: Tania
'''
from wikitools import wiki, api
import wikipedia
import pprint
import csv

def wiki_search(keyword):
    title=""
    site = wiki.Wiki("https://en.wikipedia.org/w/api.php")
    # get the title of the article
    params = {'action':'query',  'list':'search', 'srsearch':keyword, 'srnamespace':0, 'srwhat':'nearmatch', 'srlimit':1, 'srprop':'titlesnippet', 'srenablerewrites':1}
    req = api.APIRequest(site, params)
    result = req.query()
    if result['query']['search']: 
        for key, value in result['query']['search'][0].iteritems():
            if key=='title':
                title=value
        # get the URL of the article
        params = {'action':'query',  'prop':'info', 'titles':title, 'inprop':'url'}
        req = api.APIRequest(site, params)
        result = req.query()
        for pidkey in result['query']['pages']:
            for key, value in result['query']['pages'][pidkey].iteritems():
                if key=='fullurl':
                    url=value
        return url
    
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
baseline_dir = os.path.join(data_dir, 'baseline')

csv_path =os.path.join(baseline_dir, 'prominent_scientists_(mearged_2001,2014,2015_TR).csv')
csvfile = open(csv_path , 'r')
reader = csv.reader(csvfile)
data=[]
for row in reader:
    keyword =  row[0]+" "+row[1]
    url=wiki_search(keyword)
    if url is not None:
        csv_row = [keyword, url, row[3]]
        data.append(csv_row)
csvfile.close()

output_path =  os.path.join(baseline_dir, 'baseline.csv')

with open(output_path, 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(data)

