'''
Created on 15 Aug 2016

@author: sennikta
'''
import os
from os import listdir
import numpy
import json
import operator
from itertools import islice
import math
import dis

# TODO: go through the articles again, figure out algorithm, write comments

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
    list_of_lists = []
    files_list = listdir(dir)
    with open(scientists_file) as f:
        name_list = f.read().splitlines()
        # read only SAX representation of seed or baseline data
        for filename in name_list:
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
                    list_of_lists.append(ts_list)
            else:
                print filename
    return list_of_lists

# Bounds
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
           
    sorted_shapelets = sorted(shapelet_dict.items(), key=operator.itemgetter(1)) 
    return sorted_shapelets

# compute the vector of distances between u-shapelet and each time series
def compute_distance(sax_list, shapelet):
    dis = [float("inf")]*len(sax_list)
    for i in range(0, len(sax_list)):
        ts = sax_list[i]
        for j in range(0, len(ts)-len(shapelet)): # every start position of ts
            #break
            #print 'SAX word', ts[j]
            #print 'Shapelet', shapelet
            d = numpy.linalg.norm(numpy.array(ts[j])-numpy.array(shapelet)) # calculate euclidian distance between u-shapelet and each SAX word of the time series
            dis[i] = min(dis[i], d) # we take min dist as a dist between u-shapelet and SAX word
        print dis[i], d
       
    norm_dis = [x / math.sqrt(len(shapelet)) for x in dis] # length normalized Euclidian distance (normalized by square root of shapelet length, optional)
    print norm_dis
    return norm_dis

def compute_gap(sax_list, shapelets):
    # bounds for scientists
    lb = int(262*0.03)
    ub = int(262*0.97)
    
  
    for i in range(0,len(shapelets)):
        curr_gap = 0 
        shapelets[i] = str(shapelets[i].replace('\'',''))
        shapelets[i] = shapelets[i].strip('[]').split(',')
        shapelets[i] = map(int,shapelets[i]) 
        dis = compute_distance(sax_list, shapelets[i])
        
        dis = sorted(dis)
        gap = 0

        print 'Computing gap'
        for i in range(lb, ub): #for each location of separation point
            d_a = [x for x in dis if x <= dis[i]] # points to the left 
            d_b = [x for x in dis if x > dis[i]] # points to the right
            
            if lb<=len(d_a)<=ub:
                mean_a = numpy.mean(numpy.array(d_a))
                mean_b = numpy.mean(numpy.array(d_b))
                std_a = numpy.std(numpy.array(d_a))
                std_b = numpy.std(numpy.array(d_b))
                print mean_a, mean_b, std_a, std_b
                curr_gap = mean_b-std_b-(mean_a+std_a)
                print curr_gap
            if curr_gap>gap:
                print 'in the if'
                gap=curr_gap
        print gap
    return gap



def get_candidate():
    
    return

sax_list = read_sax(views_sax_sci)

shapelets = []
shapelets_pairs = sort_shapelets('views_scientists_candidates.json', upper_bound_seed_sci, lower_bound_seed_sci)
for i in range(0,int(len(shapelets_pairs)*0.01)):
    shapelets.append(shapelets_pairs[i][0])
    #break
compute_gap(sax_list, shapelets)

    
# for name in name_list:
#     filename = os.path.join(views_sax_sci + '\\' + topic + '.txt')

#get_candidate(scientists_file, shapelets)
