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
import urllib2
import urllib
from os import listdir


base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
neighbors_dir = os.path.join(data_dir, 'neighbors')

plots_dir = os.path.join(data_dir, 'plots')
trends_dir = os.path.join(plots_dir, 'trends')


google_trends_dir = os.path.join(data_dir, 'google_trends_normed_by_baseline')
topics_dir = os.path.join(google_trends_dir, 'topics')
topics_cut_dir = os.path.join(google_trends_dir, 'topics_after_the_award')

scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 
topic_file =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json') 

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def days_between(d1, d2):
    return (d2 - d1).days

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def time_aligning(scientist_dict, topic_dict):
    name_list=[]
    error_list = []
    files_list = listdir(topics_dir)
    for fname in files_list:
        name = fname.replace('.csv','')
        name = name.lower()
        name_list.append(name)
    count = 0 
    for scientist, param_dict in scientist_dict.iteritems():
        
        print count
        count +=1
        event = param_dict["Award_date"].rstrip().split('T')[0]
        event_date = datetime.datetime.strptime(event, "%Y-%m-%d")
        if scientist in topic_dict:
            
            for topic in topic_dict[scientist]:
                ts_list = []
                #topic = topic.encode("utf-8")
                #topic = urllib2.unquote(topic).decode("utf-8")
                
                topic = urllib.quote_plus(topic.encode("utf-8"))
                topic=topic.replace('+', '_')
                
                topic = topic.replace('%28', '(')
                topic = topic.replace('%29', ')')
                topic = topic.replace('%2C', ',')
                topic = topic.lower()
               # topic = topic.replace('%2C', ',')
               # topic = topic.replace('%27', '\'')
               # print topic
                x = []
                y = []
                days_check = []
                    
                if topic in name_list:
                    
                    idx=name_list.index(topic)
                    csvname = os.path.join(topics_dir + '\\' + files_list[idx])
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
                        name = scientist.rstrip().split('/')[-1]+"_"+topic+".txt"
                        output_path =  os.path.join(topics_cut_dir, name)
                        text_file = open(output_path, "w")
                        #print y
                        for i in range(0, len(x)):
                            if x[i]>0:
                                ts_list.append(y[i])
                        #print ts_list
                        text_file.write(",".join(map(lambda x: str(x), ts_list)))
                        text_file.close()                    
                    except IOError:
                        #print "not found: ", topic
                        continue
                else:
                    error_list.append(topic)
    print set(error_list)
    return

scientist_dict = load_simple_json(scientists_file)
topic_dict = load_simple_json(topic_file)

time_aligning(scientist_dict, topic_dict)