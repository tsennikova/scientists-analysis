'''
Created on 1 Sep 2016

@author: sennikta
'''

import numpy as np
import os
import collections
import json

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')

# for cluster input
clustering_dir = os.path.join(data_dir, 'clustering')
sax_clustering_dir = os.path.join(clustering_dir, 'sax_clustering')
clustered  = os.path.join(sax_clustering_dir, 'edits')
clustered_seed  = os.path.join(clustered, 'seed')
clustered_seed_cut  = os.path.join(clustered_seed, 'cut')
clustered_baseline  = os.path.join(clustered, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)


filename =  os.path.join(clustered_seed, '1-cluster-cut.txt')  
with open(filename) as f:
    x_1 = f.read().splitlines()
f.close()


filename =  os.path.join(clustered_seed, '2-cluster-cut.txt')  
with open(filename) as f:
    x_2 = f.read().splitlines()
f.close()


# filename =  os.path.join(clustered_seed, '3-cluster.txt')  
# with open(filename) as f:
#     x_3 = f.read().splitlines()
# f.close()

scientist_dict = load_simple_json(scientists_file)

award_year_list = []
award_list = []
field_list = []
gender_list = []
status_list = []
for scientist in scientist_dict:
    scientist_name = scientist.rstrip().split('/')[-1]
    if scientist_name in x_2:
        award_year_list.append(scientist_dict[scientist]['Year'])
        award_list.append(scientist_dict[scientist]['Award'])
        field_list.append(scientist_dict[scientist]['Field'])
        gender_list.append(scientist_dict[scientist]['Gender'])
        status_list.append(scientist_dict[scientist]['Status'])


counter=collections.Counter(award_year_list)
print(counter)

counter=collections.Counter(award_list)
print(counter)

counter=collections.Counter(field_list)
print(counter)

counter=collections.Counter(gender_list)
print(counter)

counter=collections.Counter(status_list)
print(counter)