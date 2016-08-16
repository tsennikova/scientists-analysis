'''
Created on 16 Aug 2016

@author: sennikta
'''

import os
from os import listdir
import json

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
output_dir = os.path.join(data_dir, 'general')


def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)


scientists_file = os.path.join(baseline_dir, 'baseline_creation_date.json') 
scientists_dict = load_simple_json(scientists_file)

print scientists_dict
scientist_list = scientists_dict.keys()
output_path = os.path.join(output_dir, 'baseline_scientists_list.txt')

text_file = open(output_path, "w")
for scientist in scientist_list:
    text_file.write(scientist.rstrip().split('/')[-1])
    text_file.write("\n")
text_file.close()  