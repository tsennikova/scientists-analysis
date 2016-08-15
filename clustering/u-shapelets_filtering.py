'''
Created on 15 Aug 2016

@author: sennikta
'''
import os
from os import listdir
import numpy
import json
import operator

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# u-shapelets folders
clustering_dir =os.path.join(data_dir, 'clustering')
u_shapelets_dir = os.path.join(clustering_dir, 'u-shapelets_candidates')
u_shapelets_seed = os.path.join(u_shapelets_dir, 'seed')
u_shapelets_baseline = os.path.join(u_shapelets_dir, 'baseline')


def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)

# Bounds
lower_bound_seed_sci = 262*0.1
upper_bound_seed_sci = 262*0.9

lower_bound_baseline_sci = 276*0.1
upper_bound_baseline_sci = 276*0.9

lower_bound_seed_topic = 1912*0.1
upper_bound_seed_topic = 1912*0.9

lower_bound_baseline_topic = 1071*0.1
upper_bound_basleine_topic = 1071*0.9

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

def compute_gap():
    return

sort_shapelets('views_scientists_candidates.json', upper_bound_seed_sci, lower_bound_seed_sci)
