'''
Created on 14 Oct 2016

@author: sennikta
'''

import os
from os import listdir
from shutil import copyfile

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
general_dir = os.path.join(data_dir, 'general')

dir = os.path.join(data_dir, 'views')
scientist_dir = os.path.join(dir, 'scientists')
vews_seed_dir = os.path.join(dir, 'seed')
scientist_cut_dir = os.path.join(vews_seed_dir, '3_years_before')
output_dir = os.path.join(vews_seed_dir,'3_years_before_nobel_cl')

scientists_file = os.path.join(general_dir, 'citation_scientists.txt')

with open(scientists_file) as f:
    name_list = f.read().splitlines()
    for filename in name_list:
        filename = filename + '.txt'
        copyfile(scientist_cut_dir+'\\'+filename, output_dir+'\\'+filename)
