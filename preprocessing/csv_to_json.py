'''
Created on May 28, 2016

@author: Tania
'''
import csv
import json
import urllib2
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')

csv_path =os.path.join(seed_dir, 'seed_data.csv')
json_path =os.path.join(seed_dir, 'seed_data.json')

csvfile = open(csv_path, 'r')
jsonfile = open(json_path, 'w')

dump = {}
dump_key = ""
dump_dict = {} 
fieldnames = ("Name","Wikipage","Award","Field","Year","Gender","Status")
reader = csv.DictReader(csvfile, fieldnames)
next(reader, None)
for line in reader:
    dump_key = ""
    dump_dict = {} 
    for key, value in line.iteritems():
        value = value.decode('latin-1').encode("utf-8")
        #value = urllib2.unquote(value).decode("utf-8")
        line[key]=value
        if key == "Wikipage":
            dump_key = line[key]
        else:
            dump_dict.update({key:line[key]})
    dump.update({dump_key:dump_dict})
json.dump(dump, jsonfile, encoding='utf-8')
jsonfile.write('\n')