'''
Created on 9 Aug 2016

@author: sennikta
'''

# TODO: continue testing on a small dataset

import os
from os import listdir
import numpy
import json
import random
from collections import defaultdict
import urllib2
import urllib
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------- Define directories ---------------------- Define directories ---------------- Define directories --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# sax representation
sax_dir = os.path.join(data_dir, 'sax_representation')
views_sax = os.path.join(sax_dir, 'views')
edits_sax = os.path.join(sax_dir, 'edits')
google_trends_sax = os.path.join(sax_dir, 'google_trends')
test_sax = os.path.join(sax_dir, 'test')

# scientists or topics
views_sax_sci = os.path.join(views_sax, 'scientists')
edits_sax_sci = os.path.join(edits_sax, 'scientists')
google_trends_sax_sci = os.path.join(google_trends_sax, 'scientists')

views_sax_topic = os.path.join(views_sax, 'topics')
edits_sax_topic = os.path.join(edits_sax, 'topics')
google_trends_sax_topic = os.path.join(google_trends_sax, 'topics')

# for scientists change seed/baseline
scientists_file = os.path.join(seed_dir, 'seed_creation_date.json') 
test_file = os.path.join(seed_dir, 'test_creation_date.json') 

# for topics change seed/baseline
topic_file =  os.path.join(neighbors_dir, 'seed-topics_list.txt') 

# for output
clustering_dir =os.path.join(data_dir, 'clustering')
u_shapelets_dir = os.path.join(clustering_dir, 'u-shapelets_candidates')
u_shapelets_seed = os.path.join(u_shapelets_dir, 'seed')
u_shapelets_baseline = os.path.join(u_shapelets_dir, 'baseline')
u_shapelets_test = os.path.join(u_shapelets_dir, 'test')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)


def read_sax (filename):
    ts_list = []
    temp_list = []
    try:
        with open(filename) as f:
            temp_list = f.read().splitlines()
        temp_list = list(set(temp_list))
        for word in temp_list: 
            word = list(word.replace(',',''))
            #word = map(int,word)
            ts_list.append(word)
    except IOError:
        print filename
        return ts_list
    return ts_list

def random_masking(sax_list):
    print 'in random masking function'
    R = 10
    maskedNum = 3
    candidate_dict = defaultdict(list)
    for i in range (0,R):
        masked_list = []
        stop_list = []
        mask_ind = random.sample(range(0, 9), 3)
        #print 'mask_ind', mask_ind
        masked_dict = {}
        print 'started random masking'
        
        # apply mask to the list of time series
        for time_series in sax_list:
            masked_time_series = []
            for word in time_series:  
                masked_word = list(word)
                
                for l in sorted(mask_ind, reverse=True):
                    del masked_word[l]
                masked_word = int(''.join(masked_word))
                
                masked_time_series.append(masked_word)
            masked_time_series = set(masked_time_series)
            masked_list.append(masked_time_series)
        #print masked_list
        
        print 'counting frequency'
        for time_series in sax_list:
            for candidate in time_series:
                if  candidate not in stop_list:
                    masked_candidate = list(candidate)
                    sum = 0
                    sum_list = []
                    
                    for l in sorted(mask_ind, reverse=True):
                        del masked_candidate[l]
                    masked_candidate = int(''.join(masked_candidate))
                
                   # Critical point                    
                    for masked_time_series in masked_list:
                        if masked_candidate in masked_time_series:
                           # print masked_candidate
                            sum+=1
                    #print candidate, sum
                    candidate_dict[str(candidate)].append(sum)
                    
                    stop_list.append(candidate)
        
        print i
    #print candidate_dict
    return candidate_dict


dir = views_sax_sci
sax_list = []


# ------------------------------- FOR TESTING  -------------------------------

# scientist_list=['1.txt','2.txt','3.txt','4.txt','5.txt']
# for scientist in scientist_list:
#     filename = os.path.join(test + "\\"+scientist)
#     ts_list=read_sax(filename)
#     sax_list.append(ts_list)
# candidate_dict = random_masking(sax_list)

#  ------------------------------- REAL CODE  -------------------------------
#for scientists
scientist_dict = load_simple_json(scientists_file)
for scientist in scientist_dict:
    scientist = scientist.rstrip().split('/')[-1]
    filename = os.path.join(dir + '\\' + scientist + '.txt')
    ts_list=read_sax(filename)
    if ts_list!=[]:
        sax_list.append(ts_list)
candidate_dict = random_masking(sax_list)
print candidate_dict
# for topics
# with open(topic_file) as f:
#     topic_list = f.read().splitlines()
#     
# for topic in topic_list:
#     topic = topic.encode("utf-8")
#     topic = urllib2.unquote(topic).decode("utf-8")
#     topic = topic.replace('+', '_')
#     topic = urllib.quote_plus(topic.encode("utf-8"))
#     topic = topic.replace('%28', '(')
#     topic = topic.replace('%29', ')')
#     topic = topic.replace('%2C', ',')
#     #topic = topic.replace('%27', '\'')
#     filename = os.path.join(dir + '\\' + topic + '.txt')
#     ts_list=read_sax(filename)
#     if ts_list!=[]:
#         sax_list.append(ts_list)
# candidate_dict = random_masking(sax_list)
#  
output_path =  os.path.join(u_shapelets_seed, 'views_scientists_candidates.json')    
with open(output_path, 'w') as out:
    json.dump(candidate_dict, out, indent=4, sort_keys=True)
