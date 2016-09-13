'''
Created on 19 Jul 2016

@author: sennikta
'''
import json
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import operator
import csv
from itertools import islice


# The result of the plotting is not readable

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')


# Change address for each dataset: views, edits, google_trends
norm_dir = os.path.join(data_dir, 'google_trends_normalized')
norm_scientist_dir = os.path.join(norm_dir, 'scientists')

# for cluster input
clustering_dir = os.path.join(data_dir, 'clustering')
sax_clustering_dir = os.path.join(clustering_dir, 'sax_clustering')
clustered_gt  = os.path.join(sax_clustering_dir, 'google_trends')

clustered_gt_seed  = os.path.join(clustered_gt, 'seed')
clustered_gt_baseline  = os.path.join(clustered_gt, 'baseline')

# for plotting
clustered_gt_plots  = os.path.join(clustered_gt, 'plots')
data_for_plotting  = os.path.join(clustered_gt_baseline, 'data_for_plotting')



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
    ts_list = []
    time_list = []
    for scientist, param_dict in scientist_dict.iteritems():
        time_dict = {}
        x = []
        y = []
        days_check = []
        # comment for baseline
        #event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        
        scientist = scientist.rstrip().split('/')[-1]
        csvname = os.path.join(norm_scientist_dir + '\\' + scientist + '.csv')      
        try:
            f = open(csvname)
            reader = csv.reader(f)
            for row in islice(reader, 1, 653):
                year = int(row[2].rstrip().split('-')[0])
                if year>2004 and year<2016:
                    y.append(float(row[1]))
                    week_beg = datetime.datetime.strptime(row[2].rstrip().split(' - ')[0], "%Y-%m-%d")
                    week_end = datetime.datetime.strptime(row[2].rstrip().split(' - ')[1], "%Y-%m-%d")
                    #if event_date>week_beg and event_date<week_end:
                    #    ind=len(y)-1
            f.close()
            for i in range(0,len(y)):
                # comment for baseline
#                x.append(i-ind)
                x.append(i)
            #x = running_mean(x, 13)
            #y = running_mean(y, 13)
            ts_list.append(y)
            time_list.append(x)
        except IOError:
            continue
        #print ts_list
    return list(ts_list), list(time_list)


def take_average(ts_list, time_list):
    # make dict
    ts_dict = {}
    avg_dict = {}
    for i in range(0, len(time_list)):
        for day in time_list[i]:
            if day in ts_dict:
                temp_list=ts_dict[day]
                index = list(time_list[i]).index(day)
                ts_dict[day].append(ts_list[i][index])
            else:
                #print day
                #print time_list
                index = list(time_list[i]).index(day)
                ts_dict.update({day:[ts_list[i][index]]})
   
    for day in ts_dict:
        avg = np.median(np.array(ts_dict[day]))
        #avg=sum(ts_dict[day]) / float(len(ts_dict[day]))
        avg_dict.update({day:avg})    
    return avg_dict

filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')  
scientist_dict = load_simple_json(filename)

filename =  os.path.join(clustered_gt_baseline, '1-cluster.txt')  
with open(filename) as f:
    cluster_list = f.read().splitlines()

cluster_dict = {}   
for scientist, param_list in scientist_dict.iteritems():
    scientist = scientist.rstrip().split('/')[-1]
    if scientist in cluster_list:
        cluster_dict.update({scientist:param_list})


ts_list, time_list = time_aligning(cluster_dict)
avg_dict=take_average(ts_list, time_list)

x=[]
y=[]
sorted_dict=sorted(avg_dict.items(), key=operator.itemgetter(0))
for item in sorted_dict:
    x.append(item[0])
    y.append(item[1])
    

#plt.savefig(plots_dir+'\\'+'cluster_1_views.pdf')

filename =  os.path.join(data_for_plotting, '1-cluster_x.txt')  

text_file = open(filename, "w")
for item in x:
    text_file.write("%s\n" % item)
text_file.close()

filename =  os.path.join(data_for_plotting, '1-cluster_y.txt')  

text_file = open(filename, "w")
for item in y:
    text_file.write("%s\n" % item)
text_file.close()


plt.xlabel('days before the award')
plt.ylabel('attention (google trends)')
plt.title('Trend inside cluster 1 (baseline)')
 
x = running_mean(x, 6)
y = running_mean(y, 6)
plt.plot(x, y)

plt.savefig(clustered_gt_plots+'\\'+'cluster_1_google_trends_baseline.pdf')
