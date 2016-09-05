'''
Created on 30 Aug 2016

@author: sennikta
'''
import matplotlib.pyplot as plt
import numpy as np
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
plots_dir = os.path.join(data_dir, 'plots')

# for cluster input
clustering_dir = os.path.join(data_dir, 'clustering')
sax_clustering_dir = os.path.join(clustering_dir, 'sax_clustering')
clustered_views  = os.path.join(sax_clustering_dir, 'views')
clustered_views_seed  = os.path.join(clustered_views, 'seed')
clustered_views_baseline  = os.path.join(clustered_views, 'baseline')

data_for_plotting  = os.path.join(clustered_views_seed, 'data_for_plotting')

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

filename =  os.path.join(data_for_plotting, '1-cluster-cut_x.txt')  
with open(filename) as f:
    x_1 = f.read().splitlines()

x_1 = map(int, x_1)
x_1 = running_mean(x_1[:5000], 360)
f.close()

filename =  os.path.join(data_for_plotting, '1-cluster-cut_y.txt')  
with open(filename) as f:
    y_1 = f.read().splitlines()

y_1 = map(float, y_1)
y_1 = running_mean(y_1[:5000], 360)
f.close()

filename =  os.path.join(data_for_plotting, '2-cluster-cut_x.txt')  
with open(filename) as f:
    x_2 = f.read().splitlines()

x_2 = map(int, x_2)
x_2 = running_mean(x_2, 360)
f.close()


filename =  os.path.join(data_for_plotting, '2-cluster-cut_y.txt')  
with open(filename) as f:
    y_2 = f.read().splitlines()

y_2 = map(float, y_2)
y_2 = running_mean(y_2, 360)
f.close()


filename =  os.path.join(data_for_plotting, '3-cluster-cut_x.txt')  
with open(filename) as f:
    x_3 = f.read().splitlines()

x_3 = map(int, x_3)
x_3 = running_mean(x_3[:4500], 360)
f.close()


filename =  os.path.join(data_for_plotting, '3-cluster-cut_y.txt')  
with open(filename) as f:
    y_3 = f.read().splitlines()

y_3 = map(float, y_3)
y_3 = running_mean(y_3[:4500], 360)
f.close()


plt.xlabel('days')
plt.ylabel('attention (views)')
plt.title('Trend inside the clusters')
plt.plot(x_1, y_1)
plt.plot(x_2, y_2)
plt.plot(x_3, y_3)

plt.legend(['cluster 1', 'cluster 2', 'cluster 3'], loc='upper left')

#plt.show()
plt.savefig(plots_dir+'\\'+'clusters_views_cut_seed.pdf')