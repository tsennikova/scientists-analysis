'''
Created on 15 Aug 2016

@author: sennikta
'''
import os
from os import listdir
import numpy
import json
import operator
from operator import itemgetter 
from itertools import islice
import math
import dis
from itertools import islice

# TODO: recursion does not work, something wrong with clustering_result

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
general_dir = os.path.join(data_dir, 'general')

# u-shapelets folders
clustering_dir =os.path.join(data_dir, 'clustering')
u_shapelets_dir = os.path.join(clustering_dir, 'u-shapelets_candidates')
u_shapelets_seed = os.path.join(u_shapelets_dir, 'seed')
u_shapelets_baseline = os.path.join(u_shapelets_dir, 'baseline')

# SAX folders
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

# lists of topics and scientists change seed/baseline
scientists_file = os.path.join(general_dir, 'seed_scientists_list.txt') 
topic_file = os.path.join(general_dir, 'seed_topics_list.txt') 


def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
# returns list of list, where each raw is a time-series of scientist (topic) and each column is a sax - word    
def read_sax (dir):
    ts_dict = {}
    files_list = listdir(dir)
    with open(scientists_file) as f:
        name_list = f.read().splitlines()
        # read only SAX representation of seed or baseline data
        for filename in name_list:
            name = filename
            filename = filename + '.txt'
            if filename in files_list:
                ts_list = []
                temp_list = []
                try:
                    with open(dir+'\\'+filename) as f:
                        temp_list = f.read().splitlines()
                    temp_list = list(set(temp_list))
                    for word in temp_list: 
                        word = list(word.replace(',',''))
                        word = map(int,word)
                        ts_list.append(word)
                except IOError:
                    print filename
                    continue
                if ts_list!=[]:
                    ts_dict.update({name:ts_list})
            else:
                print filename
    return ts_dict

# Bounds change back!!
lower_bound_seed_sci = 262*0.1
upper_bound_seed_sci = 262*0.9

lower_bound_baseline_sci = 276*0.1
upper_bound_baseline_sci = 276*0.9

lower_bound_seed_topic = 1912*0.1
upper_bound_seed_topic = 1912*0.9

lower_bound_baseline_topic = 1071*0.1
upper_bound_basleine_topic = 1071*0.9

# sorts shapelet candidates based on its random masking variance, exclude outliers 
def sort_shapelets(filename, upper_bound, lower_bound):
    u_shapelets_file =  os.path.join(u_shapelets_seed, filename) 
    u_shapelets_dict = load_simple_json(u_shapelets_file)
    shapelet_dict = {}
    
    for shapelet, masks in u_shapelets_dict.iteritems():
        shapelet_mean = numpy.mean(numpy.array(masks))
        if shapelet_mean<upper_bound and shapelet_mean>lower_bound:
            #print shapelet, masks, numpy.var(numpy.array(masks))
            shapelet_dict.update({shapelet:numpy.var(numpy.array(masks))})
           
    sorted_shapelets = sorted(shapelet_dict.items(), key=operator.itemgetter(1)) # sort by values
    return sorted_shapelets

# compute the vector of distances between u-shapelet and each time series
def compute_distance(sax_dict, shapelet):
    dis = [float("inf")]*len(sax_dict)
    dis_dict = {}
    i=-1
    for name in sax_dict:
        i+=1
        
        ts = sax_dict[name]
        for j in range(0, len(ts)-len(shapelet)): # every start position of ts
            d = numpy.linalg.norm(numpy.array(ts[j])-numpy.array(shapelet)) # calculate euclidian distance between u-shapelet and each SAX word of the time series
            dis[i] = min(dis[i], d) # we take min dist as a dist between u-shapelet and SAX word    
        dis_dict.update({name:dis[i]/ math.sqrt(len(shapelet))}) 
    #norm_dis = [x / math.sqrt(len(shapelet)) for x in dis] # length normalized Euclidian distance (normalized by square root of shapelet length, optional)
    return dis_dict

