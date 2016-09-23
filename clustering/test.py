'''
Created on 9 Aug 2016

@author: sennikta
'''
import urllib2
import urllib

str=u'Cauchy\u2013Schwarz inequality'



str = str.encode("utf-8")
str = urllib2.unquote(str).decode("utf-8")
str = urllib.quote_plus(str.encode("utf-8"))

print str