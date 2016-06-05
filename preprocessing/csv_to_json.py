'''
Created on May 28, 2016

@author: Tania
'''
import csv
import json
import urllib2

csvfile = open('data/seed_data.csv', 'r')
jsonfile = open('data/seed_data.json', 'w')

fieldnames = ("Name","Wikipage","Award","Field","Year","Gender","Status")
reader = csv.DictReader(csvfile, fieldnames)
for line in reader:
    print line
    for key, value in line.iteritems():
        value = value.decode('latin-1').encode("utf-8")
        #value = urllib2.unquote(value).decode("utf-8")
        line[key]=value
    print line
    json.dump(line, jsonfile, encoding='utf-8')
    jsonfile.write('\n')