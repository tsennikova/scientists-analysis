'''
Created on Aug 24, 2016

@author: Tania
'''
import json
import os
from os import listdir
import numpy as np
import csv
from itertools import islice
import pandas as pd
from scipy.sparse import lil_matrix
import itertools
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import pairwise_distances


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------- Define directories ---------------------- Define directories ---------------- Define directories --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
general_dir = os.path.join(data_dir, 'general')


# SAX
sax_dir = os.path.join(data_dir, 'sax_representation')
views_sax = os.path.join(sax_dir, 'views')
edits_sax = os.path.join(sax_dir, 'edits')
google_trends_sax = os.path.join(sax_dir, 'google_trends')
test_sax = os.path.join(sax_dir, 'test')

# scientists or topics
views_sax_sci = os.path.join(views_sax, 'scientists')
edits_sax_sci = os.path.join(edits_sax, 'scientists')
gooogle_trends_sax_sci = os.path.join(google_trends_sax, 'scientists')

views_sax_topic = os.path.join(views_sax, 'topics')
edits_sax_topic = os.path.join(edits_sax, 'topics')
gooogle_trends_sax_topic = os.path.join(google_trends_sax, 'topics')

# for output
clustering_dir =os.path.join(data_dir, 'clustering')
bop_dir = os.path.join(clustering_dir, 'bop')
seed_bop_dir = os.path.join(bop_dir, 'seed')

scientists_file = os.path.join(general_dir, 'seed_scientists_list.txt') 



# returns dict, where each raw is a time-series of scientist (topic) and each column is a sax - word    
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
                        #word = list(word.replace(',',''))
                        #word = map(int,word)
                        ts_list.append(word)
                except IOError:
                    print filename
                    continue
                if ts_list!=[]:
                    ts_dict.update({name:ts_list})
            else:
                print filename
    return ts_dict

sax_dict = read_sax(views_sax_sci)

#print sax_dict

#create dictionary
dictionary = []
for combination in itertools.product(xrange(1,5), repeat=12):
    dictionary.append(','.join(map(str, combination)))
print len(dictionary), type(dictionary[0])
count = 1 
ts_names=list(sax_dict.keys())
print ts_names
BOP = lil_matrix((len(ts_names), len(dictionary)), dtype=np.int8)
for name, ts in sax_dict.iteritems():
    print count
    column_index = ts_names.index(name) 
    for word in ts:
        row_index = dictionary.index(word)
        BOP[column_index, row_index]+=1
    count +=1

print "finished BOP formation"

# perform clustering
kmeans_model = KMeans(n_clusters=2, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '2 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("2_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()


kmeans_model = KMeans(n_clusters=3, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '3 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("3_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()


kmeans_model = KMeans(n_clusters=4, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '4 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("4_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()
    



kmeans_model = KMeans(n_clusters=5, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '5 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("5_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()


kmeans_model = KMeans(n_clusters=6, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '6 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("6_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()


kmeans_model = KMeans(n_clusters=7, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '7 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("7_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()


kmeans_model = KMeans(n_clusters=8, random_state=1).fit(BOP.tocsr())
labels = kmeans_model.labels_
print '8 clusters: ', metrics.silhouette_score(BOP.tocsr(), labels, metric='euclidean')
text_file = open("8_clust.txt", "w")
for (row, label) in enumerate(labels):
    text_file.write(ts_names[row], label)
text_file.close()



# labeler = KMeans(n_clusters=5)
# labeler.fit(BOP.tocsr()) 

# print cluster assignments for each row

#for (row, label) in enumerate(labels):
#    print ts_names[row], label


bop_matrix = np.asarray(BOP.toarray())
output_path =  os.path.join(seed_bop_dir, 'views_seed.csv')
np.savetxt(output_path, bop_matrix, delimiter=",", header=str(ts_names).replace('\'','').strip('[]'))
          
