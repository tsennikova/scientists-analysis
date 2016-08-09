'''
Created on 9 Aug 2016

@author: sennikta
'''

# TODO: remove candidate from the list

import os
from os import listdir
import numpy
import json
import random

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

# scientists or topics
views_sax_sci = os.path.join(views_sax, 'scientists')
edits_sax_sci = os.path.join(edits_sax, 'scientists')
gooogle_trends_sax_sci = os.path.join(google_trends_sax, 'scientists')

views_sax_topic = os.path.join(views_sax, 'topics')
edits_sax_topic = os.path.join(edits_sax, 'topics')
gooogle_trends_sax_topic = os.path.join(google_trends_sax, 'topics')

def read_sax (dir):
    list_of_lists = []
    files_list = listdir(dir)
    for name in files_list:
        sax_list = []
        with open(dir + '/' + name) as f:
            sax_list = f.read().splitlines()
        sax_list = set(sax_list)
        list_of_lists.append(sax_list)
    return list_of_lists

def random_masking(sax_list):
    print 'in random masking function'
    R = 10
    maskedNum = 3
    candidate_dict = {}
    masked_list = []
    for i in range (0,R):
        stop_list = []
        mask_ind = random.sample(range(0, 8), 3)
        masked_dict = {}
        print 'started random masking'
        
        # apply mask to the list of time series
        for time_series in sax_list:
            masked_time_series = []
            for word in time_series:  
                masked_word = list(word.replace(',',''))
                for l in sorted(mask_ind, reverse=True):
                    del masked_word[l]
                masked_time_series.append(masked_word)
            masked_list.append(masked_time_series)

        print 'counting frequency'
        for time_series in sax_list:
            for candidate in time_series:
                if  candidate not in stop_list:
                    masked_candidate = list(candidate.replace(',',''))
                    sum = 0
                    sum_list = []
                    
                    for l in sorted(mask_ind, reverse=True):
                        del masked_candidate[l]
                   
                    for masked_time_series in masked_list:
                        if masked_candidate in masked_time_series:
                            sum+=1
                            
                    candidate_dict.update({candidate:sum_list.append(sum)})
                    stop_list.append(candidate)
        #print candidate_dict
        
        print i
    #print candidate_dict
    return candidate_dict

sax_list = read_sax(views_sax_sci)
candidate_dict = random_masking(sax_list)

with open('candidate_list.json', 'w') as f:
        json.dump(candidate_dict, f, indent=4, sort_keys=True)
