'''
Created on 15 Sep 2016

@author: sennikta
'''
import os
from os import listdir
import collections

# basic dir
base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
general_dir = os.path.join(data_dir, 'general')

# for input
edits_dir = os.path.join(data_dir, 'edits')
scientists_dir = os.path.join(edits_dir, 'scientists')
topic_dir = os.path.join(edits_dir, 'topics')
main_page_file = os.path.join(general_dir, 'Main_Page.txt')

# for output
edits_dir_normed = os.path.join(data_dir, 'edits_normed_by_main_page')
scientists_dir_normed = os.path.join(edits_dir_normed, 'scientists')
topic_dir_normed = os.path.join(edits_dir_normed, 'topics')

def read_main_page():
    main_page = {}
    f = open(main_page_file)
    for line in f:
        time_series = []
        time_list = []
        time_list = map(int, line.split(','))
        year = int(time_list.pop(0))
        if  year>2001 and year<2016:
            time_series += time_list
            main_page.update({year:time_series})
    return main_page

def edits_normalization(dir):
    main_page = read_main_page()
    files_list = listdir(dir)
    for name in files_list:
        time_dict = {}

        filename = os.path.join(dir + '\\' + name)
        f = open(filename)
        for line in f:
            time_series = []
            time_list = []

            time_list = map(float, line.split(','))
            year = int(time_list.pop(0))
            if  year>2001 and year<2016:
                time_series += time_list
                time_series_normed = time_series
                for denominator in main_page[year]:
                    if denominator != 0:
                        idx = main_page[year].index(denominator)
                        #print year, denominator, time_series[idx], time_series_normed[idx]

                        time_series_normed[idx] = float(time_series[idx]) / denominator
                time_series_normed = [year] +time_series_normed
                time_dict.update({year:time_series_normed})
        time_dict = collections.OrderedDict(sorted(time_dict.items()))
        output_path =  os.path.join(scientists_dir_normed, name)
        text_file = open(output_path, "w")
        for key in time_dict:
            text_file.write(",".join(map(lambda x: str(x), time_dict[key])))
            text_file.write("\n")
        text_file.close()  
        time_dict = {} 
        
        
        #text_file = open(output_path, "w")
        #text_file.write(",".join(map(lambda x: str(x), time_series_normed)))
        #text_file.close() 
    return 

edits_normalization(scientists_dir)