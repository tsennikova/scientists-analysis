'''
Created on Sep 9, 2016

@author: Tania
'''
import json
import csv
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import operator
from itertools import islice

# patterns are fucked up, change the time period for clustering and etc
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')


# Change address for each dataset: views, edits, google_trends
dir = os.path.join(data_dir, 'google_trends_normed_by_baseline')
scientist_dir = os.path.join(dir, 'scientists')


# for plotting
general_plot_dir  = os.path.join(data_dir, 'plots')
plots_dir = os.path.join(general_plot_dir, 'ts_plots')
gt_plots_dir = os.path.join(plots_dir, 'google_trends')

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
    ts_list = []
    time_list = []
    for scientist, param_dict in scientist_dict.iteritems():
        time_dict = {}
        x = []
        y = []
        days_check = []
        # comment for baseline
        event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        scientist = scientist.rstrip().split('/')[-1]
        csvname = os.path.join(scientist_dir + '\\' + scientist + '.csv')      
        try:
            f = open(csvname)
            reader = csv.reader(f)
            for row in islice(reader, 1, 653):
                year = int(row[2].rstrip().split('-')[0])
                if year>2004 and year<2016:
                    y.append(float(row[1]))
            f.close()
            
            x = list(xrange(len(y)))
            x = running_mean(x, 13)
            y = running_mean(y, 13)
            
            plt.plot(x, y)
            plt.savefig(gt_plots_dir+'\\'+scientist+'.pdf')
            plt.clf()
            plt.cla()
            time_list.append(x)
            ts_list.append(y)
        except IOError:
            continue
        #break
    return list(ts_list), list(time_list)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

ts_list, time_list = time_aligning(scientist_dict)
