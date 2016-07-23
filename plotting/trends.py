'''
Created on 19 Jul 2016

@author: sennikta
'''
import json
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

# The result of the plotting is not readable

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')
general_trends = os.path.join(plots_dir, 'general_trends')

# Change address for each dataset: views, edits, google_trends
norm_dir = os.path.join(data_dir, 'views_normalized')
norm_scientist_dir = os.path.join(norm_dir, 'scientists')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def days_between(d1, d2):
    return (d2 - d1).days

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def time_aligning(scientist_dict, norm_dir):
    
    for scientist, param_dict in scientist_dict.iteritems():
        print scientist
        plt.figure()
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
        x = np.array(x, dtype=np.int)
        y = np.array(y, dtype=np.float)
        y = running_mean(y, 90)
        x = running_mean(x, 90)
        plt.plot(x, y)
#        break
    plt.show()
    return

filename =  os.path.join(seed_dir, 'test.json')  
scientist_dict = load_simple_json(filename)

time_aligning(scientist_dict, norm_dir)





