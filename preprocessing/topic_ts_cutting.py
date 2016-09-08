'''
Created on 8 Sep 2016

@author: sennikta
'''
import json
import os
import datetime
import numpy as np
import operator
import matplotlib.pyplot as plt
import urllib2
import urllib
from os import listdir

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
neighbors_dir = os.path.join(data_dir, 'neighbors')

# Change address for each dataset: views, edits, google_trends
views_dir = os.path.join(data_dir, 'views')
views_baseline_dir = os.path.join(views_dir, 'baseline')
views_topic_dir = os.path.join(views_dir, 'topics')
views_topic_cut_dir = os.path.join(views_baseline_dir, 'topics_after_creation')

scientists_file =  os.path.join(baseline_dir, 'baseline_creation_date.json') 
topic_file =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json') 

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def days_between(d1, d2):
    return (d2 - d1).days

def time_aligning(scientist_dict, topic_dict):
    print scientist_dict
    print topic_dict
    name_list=[]
    error_list = []
    files_list = listdir(views_topic_dir)
    for fname in files_list:
        name = fname.replace('.txt','')
        name = name.lower()
        name_list.append(name)
    count = 0 
    for scientist, param_dict in scientist_dict.iteritems():
        print count
        count +=1
        event = param_dict["Page_created"].rstrip().split('T')[0]
        event_date = datetime.datetime.strptime(event, "%Y-%m-%d")
        if scientist in topic_dict:
            for topic in topic_dict[scientist]:
                
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
                ts_list = []    
                if topic in name_list:
                    txtname = os.path.join(views_topic_dir + '\\' + fname)
                    
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
                        x = np.array(x, dtype=np.int)
                        y = np.array(y, dtype=np.float)
                        name = scientist.rstrip().split('/')[-1]+"_"+topic+".txt"
                        output_path =  os.path.join(views_topic_cut_dir, name)
                        text_file = open(output_path, "w")
                        for i in range(0, len(x)):
                            if x[i]>0:
                                ts_list.append(y[i])
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