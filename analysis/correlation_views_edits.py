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

# TODO: normalize edits by total number of edits 
# TODO regenerate data

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 
topic_file =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json') 

# views, edits
views_dir = os.path.join(data_dir, 'views')
edits_dir = os.path.join(data_dir, 'edits')

# scientists or topics
views_sci = os.path.join(views_dir, 'scientists')
edits_sci = os.path.join(edits_dir, 'scientists')


views_topic = os.path.join(views_dir, 'topics')
edits_topic = os.path.join(edits_dir, 'topics')


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
            year = time_list.pop(0)
            if  year!=2016:
                scientist_series += time_list
            else:
                return scientist_series
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
            edits_txt = os.path.join(edits_topic + '\\' + topic + '.txt')
            views_series = get_series(views_txt)
            edits_series = get_series(edits_txt)
            if views_series!=[] and edits_series!=[]:
                if len(views_series)<len(edits_series):
                    zero_list = [0] * (len(edits_series) - len(views_series))
                    views_series = numpy.array(zero_list + views_series, dtype=float)
                if len(views_series)>len(edits_series):   
                    zero_list = [0] * (len(views_series) - len(edits_series))
                    edits_series = numpy.array(zero_list + edits_series, dtype=float )         
                views_series = (views_series - numpy.mean(views_series)) / (numpy.std(views_series)* len(views_series))
                edits_series = (edits_series - numpy.mean(edits_series)) /  (numpy.std(edits_series) )
                correlation_list.append(numpy.correlate(views_series, edits_series)[0])
    print correlation_list
    print 'average correlation', numpy.mean(correlation_list)
    print 'min correlation', format(numpy.min(correlation_list),'f')
    print 'max correlation',format(numpy.max(correlation_list),'f')
    return

def correlation_btw_scientists():     
    correlation_list = []
    scientist_dict = load_simple_json(scientists_file)
    for scientist in scientist_dict:
        scientist = scientist.rstrip().split('/')[-1]
        views_txt = os.path.join(views_sci + '\\' + scientist + '.txt') 
        edits_txt = os.path.join(edits_sci + '\\' + scientist + '.txt')
        views_series = get_series(views_txt)
        edits_series = get_series(edits_txt)
        if views_series!=[] and edits_series!=[]:
            if len(views_series)<len(edits_series):
                zero_list = [0] * (len(edits_series) - len(views_series))
                views_series = numpy.array(zero_list + views_series, dtype=float)
            if len(views_series)>len(edits_series):   
                zero_list = [0] * (len(views_series) - len(edits_series))
                edits_series = numpy.array(zero_list + edits_series, dtype=float )         
            views_series = (views_series - numpy.mean(views_series)) / (numpy.std(views_series)* len(views_series))
            edits_series = (edits_series - numpy.mean(edits_series)) /  (numpy.std(edits_series) )
            correlation_list.append(numpy.correlate(views_series, edits_series)[0])

    print correlation_list
    print 'average correlation', numpy.mean(correlation_list)
    print 'min correlation', format(numpy.min(correlation_list),'f')
    print 'max correlation',format(numpy.max(correlation_list),'f')
    return
    
correlation_btw_scientists()
