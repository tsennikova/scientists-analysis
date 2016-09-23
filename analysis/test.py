'''
Created on 25 Jul 2016

@author: sennikta
'''
import json
import os
import numpy
import matplotlib.pyplot as plt
import csv

from itertools import islice

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
# For views and edits
def read_txt(filename):
    scientist_dict = load_simple_json(filename)
    data_list = []
    attention_value = 0
    attention_list = []
    for scientist in scientist_dict:
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(reading_dir + '\\' + scientist + '.txt')   
        try:
            f = open(txtname)
            for line in f:
                time_list = map(float, line.split(','))
                time_list.pop(0)
                scientist_series += time_list
            f.close()
            attention_list.append(attention_value)
        except IOError:
        #    print scientist
            continue
    return attention_list


# For google trends
def read_csv(filename):
    scientist_dict = load_simple_json(filename)
    data_list = []
    attention_value = 0
    attention_list = []
    for scientist in scientist_dict:
        scientist = scientist.rstrip().split('/')[-1]
        csvname = os.path.join(reading_dir + '\\' + scientist + '.csv')
        try: 
            f = open(csvname, 'rb')
            reader = csv.reader(f)
            # skip template
            for row in islice(reader, 5, 657):
                attention_value += int(row[1])
            f.close()
            attention_list.append(attention_value)
        except IOError:
        #    print scientist
            continue        
    return attention_list

series_dict = {}

# for views and edits
name_set = ['views', 'edits']
for name in name_set:
    filename =  os.path.join(seed_dir, 'seed_creation_date.json') 
    norm_dir = os.path.join(data_dir, name)
    reading_dir = os.path.join(norm_dir, 'scientists')
    time_series = read_txt(filename)
    series_dict.update({name:time_series})

# for google trends
#filename =  os.path.join(seed_dir, 'seed_creation_date.json')    
#google_series = read_csv(filename)
#series_dict.update({'google_trends':google_series})

print numpy.correlate(series_dict['views'], series_dict['edits'])
