'''
Created on 26 Jul 2016

@author: sennikta
'''
import json
import os
import numpy
import csv
import random
from itertools import islice
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt

# TODO recollect edits for scientists, regenerate all the plots and statistics, write code for topics

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 
#scientists_file =  os.path.join(seed_dir, 'test.json') 
topic_file =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json') 

# views, edits or google trends
views_dir = os.path.join(data_dir, 'views_normalized')
edits_dir = os.path.join(data_dir, 'edits_normalized')
google_trends_dir = os.path.join(data_dir, 'google_trends_normalized')

# scientists or topics
views_sci = os.path.join(views_dir, 'scientists')
edits_sci = os.path.join(edits_dir, 'scientists')
gooogle_trends_sci = os.path.join(google_trends_dir, 'scientists')

views_topic = os.path.join(views_dir, 'topics')
edits_topic = os.path.join(edits_dir, 'topics')
gooogle_trends_topic = os.path.join(google_trends_dir, 'google_trends')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 
    
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
    
def get_google_trends_series(scientist):
    scientist_series = []   
    csvname = os.path.join(gooogle_trends_sci + '\\' + scientist + '.csv')
    try: 
        f = open(csvname, 'rb')
        reader = csv.reader(f)
        # skip template
        for row in islice(reader, 1, 653):
        #for row in islice(reader, 5, 657):
            scientist_series.append(float(row[1]))
        f.close()
    except IOError:
        return scientist_series
    return scientist_series

def get_scientist_series_from_txt(scientist_dict, dir):
    series_dict = {}
    correlation_list = []
    for scientist in scientist_dict:
        year_dict = {}
        scientist_series = []
        scientist = scientist.rstrip().split('/')[-1]
        filename = os.path.join(dir + '\\' + scientist + '.txt')
        try:
            f = open(filename)
            for line in f:
                time_list = map(float, line.split(','))
                year = int(time_list.pop(0))
                if  year>2004 and year<2016:
                    year_dict.update({year:len(time_list)}) 
                    scientist_series += time_list 
            f.close()
        except IOError:
            #    print scientist
            continue
        if year_dict!={}:
            start_year = min(list(year_dict.keys()))
            end_year = max(list(year_dict.keys()))
            d = datetime.date(start_year, 1, 1)
            # 0 = Monday, 1=Tuesday, 2=Wednesday... We use Sunday as in Google Trends csv file every week starts from Sunday
            start_point = str(start_year) + '-01-01' 
            end_point = datetime.datetime(int(end_year), 1, 1) + datetime.timedelta(year_dict[end_year]-1)
            #Generate periods
            rng = pd.date_range(start_point, end_point, freq='D')
            #print scientist, start_point, len(rng)
            ts = pd.Series(scientist_series, index=rng)
            param_ts = numpy.array(ts.asfreq('W', method='pad').values, dtype = float)
            gt_series = get_google_trends_series(scientist)
            if gt_series!=[]:
                rng = pd.date_range('2004-01-04', '2016-06-26', freq='W')
                ts = pd.Series(gt_series, index=rng)
                rng = pd.date_range(start_point, end_point, freq='W')
                gtrends_ts = numpy.array(pd.Series(ts, index=rng).values, dtype = float)
                param_ts = running_mean(param_ts, 13)
                gtrends_ts = running_mean(gtrends_ts, 13)
                #print scientist, gtrends_ts
# Plotting            
    #             plt.figure()
    #             plt.title(scientist)
    #             plt.plot(param_ts, label = 'views')
    #             plt.plot(gtrends_ts, label = 'google_trends')
    #             plt.legend(loc='upper left')
                
                param_ts = (param_ts - numpy.mean(param_ts)) / (numpy.std(param_ts)* len(param_ts))
                gtrends_ts = (gtrends_ts - numpy.mean(gtrends_ts)) /  (numpy.std(gtrends_ts) )
    #            print scientist, numpy.correlate(param_ts, gtrends_ts)[0]
                correlation_list.append(numpy.correlate(param_ts, gtrends_ts)[0])

    
    print 'average correlation', numpy.mean(numpy.absolute(correlation_list))
    print 'min correlation', format(numpy.min(numpy.absolute(correlation_list)),'f')
    print 'max correlation',format(numpy.max(numpy.absolute(correlation_list)),'f')
#    plt.show()
    return

scientist_dict = load_simple_json(scientists_file)
scientist_series = get_scientist_series_from_txt(scientist_dict, edits_sci)


# start_point = next_weekday(d, 6) 
# end_point = '2016-01-01'
# #Generate periods
# rng = pd.date_range(start_point, end_point, freq='W')
