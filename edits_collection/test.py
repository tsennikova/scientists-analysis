'''
Created on 23 Jun 2016

@author: sennikta
'''
from datetime import datetime
import collections

time_array = [0]
common_year = [31,28,31,30,31,30,31,31,30,31,30,31]
leap_year = [31,29,31,30,31,30,31,31,30,31,30,31]

timestamp_list = ["2007-12-12T03:33:39Z", "2007-12-11T14:27:53Z", "2007-12-11T01:54:10Z", "2007-12-11T01:53:11Z", "2007-12-11T01:51:18Z", "2007-12-09T23:01:03Z", "2007-12-08T21:41:43Z", 
                  "2007-12-07T17:46:06Z", "2007-11-29T04:17:19Z", "2007-11-14T03:14:38Z", "2007-10-27T19:10:43Z", "2007-10-27T19:10:37Z", "2007-10-26T10:46:36Z", "2007-10-10T22:30:41Z",
                  "2007-10-10T22:02:43Z", "2007-09-24T12:44:00Z", "2007-09-23T02:31:48Z", "2007-09-21T08:36:07Z", "2007-09-21T08:35:51Z", "2007-09-21T08:34:51Z", "2007-09-21T08:30:31Z",
                  "2007-09-21T08:29:57Z", "2007-09-21T08:28:58Z", "2007-09-21T08:28:18Z", "2007-09-21T08:27:57Z", "2007-09-12T19:16:53Z", "2007-09-08T21:54:17Z", "2007-08-17T23:35:28Z", 
                  "2007-08-17T23:28:53Z", "2007-08-15T21:32:19Z", "2007-08-08T22:20:26Z", "2007-07-25T20:05:57Z", "2007-07-20T15:56:02Z", "2007-07-20T15:55:27Z", "2007-07-10T12:35:38Z", 
                  "2007-07-05T17:28:17Z", "2007-07-05T13:58:31Z", "2007-06-25T17:47:09Z", "2007-06-23T18:27:29Z", "2007-06-23T05:41:01Z", "2007-06-18T08:30:48Z", "2007-06-18T08:27:45Z",
                  "2007-06-18T08:27:16Z", "2007-06-04T01:46:15Z", "2007-06-04T00:41:08Z", "2007-05-29T17:26:29Z", "2007-05-23T03:43:38Z", "2007-05-22T18:33:07Z", "2007-05-21T22:23:40Z",
                  "2007-05-19T15:21:48Z", "2007-05-19T08:20:08Z", "2007-05-16T19:13:59Z", "2007-04-07T07:38:38Z", "2007-03-31T09:16:12Z", "2007-03-28T22:07:08Z", "2007-03-28T22:06:49Z",
                  "2007-03-28T08:49:23Z", "2007-03-26T02:03:47Z", "2007-03-05T17:57:54Z", "2007-03-05T17:30:47Z", "2007-03-05T17:27:57Z", "2007-02-20T22:26:16Z", "2007-02-19T23:04:11Z",
                  "2007-02-11T21:29:15Z", "2007-02-10T18:52:13Z", "2007-02-08T11:08:38Z", "2007-02-07T11:17:39Z", "2007-01-30T21:21:38Z", "2007-01-28T17:32:52Z", "2007-01-28T17:32:36Z",
                  "2007-01-27T01:45:54Z", "2007-01-27T01:45:22Z", "2007-01-13T21:07:22Z", "2007-01-08T21:56:54Z"]

#timestamp_list = ["2009-07-31T08:02:37Z", "2011-02-08T02:30:48Z"]
time_dict = {}
for timestamp in timestamp_list:
    time = timestamp
    timestamp = timestamp.rstrip().split('T')[0]
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d')
    index = int(timestamp.strftime('%j'))
    
    year = int(timestamp.year)
    print time, " ", index
    if year==time_array[0]:
        time_array[index] +=1
    else:    
        
        time_array = [year]
        
        if year != 2008 and year != 2012:
            listofzeros = [0] * 365
            listofzeros [index-1] = 1
            time_array = time_array + listofzeros
        else:
            listofzeros = [0] * 366
            listofzeros [index-1] = 1
            time_array = time_array + listofzeros
   
    time_dict.update({time_array[0]:time_array})   
time_dict = collections.OrderedDict(sorted(time_dict.items()))
print time_dict


text_file = open("test.txt", "w")

for key in time_dict:
    text_file.write(",".join(map(lambda x: str(x), time_dict[key])))
    text_file.write("\n")
text_file.close()   
    
# for key in time_dict:
#     for value in time_dict[key]:
#         text_file.write("%s," % value)
#     text_file.write("\n")
# text_file.close()   