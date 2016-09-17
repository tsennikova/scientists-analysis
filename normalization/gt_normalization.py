'''
Created on Sep 14, 2016

@author: Tania
'''
import os
from os import listdir
import calendar
import collections
import csv
import pandas as pd

from itertools import islice

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
general_dir = os.path.join(data_dir, 'general')

google_trends_dir = os.path.join(data_dir, 'google_trends')
scientists_dir = os.path.join(google_trends_dir, 'scientists')
topic_dir = os.path.join(google_trends_dir, 'topics')

scientists_seed = os.path.join(general_dir, 'seed_scientists_list.txt')
scientists_baseline = os.path.join(general_dir, 'seed_scientists_list.txt')
topic_seed = os.path.join(general_dir, 'seed_topics_list.txt')
topic_baseline = os.path.join(general_dir, 'baseline_topics_list.txt')

# for output
google_trends_dir_normed = os.path.join(data_dir, 'google_trends_normed_by_baseline')
scientists_dir_normed = os.path.join(google_trends_dir_normed, 'scientists')
topic_dir_normed = os.path.join(google_trends_dir_normed, 'topics')

topic_baseline = os.path.join(general_dir, 'baseline_topics_list.txt')


def get_baseline(dir):    
    baseline_dict = {}
    baseline = [0]*652
    counter = 0
    files_list = listdir(dir)
    with open(scientists_baseline) as f:
        name_list = f.read().splitlines()
    for filename in name_list:
        time_series = []
        name = filename
        filename = filename + '.csv'
        if filename in files_list:
            counter +=1
            csvname = os.path.join(dir + '\\' + filename)
                     
            f = open(csvname, 'rb')
            reader = csv.reader(f)
            for row in islice(reader, 5, 657):
                time_series.append(row[1])
            f.close()
            time_series = map(int, time_series)
            baseline = [x+y for x,y in zip(baseline, time_series)]
    baseline_avg = [z / counter for z in baseline]
        #baseline_dict.update({filename:time_series})
        #print len(time_series)
    return baseline_avg

def normalize(dir, baseline_avg):    
    files_list = listdir(dir)
    with open(scientists_seed) as f:
        name_list = f.read().splitlines()
    for filename in name_list:
        time_series = []
        week_intervals = []
        name = filename
        filename = filename + '.csv'
        if filename in files_list:
            csvname = os.path.join(dir + '\\' + filename)
            f = open(csvname, 'rb')
            reader = csv.reader(f)
            for row in islice(reader, 5, 657):
                time_series.append(row[1])
                week_intervals.append(row[0])
            f.close()
            time_series = map(int, time_series)
            time_series_normed = [float(x)/y for x,y in zip(time_series, baseline_avg)]
            output_path =  os.path.join(scientists_dir_normed, filename)
            #text_file = open(output_path, "w")
            #text_file.write(",".join(map(lambda x: str(x), time_series_normed)))
            #text_file.close()  
            data = pd.DataFrame({'Week':week_intervals, 'Interest':time_series_normed})
            data.to_csv(output_path, sep=',')
    return


baseline_avg = get_baseline(scientists_dir)
print baseline_avg
normalize(scientists_dir, baseline_avg)

