import os
from os.path import basename
from urlparse import urlsplit
import urllib2
import nuke

import sys


def url2name(url):
	return basename(urlsplit(url)[2])


def down(url, localFileName=None):
	localName = url2name(url)
	req = urllib2.Request(url)
	r = urllib2.urlopen(req)
	f = open(localName, 'wb')
	f.write(r.read())
	f.close()

#****************************************************************#
def getPyVersion():
	""""""
	import sys
	return sys.version[:3]
#****************************************************************#
# if not os.path.exists('Moses.pyc'):
mosesPaths = ['http://huangxf.sunupcg.cn:8000/py/'+ getPyVersion() +'/Moses.pyc']
for mp in mosesPaths:
	try:
		down(mp)
	except Exception, e:
		print e
		pass
print os.getcwd()
#****************************************************************#
import Moses
Moses.NukeDo()

#****************************************************************#

global syspath
syspath = Moses.mosesAnswer['syspath']
print 'CGE NUKE syspath: ------------> \n', syspath
print '==========================='

for p in sys.path:
	print p
print '==========================='
