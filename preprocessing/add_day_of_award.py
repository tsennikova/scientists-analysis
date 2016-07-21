'''
Created on Jul 20, 2016

@author: Tania
'''
import json
import os
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
general_dir = os.path.join(data_dir, 'general')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')  
scientist_dict = load_simple_json(filename)

filename =  os.path.join(general_dir, 'award_dates.csv')  
award_dates = pd.read_csv(filename)


for scientist, param_dict in scientist_dict.iteritems():
    award = param_dict["Award"]
    if award != "Turing Award":
        field = param_dict["Field"]
        year = int(param_dict["Year"])
        day = award_dates["Day"].loc[award_dates['Award'] == award][award_dates['Field'] == field][award_dates['Year'] == year]
        month = award_dates["Month"].loc[award_dates['Award'] == award][award_dates['Field'] == field][award_dates['Year'] == year]
        awarded = str(year) + "-" + str("%02d" % month.values[0]) + "-" + str("%02d" % day.values[0])
    param_dict.update({'Award_date':awarded})

output_path =  os.path.join(seed_dir, 'seed_creation_date.json')    
with open(output_path, 'w') as out:
        json.dump(scientist_dict, out, indent=4, sort_keys=True)  