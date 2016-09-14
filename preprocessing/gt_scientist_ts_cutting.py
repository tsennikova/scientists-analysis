'''
Created on Sep 14, 2016

@author: Tania
'''
import json
import os
import datetime
import csv
import numpy as np
import operator
import matplotlib.pyplot as plt
from itertools import islice


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

plots_dir = os.path.join(data_dir, 'plots')
trends_dir = os.path.join(plots_dir, 'trends')


google_trends_dir = os.path.join(data_dir, 'google_trends_normed_by_baseline')
scientist_dir = os.path.join(google_trends_dir, 'scientists')
scientist_cut_dir = os.path.join(google_trends_dir, 'scientists_before_the_award')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def days_between(d1, d2):
    return (d2 - d1).days

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def time_aligning(scientist_dict):
    for scientist, param_dict in scientist_dict.iteritems():
        ts_list = []
        time_list = []
        time_dict = {}
        x = []
        y = []
        days_check = []
        # comment for baseline
        event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        
        scientist = scientist.rstrip().split('/')[-1]
        csvname = os.path.join(scientist_dir + '\\' + scientist + '.csv')  
        #print csvname    
        try:
            f = open(csvname)
            reader = csv.reader(f)
            for row in islice(reader, 1, 653):
                year = int(row[2].rstrip().split('-')[0])
                if year>2004 and year<2016:
                    y.append(float(row[1]))
                    week_beg = datetime.datetime.strptime(row[2].rstrip().split(' - ')[0], "%Y-%m-%d")
                    week_end = datetime.datetime.strptime(row[2].rstrip().split(' - ')[1], "%Y-%m-%d")
                    if event_date>week_beg and event_date<week_end:
                        ind=len(y)-1
            f.close()
            for i in range(0,len(y)):
                # comment for baseline
                x.append(i-ind)
                #x.append(i)
            output_path =  os.path.join(scientist_cut_dir, scientist+'.txt')
            text_file = open(output_path, "w")
            for i in range(0, len(x)):
                if x[i]<0:
                    ts_list.append(y[i])
                    time_list.append(x[i])
            text_file.write(",".join(map(lambda x: str(x), ts_list)))
            text_file.close()
        except IOError:
            continue
        
    return list(ts_list), list(time_list)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

cutted_ts = []
ts_list, time_list = time_aligning(scientist_dict)
