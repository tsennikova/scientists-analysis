'''
Created on 2 Aug 2016

@author: sennikta
'''

#TODO play around with the normalization - each ts separately, or all together

# Input:
#    data              is the raw time series. 
#    N                 is the length of sliding window (use the length of the raw time series
#                      instead if you don't want to have sliding windows)
#    n                 is the number of symbols in the low dimensional approximation of the sub sequence. (Size of the word to produce)
#    alphabet_size     is the number of discrete symbols. 2 <= alphabet_size <= 20, although 
#                      alphabet_size = 2 is a special "useless" case.
# 
# Output:
#    symbolic_data:    matrix of symbolic data (no-repetition).  If consecutive subsequences
#                      have the same string, then only the first occurrence is recorded, with
#                      a pointer to its location stored in "pointers"
#    pointers:         location of the first occurrences of the strings
# 
#  The variable "win_size" is assigned to N/n, this is the number of data points on the raw 
#  time series that will be mapped to a single symbol, and can be imagined as the 
#  "compression rate".
#
# The symbolic data is returned in "symbolic_data", with pointers to the subsequences  

import json
import os
from os import listdir
import numpy
import csv
from itertools import islice
import pandas as pd
import datetime
import time

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------- Define directories ---------------------- Define directories ---------------- Define directories --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 

# for topics change seed/baseline
topic_file =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json') 

# views, edits or google trends
views_dir = os.path.join(data_dir, 'views')
edits_dir = os.path.join(data_dir, 'edits')
google_trends_dir = os.path.join(data_dir, 'google_trends')
test_dir = os.path.join(data_dir, 'test')

# scientists or topics
views_sci = os.path.join(views_dir, 'scientists')
edits_sci = os.path.join(edits_dir, 'scientists')
gooogle_trends_sci = os.path.join(google_trends_dir, 'scientists')

views_topic = os.path.join(views_dir, 'topics')
edits_topic = os.path.join(edits_dir, 'topics')
gooogle_trends_topic = os.path.join(google_trends_dir, 'topics')

# for output
sax_dir = os.path.join(data_dir, 'sax_representation')
views_sax = os.path.join(sax_dir, 'views')
edits_sax = os.path.join(sax_dir, 'edits')
google_trends_sax = os.path.join(sax_dir, 'google_trends')
test_sax = os.path.join(sax_dir, 'test')

# scientists or topics
views_sax_sci = os.path.join(views_sax, 'scientists')
edits_sax_sci = os.path.join(edits_sax, 'scientists')
gooogle_trends_sax_sci = os.path.join(google_trends_sax, 'scientists')

views_sax_topic = os.path.join(views_sax, 'topics')
edits_sax_topic = os.path.join(edits_sax, 'topics')
gooogle_trends_sax_topic = os.path.join(google_trends_sax, 'topics')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)

def output_txt(symbolic_data, file_name):
    output_path =  os.path.join(views_sax_sci, file_name)
    text_file = open(output_path, "w")
    for string in symbolic_data:
        text_file.write(",".join(map(lambda x: str(x), string)))
        text_file.write("\n")
    text_file.close()  
    symbolic_data = [] 
    return

    
