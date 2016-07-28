'''
Created on 19 Jul 2016

@author: sennikta
'''

import os
from sklearn import preprocessing
import numpy as np
from os import listdir
import calendar
import collections
import csv
from itertools import islice
import pandas as pd

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)}, threshold=np.inf)

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
views_norm_dir = os.path.join(data_dir, 'views_normalized')
edits_norm_dir = os.path.join(data_dir, 'edits_normalized')
google_trends_norm_dir = os.path.join(data_dir, 'google_trends_normalized')
views_norm_scientist_dir = os.path.join(views_norm_dir, 'scientists')
google_trends_norm_scientist_dir  = os.path.join(google_trends_norm_dir, 'scientists')
edits_norm_scientist_dir  = os.path.join(edits_norm_dir, 'scientists')

# Change address for each dataset: views, edits, google_trends
edits_dir = os.path.join(data_dir, 'edits')
google_trends_dir = os.path.join(data_dir, 'google_trends')
scientists_dir = os.path.join(edits_dir, 'scientists')

# Split normalized time series back to years
def split_time_series(time_series_norm, years_list):
    i = 0
    time_dict = {}
    time_series_norm = time_series_norm.tolist()
    for year in years_list:
        if calendar.isleap(year) == True:
            year_series = time_series_norm[0][i:i+366]
            year_series.insert(0,year)
            i += 366
        else:
            year_series = time_series_norm[0][i:i+365]
            year_series.insert(0,year)
            i += 365
          
        time_dict.update({year:year_series})
        year_series = []
    time_dict = collections.OrderedDict(sorted(time_dict.items()))
    return time_dict

def output_txt(time_dict, file_name):
    output_path =  os.path.join(edits_norm_scientist_dir, file_name)
    text_file = open(output_path, "w")
    for key in time_dict:
        text_file.write(",".join(map(lambda x: str(x), time_dict[key])))
        text_file.write("\n")
    text_file.close()  
    time_dict = {} 
    return

# For views and edits
def read_txt(dir):
    files_list = listdir(dir)
    for file_name in files_list:
        print file_name
        time_list = []
        time_series = []
        years_list = [] 
        txtname = os.path.join(dir + '\\' + file_name)      
        f = open(txtname)
        for line in f:
            time_list = map(int, line.split(','))
            years_list.append(time_list[0])
            time_list.pop(0)
            time_series += time_list 
        f.close()
        # Normalization mean=0, std=1
        time_series = np.array([time_series],  dtype=np.float64)  
        time_series_norm = preprocessing.scale(time_series, axis=1)
        time_dict = split_time_series(time_series_norm, years_list)
        output_txt(time_dict, file_name)
        time_series.fill(0)
        time_series_norm.fill(0)                     
    return

def read_csv(dir):
    
    files_list = listdir(dir)
    for file_name in files_list:
        print file_name
        output_path =  os.path.join(google_trends_norm_scientist_dir, file_name)
        time_series = []
        week_intervals = []
        csvname = os.path.join(dir + '\\' + file_name)         
        f = open(csvname, 'rb')
        reader = csv.reader(f)
        # skip template
        for row in islice(reader, 5, 657):
            time_series.append(row[1])
            week_intervals.append(row[0])
        f.close()
        time_series = np.array([time_series],  dtype=np.float64)
        time_series_norm = preprocessing.scale(time_series, axis=1)      
        data = pd.DataFrame({'Week':week_intervals, 'Interest':time_series_norm[0]})
        data.to_csv(output_path, sep=',') 
    return

read_txt(scientists_dir)