def compute_gap(sax_dict, shapelet, lb, ub):
    ts_dict = {}
    names = []
    dis = []
    dis_dict = compute_distance(sax_dict, shapelet) 
    dis_list = sorted(dis_dict.items(), key=operator.itemgetter(1)) 
    for item in dis_list:
        names.append(item[0])
        dis.append(item[1])
    gap = 0
    curr_gap = 0
    cluster = []
    for j in range(lb, ub): #for each location of separation point
        d_a = [x for x in dis if x <= dis[j]] # points to the left 
        a_ind = [ind for ind,v in enumerate(dis) if v <= dis[j]]
        cluster_a = itemgetter(*a_ind)(names)
        d_b = [x for x in dis if x > dis[j]] # points to the right

        if lb<=len(d_a)<=ub:
            mean_a = numpy.mean(numpy.array(d_a))
            mean_b = numpy.mean(numpy.array(d_b))
            std_a = numpy.std(numpy.array(d_a))
            std_b = numpy.std(numpy.array(d_b))
            curr_gap = mean_b-std_b-(mean_a+std_a)
        if curr_gap>gap:
            gap=curr_gap
            cluster = cluster_a
    return gap, cluster

def clustering(sax_dict, shapelets, gap_dict, iter, clustering_result):
    print 'in the clustering function'
    # bounds for scientists
    cluster_list = []
    gap_list = []
#    lb = int(262*0.03)
#    ub = int(262*0.97)
    lb = int(262*0.03)
    ub = int(262*0.4)

    candidate_dict = {}
    sorted_candidate_dict = {}

    for i in range(0,len(shapelets)):
        curr_gap = 0 
        if iter == 0:
            shapelets[i] = str(shapelets[i].replace('\'',''))
            shapelets[i] = shapelets[i].strip('[]').split(',')
            shapelets[i] = map(int,shapelets[i]) 
        gap, cluster = compute_gap(sax_dict, shapelets[i], lb, ub)
        gap_list.append(gap)
        cluster_list.append(cluster)
    index, max_gap = max(enumerate(gap_list), key=operator.itemgetter(1)) # find max gap and its index
    print 'current gap', max_gap
    if gap_dict!={}:
        print 'first gap', gap_dict.get(0)
        if max_gap < gap_dict.get(0)/3:
            return clustering_result
        else: 
            d_a = list(cluster_list[index])
            candidate = shapelets[index]
            # remove cluster from the rest of the data
            for ts in d_a:
                sax_dict.pop(ts, None)
            # remove shapelets candidate from the list of shapelets
            shapelets.remove(candidate)
            clustering_result.update({iter:d_a})
            gap_dict.update({iter:max_gap})
            iter+=1
            if len(sax_dict)>=lb:
                print clustering_result
                return clustering(sax_dict, shapelets, gap_dict, iter, clustering_result)
            else:
                return clustering_result
    else:
        d_a = list(cluster_list[index])
        candidate = shapelets[index]
        # remove cluster from the rest of the data
        for ts in d_a:
            sax_dict.pop(ts, None)
        # remove shapelets candidate from the list of shapelets
        shapelets.remove(candidate)
        clustering_result.update({iter:d_a})
        gap_dict.update({iter:max_gap})
        iter+=1
        # HERE SOMETHING WRONG WITH THE DATATYPES
        if len(sax_dict)>=lb:
            print clustering_result
            return clustering(sax_dict, shapelets, gap_dict, iter, clustering_result)
        else:
            return clustering_result


sax_dict = read_sax(views_sax_sci)
shapelets = []
shapelets_pairs = sort_shapelets('views_scientists_candidates.json', upper_bound_seed_sci, lower_bound_seed_sci)
for i in range(0,int(len(shapelets_pairs)*0.01)):
    shapelets.append(shapelets_pairs[i][0])
    #break
cluster_list = clustering(sax_dict, shapelets, {}, 0, {})
print cluster_list
    
# for name in name_list:
#     filename = os.path.join(views_sax_sci + '\\' + topic + '.txt')

#get_candidate(scientists_file, shapelets)
