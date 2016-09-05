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

# The result of the plotting is not readable

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')
general_trends = os.path.join(plots_dir, 'general_trends')
plots_dir = os.path.join(plots_dir, 'trends')

# Change address for each dataset: views, edits, google_trends
norm_dir = os.path.join(data_dir, 'views')
norm_scientist_dir = os.path.join(norm_dir, 'scientists')

# for cluster input
clustering_dir = os.path.join(data_dir, 'clustering')
sax_clustering_dir = os.path.join(clustering_dir, 'sax_clustering')
clustered_views  = os.path.join(sax_clustering_dir, 'views')
clustered_views_seed  = os.path.join(clustered_views, 'seed')
clustered_views_baseline  = os.path.join(clustered_views, 'baseline')
# for plotting
data_for_plotting  = os.path.join(clustered_views_seed, 'data_for_plotting')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def days_between(d1, d2):
    return (d2 - d1).days

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def time_aligning(scientist_dict, norm_dir):
    ts_list = []
    time_list = []
    for scientist, param_dict in scientist_dict.iteritems():
        time_dict = {}
        x = []
        y = []
        days_check = []
        # comment for baseline
#        event_date = datetime.datetime.strptime(param_dict["Award_date"], "%Y-%m-%d")
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(norm_scientist_dir + '\\' + scientist + '.txt')      
        f = open(txtname)
        # converting string to dates
        for line in f:
            day_list = line.rstrip().split(',')
            year = day_list.pop(0)
            for idx,day in enumerate(day_list):
                # comment for baseline
#                date = datetime.datetime(int(year), 1, 1) + datetime.timedelta(idx+1)
                
#                days_difference = days_between(event_date, date)
#                days_check.append(date)
#                x.append(days_difference)
                y.append(day)     
        f.close()
 
        x = list(range(len(y))) # only for baseline
        x = np.array(x, dtype=np.int)
        y = np.array(y, dtype=np.float)
        time_list.append(x)
        ts_list.append(y)
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

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

filename =  os.path.join(clustered_views_seed, '1-cluster-cut.txt')  
with open(filename) as f:
    cluster_list = f.read().splitlines()

cluster_dict = {}   
for scientist, param_list in scientist_dict.iteritems():
    scientist = scientist.rstrip().split('/')[-1]
    if scientist in cluster_list:
        cluster_dict.update({scientist:param_list})


ts_list, time_list = time_aligning(cluster_dict, norm_dir)
avg_dict=take_average(ts_list, time_list)

x=[]
y=[]
sorted_dict=sorted(avg_dict.items(), key=operator.itemgetter(0))
for item in sorted_dict:
    x.append(item[0])
    y.append(item[1])
    

#plt.savefig(plots_dir+'\\'+'cluster_1_views.pdf')

filename =  os.path.join(data_for_plotting, '1-cluster-cut_x.txt')  

text_file = open(filename, "w")
for item in x:
    text_file.write("%s\n" % item)
text_file.close()

filename =  os.path.join(data_for_plotting, '1-cluster-cut_y.txt')  

text_file = open(filename, "w")
for item in y:
    text_file.write("%s\n" % item)
text_file.close()


plt.xlabel('days')
plt.ylabel('attention (views)')
plt.title('Trend inside cluster 1 (seed)')
 
x = running_mean(x, 90)
y = running_mean(y, 90)
plt.plot(x, y)

plt.savefig(plots_dir+'\\'+'cluster_1_cut_views_seed.pdf')
