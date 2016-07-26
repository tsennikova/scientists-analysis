'''
Created on 26 Jul 2016

@author: sennikta
'''
import json
import os
import numpy
import csv
import random

from itertools import islice


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 
topic_file =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json') 

# views, edits or google trends
views_dir = os.path.join(data_dir, 'views')
edits_dir = os.path.join(data_dir, 'edits')
google_trends_dir = os.path.join(data_dir, 'google_trends')

# scientists or topics
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

def time_aligning(scientist_dict, views_dir):
    for scientist, param_dict in scientist_dict.iteritems():
        time_dict = {}
        x = []
        y = []
        days_check = []
        event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(norm_scientist_dir + '\\' + scientist + '.txt')      
        f = open(txtname)
        # converting string to dates
        for line in f:
            day_list = line.rstrip().split(',')
            year = day_list.pop(0)
            for idx,day in enumerate(day_list):
                date = datetime.datetime(int(year), 1, 1) + datetime.timedelta(idx+1)
                days_difference = days_between(event_date, date)
                days_check.append(date)
                x.append(days_difference)
                y.append(day)     
        f.close()

    return
