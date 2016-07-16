'''
Created on Jul 16, 2016

@author: Tania
'''
# TODO make weekly and monthly aggregation

import json
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
neighbors_dir = os.path.join(data_dir, 'neighbors')
plots_dir = os.path.join(data_dir, 'plots')

def load_simple_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

filename =  os.path.join(neighbors_dir, 'seed_topic_creation_date.json')    
topic_dict = load_simple_json(filename)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')    
scientist_dict = load_simple_json(filename)

filename =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json')    
main_dict = load_simple_json(filename)

timelag_dict = {}
time_list = []

for scientist, topic_list in main_dict.iteritems():
    
    scientist_date = scientist_dict.get(scientist).get('Page_created').rstrip().split('T')[0]
    for topic in topic_list:
        topic_date = topic_dict.get(topic).rstrip().split('T')[0]
        time_lag = days_between(scientist_date, topic_date)
        time_list.append(time_lag)
#         if time_lag in timelag_dict:
#             timelag_dict[time_lag]+=1
#         else:
#             timelag_dict[time_lag]=1
#print timelag_dict
plt.title("Time lag between the articles creation")
plt.xlabel("Time lag (days)")
plt.ylabel("Probability")
#plt.hist(time_list, bins=[-360, -330, -300, -270, -240, -210, -180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
#plt.hist(time_list, bins=[-1000, -900, -800, -700, -600, -500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
plt.hist(time_list, bins=50, normed = True)
#plt.show()
plt.savefig(plots_dir+'/timelag_(seed_creation_date).pdf')
            

#timestamp = timestamp.rstrip().split('T')[0]
# Convert str to the data format
#timestamp = datetime.strptime(timestamp, '%Y-%m-%d')
# Get the number of the day in the year
#index = int(timestamp.strftime('%j'))
#year = int(timestamp.year)


