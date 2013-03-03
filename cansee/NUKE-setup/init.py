import os
from os.path import basename,join,dirname
from urlparse import urlsplit
import urllib2
import nuke

import sys


def getNukeUserPath():
	import platform
	import getpass

	ostype = platform.system()

	userName = getpass.getuser()
	if ostype == 'Windows':
		return os.path.join('c:/', 'users', userName, '.nuke')
	elif ostype == 'Linux':
		return os.path.join('/home', userName, '.nuke')
	else:
		print "can't get os type!"


def url2name(url):
	return basename(urlsplit(url)[2])


def down(url, localFileName=None):
	if localFileName:
		localName = localFileName
	else:
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
def main():
	# if not os.path.exists('Moses.pyc'):
	mosesPaths = ['http://10.0.0.135:8000/py/' + getPyVersion() + '/Moses.pyc']
	toFPath = join(getNukeUserPath(),'Moses.pyc')
	for mp in mosesPaths:
		try:
			down(mp,toFPath)
		except Exception, e:
			print e
			pass
	print 'Moses down to ' + dirname(toFPath)
	#****************************************************************#
	import Moses

	Moses.NukeDo()

	#****************************************************************#

	global syspath
	syspath = Moses.syspath
	print 'CGE NUKE syspath: ------------> \n', syspath
	print '==========================='

	for p in sys.path:
		print p
	print '==========================='


if __name__ == '__main__':
	main()
