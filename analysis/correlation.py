'''
Created on 25 Jul 2016

@author: sennikta
'''
import json
import os
import numpy
import csv
import random

from itertools import islice

# TODO solve normalization, try the same length of arrays
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 
topic_file =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json') 

views_dir = os.path.join(data_dir, 'views')
edits_dir = os.path.join(data_dir, 'edits')
google_trends_dir = os.path.join(data_dir, 'google_trends')

views_sci = os.path.join(views_dir, 'scientists')
edits_sci = os.path.join(edits_dir, 'scientists')
gooogle_trends_sci = os.path.join(google_trends_dir, 'scientists')

views_topic = os.path.join(views_dir, 'topics')
edits_topic = os.path.join(edits_dir, 'topics')
gooogle_trends_topic = os.path.join(google_trends_dir, 'google_trends')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def get_series(filename):
    scientist_series = []
    try:
        f = open(filename)
        for line in f:
            time_list = map(float, line.split(','))
            time_list.pop(0)
            scientist_series += time_list
        f.close()
    except IOError:
        #    print scientist
        return scientist_series
    return scientist_series

def correlation_btw_topics(): 
    correlation_list = []
    topic_dict = load_simple_json(topic_file)
    for scientist, topic_list in topic_dict.iteritems():
        for topic in topic_list:
            views_txt = os.path.join(views_topic + '\\' + topic + '.txt') 
            edits_txt = os.path.join(views_topic + '\\' + topic + '.txt')
            views_series = get_series(views_txt)
            edits_series = get_series(edits_txt)
            if views_series!=[] and edits_series!=[]:
                #views_series = sorted(views_series, key=lambda k: random.random())
                views_series = (views_series - numpy.mean(views_series)) / (numpy.std(views_series) *len(views_series))
                edits_series = (edits_series - numpy.mean(edits_series)) /  (numpy.std(edits_series) )
        
                correlation_list.append(numpy.correlate(views_series, edits_series))
        
    print 'average correlation', format(numpy.average(correlation_list),'f')
    print 'min correlation', format(numpy.min(correlation_list),'f')
    print 'max correlation',format(numpy.max(correlation_list),'f')
    return
    return

def get_google_trends_series(scientist):
    scientist_series = []
    csvname = os.path.join(gooogle_trends_sci + '\\' + scientist + '.csv')
    try: 
        f = open(csvname, 'rb')
        reader = csv.reader(f)
        # skip template
        for row in islice(reader, 5, 657):
            scientist_series.append(int(row[1]))
        f.close()
    except IOError:
        return scientist_series
    return scientist_series

def correlation_btw_scientists():     
    correlation_list = []
    scientist_dict = load_simple_json(scientists_file)
    for scientist in scientist_dict:

        scientist = scientist.rstrip().split('/')[-1]
        views_txt = os.path.join(views_sci + '\\' + scientist + '.txt') 
        edits_txt = os.path.join(edits_sci + '\\' + scientist + '.txt')
        views_series = get_series(views_txt)
        edits_series = get_series(edits_txt)
        google_series = get_google_trends_series(scientist)
        if views_series!=[] and edits_series!=[]:


            #views_series = sorted(views_series, key=lambda k: random.random())
            views_series = list((views_series - numpy.mean(views_series)) / (numpy.std(views_series) *len(views_series)))
            edits_series = list((edits_series - numpy.mean(edits_series)) /  (numpy.std(edits_series) ))
            correlation_list.append(max(numpy.correlate(views_series, edits_series)))
    print correlation_list
    print 'average correlation', format(numpy.average(correlation_list),'f')
    print 'min correlation', format(numpy.min(correlation_list),'f')
    print 'max correlation',format(numpy.max(correlation_list),'f')
    
    return
    
correlation_btw_scientists()
