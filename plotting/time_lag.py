'''
Created on Jul 16, 2016

@author: Tania
'''
import json
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

#TODO: show to hists in one plot (seed+baseline)

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
baseline_dir = os.path.join(data_dir, 'baseline')
neighbors_dir = os.path.join(data_dir, 'neighbors')
plots_dir = os.path.join(data_dir, 'plots')

def load_simple_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

def weekly_aggregation(time_list):
    weekly_list = []
    for day in time_list:
        day = day/7
        weekly_list.append(day)
    return weekly_list

def monthly_aggregation(time_list):
    monthly_list = []
    for day in time_list:
        day = day/30
        monthly_list.append(day)
    return monthly_list


def plotting(array, name):
    plt.title("Time lag between the articles creation")
    plt.xlabel("Time lag (months)")
    plt.ylabel("Probability")
    #plt.hist(time_list, bins=[-360, -330, -300, -270, -240, -210, -180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    #plt.hist(time_list, bins=[-1000, -900, -800, -700, -600, -500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    plt.hist(array, bins=50, normed = True)
    #plt.show()
    plt.savefig(plots_dir+name)
    return


filename =  os.path.join(neighbors_dir, 'baseline_topic_creation_date.json')    
topic_dict = load_simple_json(filename)

filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')    
scientist_dict = load_simple_json(filename)

filename =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json')    
main_dict = load_simple_json(filename)

timelag_dict = {}
time_list = []

for scientist, topic_list in main_dict.iteritems():
    
    scientist_date = scientist_dict.get(scientist).get('Page_created').rstrip().split('T')[0]
    for topic in topic_list:
        topic_date = topic_dict.get(topic).rstrip().split('T')[0]
        time_lag = days_between(scientist_date, topic_date)
        time_list.append(time_lag)

monthly_list = monthly_aggregation(time_list)
plotting(monthly_list, '/timelag_monthly_(baseline_creation_date).pdf')

