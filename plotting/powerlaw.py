'''
Created on 18 Jul 2016

@author: sennikta
'''
# TODO: write try-catch for files reading
# TODO: Think about the distribution (how to show)

import json
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats._continuous_distns import powerlaw
import seaborn as sns
import scipy.stats as stats

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')
powerlaw_dir = os.path.join(plots_dir, 'powerlaw')
views_dir = os.path.join(data_dir, 'views')
scientists_dir = os.path.join(views_dir, 'scientists')

def load_simple_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    


def plotting(array, name):
    plt.title("Attention distribution")
    plt.xlabel("# of scientists")
    plt.ylabel("attention")
    x = list(range(len(array)))
    print stats.normaltest(array)
    #plt.loglog(x,array)
    plt.boxplot(array)
    #plt.scatter(x, array)
    plt.show()
    #plt.savefig(plots_dir+name)
    return

filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')    
scientist_dict = load_simple_json(filename)

data_list = []
attention_value = 0
attention_list = []
for scientist in scientist_dict:
    #print scientist
    scientist = scientist.rstrip().split('/')[-1]
    txtname = os.path.join(scientists_dir + '\\' + scientist + '.txt')   
    f = open(txtname)
    for line in f:
        #line = line.replace(',', ', ')
        time_list = map(int, line.split(','))
        time_list.pop(0)
        attention_value += sum(time_list)
    f.close()
    attention_list.append(attention_value)

plotting(attention_list, '/powerlaw_baseline.pdf')