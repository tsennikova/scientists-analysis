'''
Created on May 26, 2016

@author: Tania
'''
import pandas as pd
import csv
import random
from random import shuffle


dataset = pd.read_csv('data/seed-data.csv')
y = dataset['Wikipage']
y_list = y.tolist()

for i in range(10):
    print random.choice(y_list)

