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
# if not os.path.exists('Moses.pyc'):
mosesPaths = ['http://huangxf.sunupcg.cn:8000/Moses.pyc']
for mp in mosesPaths:
	try:
		down(mp)
	except Exception, e:
		print e
		pass
print os.getcwd()
#****************************************************************#
import Moses
global syspath
syspath = Moses.Moses().getAnswer(Moses.NukeQuestionFinding())
#****************************************************************#
sys.path.append(syspath)
nuke.pluginAddPath(syspath)
#****************************************************************#
print 'CGE NUKE syspath: ------------> \n', syspath
print '==========================='
import sys
for p in sys.path:
	print p
print '==========================='
