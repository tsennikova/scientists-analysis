'''
Created on 20 Jun 2016

@author: sennikta
'''
import urllib2
import os
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer




def get_file(url):  
    file_name ='view_dumps/' + url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
     
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
     
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print url.split('/')[-1], status, '\n\r'
     
    f.close()
    
for i in range (0,8):
    for j in range (0,12):
        year = 2011 + i
        month = 1 + j
        if month<10:
            month_str = '0' + str(month) 
        else:
            month_str = str(month)
        year_str = str(year)
        request_url = 'https://dumps.wikimedia.org/other/pagecounts-raw/' + year_str + '/' + year_str + '-' + month_str + '/'
        http = httplib2.Http()
        status, response = http.request(request_url)
        
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                if 'pagecounts' in link['href']:
                    get_file(request_url+link['href'])