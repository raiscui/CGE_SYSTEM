from os.path import basename
from urlparse import urlsplit
import urllib2
import nuke, platform, sys
def url2name(url):
	return basename(urlsplit(url)[2])

def down(url, localFileName = None):
	localName = url2name(url)
	req = urllib2.Request(url)
	r = urllib2.urlopen(req)
	f = open(localName, 'wb')
	f.write(r.read())
	f.close()

#----------------------------------------------------------------------
def QuestionFinding():
	""""""
	ostype = platform.system()
	nukev = nuke.env["NukeVersionString"][:3]
	q = ','.join(['nuke_system', ostype, nukev])
	print 'os:',ostype,'version:',nukev
	return q
#****************************************************************#
if not os.path.exists('Moses.pyc'):
	down('http://huangxf.sunupcg.cn:8000/Moses.pyc')
print os.getcwd()
#****************************************************************#
import Moses
global syspath
syspath=Moses.Moses().getAnswer(QuestionFinding())
#****************************************************************#
sys.path.append(syspath)
nuke.pluginAddPath(syspath)
#****************************************************************#
print 'CGE NUKE syspath: ------------> \n',syspath
print '==========================='
import sys
for p in sys.path:
	print p
print '==========================='


