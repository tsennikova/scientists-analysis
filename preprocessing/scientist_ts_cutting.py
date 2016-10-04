'''
Created on Sep 3, 2016

@author: Tania
'''
import json
import os
import datetime
import numpy as np
import operator
import matplotlib.pyplot as plt



base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

plots_dir = os.path.join(data_dir, 'plots')
trends_dir = os.path.join(plots_dir, 'trends')


# Change address for each dataset: views, edits, google_trends
dir = os.path.join(data_dir, 'views')
vews_seed_dir = os.path.join(dir, 'seed')
vews_baseline_dir = os.path.join(dir, 'baseline')

scientist_dir = os.path.join(dir, 'scientists')
scientist_cut_dir = os.path.join(vews_seed_dir, '3_years_before_1_after')
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 


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
#    ts_list = []
#    time_list = []
    for scientist, param_dict in scientist_dict.iteritems():
        time_list = []
        ts_list = []
        time_dict = {}
        x = []
        y = []
        days_check = []
        # comment for baseline
        event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(scientist_dir + '\\' + scientist + '.txt')      
        try:
            f = open(txtname)
            # converting string to dates
            for line in f:
                day_list = line.rstrip().split(',')
                year = day_list.pop(0)
                for idx,day in enumerate(day_list):
                    # comment for baseline
                    date = datetime.datetime(int(year), 1, 1) + datetime.timedelta(idx+1)
                    days_difference = days_between(event_date, date)
                    days_check.append(date)
                    x.append(days_difference)
                    y.append(day)     
            f.close()
     
           # x = list(range(len(y))) # only for baseline
            x = np.array(x, dtype=np.int)
            y = np.array(y, dtype=np.float)
            output_path =  os.path.join(scientist_cut_dir, scientist+'.txt')
            text_file = open(output_path, "w")
            for i in range(0, len(x)):
                if (x[i]>-1068) and (x[i]<356):
                    ts_list.append(y[i])
            text_file.write(",".join(map(lambda x: str(x), ts_list)))
            text_file.close()
            #ts_list = running_mean(ts_list, 90)
            #plt.plot(ts_list)
            #plt.savefig(trends_dir+'\\'+scientist+'.pdf')
            #plt.cla()   
        except IOError:
            continue 

    return list(ts_list), list(time_list)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

cutted_ts = []
ts_list, time_list = time_aligning(scientist_dict)