def map_to_string(PAA, alphabet_size):
    string = numpy.zeros(shape=(1,len(PAA)))
    switcher = {
                2:[-numpy.inf, 0],
                3:[-numpy.inf, -0.43, 0.43],
                4:[-numpy.inf, -0.67, 0, 0.67],
                5:[-numpy.inf, -0.84, -0.25, 0.25, 0.84],
                6:[-numpy.inf, -0.97, -0.43, 0, 0.43, 0.97],
                7:[-numpy.inf, -1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
                8:[-numpy.inf, -1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
                9:[-numpy.inf, -1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
                10:[-numpy.inf, -1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28]
                }
    for i in range(0, len(PAA)):
        cut_points = []
        for s in switcher.get(alphabet_size):
            if s<=PAA[i]:
                cut_points.append(1)
            else:
                cut_points.append(0)
        string[0][i] = sum(cut_points)
    #print 'SAX: ', string
    return string

def series_to_sax(data, N, n, alphabet_size):
    if alphabet_size > 10:
        print 'Currently alphabet_size cannot be larger than 10.  Please update the breakpoint table if you wish to do so'
        return
    #Z normalize entire data
    data = (data - numpy.mean(data))/numpy.std(data)
    # win_size is the number of data points on the raw time series that will be mapped to a single symbol
    win_size = int(N/n)      
    #symbolic_data = numpy.zeros(shape=(1,n))
    symbolic_data = [0]
    PAA = []
    PAA = numpy.array(PAA)
    # Scan across the time series extract sub sequences, and converting them to strings.
    for i in range (0, (len(data) - N+1)):
    
        #Remove the current subsection
        sub_section = data[i:i+N]
        zero_array = [0]*len(sub_section)
        #Z normalize subsequence
#         if sub_section!= zero_array:
#             sub_section = (sub_section - numpy.mean(sub_section))/numpy.std(sub_section)
#         else:

#        if sub_section == list(zero_array):
#            sub_section =[-numpy.inf]*len(sub_section)
        # take care of the special case where there is no dimensionality reduction
        if N == n:
            PAA = sub_section
       
        # convert to PAA
        else:
            #N is not dividable by n
            if float(N)/n!=round(N/n):
                temp = numpy.zeros(shape=(n,N))
                for j in range(0,n):
                    temp[j,:] = sub_section
                expanded_sub_section = numpy.reshape(temp,(1, N*n), order='F')
                PAA = numpy.mean(numpy.reshape(expanded_sub_section, (N, n),order='F'), 0)
            # N is dividable by n
            else:                                  
                PAA =numpy.mean(numpy.reshape(sub_section, (win_size,n), order='F'), 0)
        #print 'PAA: ', PAA
        current_string = list(map_to_string(PAA,alphabet_size)[0])
        current_string = map(int, current_string)
        if current_string!=symbolic_data[-1]:
            symbolic_data.append(current_string)
    symbolic_data.pop(0)
    return symbolic_data

def get_series_from_txt(scientist, dir):
    scientist_series = []
    scientist = scientist.rstrip().split('/')[-1]
    filename = os.path.join(dir + '\\' + scientist + '.txt')
    try:
        f = open(filename)
        for line in f:
            time_list = map(float, line.split(','))
            year = int(time_list.pop(0))
            if  year>2004 and year<2016:
                scientist_series += time_list 
        f.close()
    except IOError:
        return []
#    print scientist_series
    return scientist_series

def get_series_from_csv(scientist, dir):
    scientist_series = []
    csvname = os.path.join(dir + '\\' + scientist + '.csv')
    try:
        f = open(csvname)
        reader = csv.reader(f)
        # skip template
        for row in islice(reader, 5, 657):
        #for row in islice(reader, 6, 30):

            year = int(row[0].rstrip().split('-')[0])
            if year>2004 and year<2016:
                scientist_series.append(float(row[1]))
        f.close()
    except IOError:
        return scientist_series
    return scientist_series


def scientists_collection(dir):
    files_list = listdir(dir)
    for scientist in files_list:
        print scientist
        scientist = scientist.replace('.txt','')
        # for Google Trends
        #scientist_series = get_series_from_csv(scientist, dir)
        # For views and edits
        scientist_series = get_series_from_txt(scientist, dir)
        symbolic_data = series_to_sax(scientist_series, 960, 9, 4)
        file_name = scientist.rstrip().split('/')[-1]+'.txt'
        output_txt(symbolic_data, file_name)
    #    series_to_sax([1,2,3,4,5,6,7,8], 8, 4, 3)
    return

def topics_collection(dir):
    files_list = listdir(dir)
    for topic in files_list: 
#         topic=topic.replace(' ', '_')
#         topic = topic[0].upper() + topic[1:]
        topic = topic.replace('.txt','')
        print topic
        # For Google Trends
        #topic_series = get_series_from_csv(topic, dir)
        # For views and edits
        topic_series = get_series_from_txt(topic, dir)
        symbolic_data = series_to_sax(topic_series, 90, 9, 4)
        file_name = topic+'.txt'            
        output_txt(symbolic_data, file_name)
    #    series_to_sax([1,2,3,4,5,6,7,8], 8, 4, 3)
    return

scientists_collection(views_sci)
