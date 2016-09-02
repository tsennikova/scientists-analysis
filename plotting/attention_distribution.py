'''
Created on 18 Jul 2016

@author: sennikta
'''

# TODO check box plot for google_trends

import json
import os
from datetime import datetime
import numpy
import matplotlib.pyplot as plt
import csv

from itertools import islice

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')
powerlaw_dir = os.path.join(plots_dir, 'attention_distribution')

# Change address for each dataset
edits_dir = os.path.join(data_dir, 'google_trends')
scientists_dir = os.path.join(edits_dir, 'scientists')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    

# Plot the frequency distribution
def plot_distribution(seed, baseline, name):
    plt.title("Attention distribution (google searches)")
    plt.xlabel("# of edits")
    plt.ylabel("probability")
    bins = range(4, 18)
    plt.xticks(bins, ["2^%s" % i for i in bins])
    plt.hist(numpy.log2(seed), log=True, normed = True, bins=bins, label = 'seed data', alpha=0.5,)
    plt.hist(numpy.log2(baseline), log=True, normed = True, bins=bins, label = 'baseline data', alpha=0.5,)
    plt.legend(loc='upper left')
    plt.savefig(powerlaw_dir+name)
    return

# Box Plot 
def box_plot(seed, baseline, name):
    data_to_plot = [seed, baseline]
    fig = plt.figure(1, figsize=(9, 4))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot, showfliers=False)
    
    plt.title("Attention distribution (google trends)")
    ax.set_xticklabels(['seed data', 'baseline'])
    plt.ylabel("# of google trends searches")
    bins = range(10, 25)
    #plt.show()
    plt.savefig(powerlaw_dir+name)
    return
    


# For views and edits
def read_txt(filename):
    scientist_dict = load_simple_json(filename)
    data_list = []
    
    attention_list = []
    for scientist in scientist_dict:
        attention_value = 0
        scientist = scientist.rstrip().split('/')[-1]
        txtname = os.path.join(scientists_dir + '\\' + scientist + '.txt')   
        try:
            f = open(txtname)
            for line in f:
                time_list = map(int, line.split(','))
                time_list.pop(0)
                attention_value += sum(time_list)
            f.close()
            attention_list.append(attention_value)
        except IOError:
            continue
    return attention_list


# For google trends
def read_csv(filename):

    scientist_dict = load_simple_json(filename)
    data_list = []

    attention_list = []
    for scientist in scientist_dict:
        attention_value = 0
        scientist = scientist.rstrip().split('/')[-1]
        csvname = os.path.join(scientists_dir + '\\' + scientist + '.csv')
        try: 
            f = open(csvname, 'rb')
            reader = csv.reader(f)
            # skip template
            for row in islice(reader, 5, 657):
                attention_value += int(row[1])
            f.close()
            print scientist, attention_value
            attention_list.append(attention_value)
        except IOError:
            attention_list.append(0)
            continue        
    #print attention_list
    return attention_list

# for views and edits
#filename =  os.path.join(seed_dir, 'seed_creation_date.json')    
#seed = read_txt(filename)
#filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')  
#baseline = read_txt(filename)

# for google trends
filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')  
baseline = read_csv(filename)
filename =  os.path.join(seed_dir, 'seed_creation_date.json')    
print "seed"
seed = read_csv(filename)

#print 'average seed', numpy.mean(numpy.absolute(seed))
#print 'min seed', format(numpy.min(numpy.absolute(seed)),'f')
#print 'max seed',format(numpy.max(numpy.absolute(seed)),'f')


#print 'average baseline', numpy.mean(numpy.absolute(baseline))
#print 'min baseline', format(numpy.min(numpy.absolute(baseline)),'f')
#print 'max baseline',format(numpy.max(numpy.absolute(baseline)),'f')

box_plot(seed, baseline, '/boxplot_google_trends_zero_values.jpg')

#plot_distribution(seed, baseline, '/loglog_google_trends.pdf')