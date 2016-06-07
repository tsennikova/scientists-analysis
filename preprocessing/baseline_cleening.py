'''
Created on 7 Jun 2016

@author: sennikta
'''

import csv
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

seed_path = os.path.join(seed_dir, 'seed_data_with_the_research_field.csv')
baseline_path = os.path.join(baseline_dir, 'baseline_relevant_fields.csv')
output_path = os.path.join(baseline_dir, 'baseline_without_seed_data.csv')

f1 = file(seed_path, 'r')
f2 = file(baseline_path, 'r')
f3 = file(output_path, 'w')

c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3 = csv.writer(f3)

masterlist = list(c1)

for hosts_row in c2:
    row = 1
    found = False
    for master_row in masterlist:
        results_row = hosts_row
        if hosts_row[1] == master_row[1]:
            #results_row.append('FOUND in master list (row ' + str(row) + ')')
            found = True
            break
        row = row + 1
    if not found:
#        results_row.append('NOT FOUND in master list')
        c3.writerow(results_row)

f1.close()
f2.close()
f3.close()