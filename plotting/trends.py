'''
Created on 19 Jul 2016

@author: sennikta
'''
import json
import os
from datetime import datetime
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import itertools

#TODO learn how to get date from year and day number

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
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

def time_aligning(scientist_dict, norm_dir):
    for scientist, param_dict in scientist_dict.iteritems():
        event_date = param_dict["Award_date"]
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(norm_scientist_dir + '\\' + scientist + '.txt')      
        f = open(txtname)
        for line in f:
            print line
        f.close()
        break
    return

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

time_aligning(scientist_dict, norm_dir)





