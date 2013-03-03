#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:  rais --<CGE>
# Purpose: Moses, gh tcp client, have md5
# Created: 2013/1/5
debug=1

import os
from socket import *
import hashlib as hl
from hashlib import md5
from os.path import basename
from urlparse import urlsplit
import urllib2
from zipfile import ZipFile
import shutil

import nuke


#========================================================
# file
#========================================================
def extract2(zip_file, output_dir,first_dir):
	f_zip = ZipFile(zip_file, 'r')
	for f in f_zip.namelist():
		f_zip.extract(f, os.path.join(output_dir, first_dir))

def copyFile(sourceFile,  targetFile, test=1):

	if os.path.isfile(sourceFile):
		if not os.path.exists(os.path.dirname(targetFile)):
			os.makedirs(os.path.dirname(targetFile))
		print 'copying --> ',sourceFile
		print 'to-->',targetFile
		if not test:
			shutil.copyfile(sourceFile,targetFile)

def url2name(url):
	return basename(urlsplit(url)[2])

def down(url, localFileName=None):
	localName = url2name(url)
	req = urllib2.Request(url)
	r = urllib2.urlopen(req)
	f = open(localName, 'wb')
	f.write(r.read())
	f.close()


def md5_file(name):
	m = md5()
	a_file = open(name, 'rb')
	m.update(a_file.read())
	a_file.close()
	return m.hexdigest()


class Moses(object):
	"""docstring for Moses"""

	def __init__(self, host='127.0.0.1', port=2012):
		super(Moses, self).__init__()
		self.host = host
		self.port = port
		self.addr = (self.host, self.port)
		self.tcps = None
		self.question = ""
		self.answer = ''

	def getAnswer(self, question):
		self.addr = (self.host, self.port)
		self.question = question
		while True:
			try:
				self.__do()
			except Exception, e:
				try:
					self.tcps.close()
				except Exception, e:
					print 'close error: ', e
					continue
				print 'do while error:', e

				continue
			break
		return self.answer

	def __do(self, ):
		self.__tcp_connect()
		self.__say(self.question)

		jsonData = self.__tcp_adv_recv()
		if debug:print 'jsonData',jsonData
		import json

		self.answer = json.loads(jsonData)
		self.tcps.close()

	def __say(self, question=None):
		if question:
			self.question = question
		self.__tcp_send(self.question)

	def __tcp_recv(self, size):
		try:
			data = self.tcps.recv(size)
		except Exception, e:
			self.tcps.close()
			print e
			raise RuntimeError, 'tcp recv error:' + str(size)
		return data

	def __tcp_adv_recv(self):
		try:
			bsize = int(self.__tcp_recv(4))
		except Exception, e:
			print e
			return ''

		md5_remote = self.__tcp_recv(32)
		data = self.__tcp_recv(bsize)
		md5_loc = hl.md5(data).hexdigest()
		assert md5_loc == md5_remote
		return data

	def __tcp_send(self, data):
		bsize = len(data)
		str_bs = '0' * (4 - len(str(bsize))) + str(bsize)
		md5 = hl.md5(data).hexdigest()
		self.tcps.send(str_bs + md5 + data)

	def __tcp_connect(self):
		self.tcps = socket(AF_INET, SOCK_STREAM)
		self.tcps.setblocking(1)
		self.tcps.connect(self.addr)

#----------------------------------------------------------------------
def NukeQuestionFinding():
	""""""
	import nuke
	import platform

	ostype = platform.system()
	nukev = nuke.env["NukeVersionString"][:3]
	q = ['nuke_system', ostype, nukev]
	print 'os:', ostype, 'version:', nukev
	return q

#----------------------------------------------------------------------
def NukeAnalysis(mosesAnswer_og):
	mosesAnswer_list = mosesAnswer_og
	if len(mosesAnswer_list) <= 1:
		return {'syspath': mosesAnswer_list[0]}
	else:
		return {'syspath': mosesAnswer_list[0], 'md5': mosesAnswer_list[1]}


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
#----------------------------------------------------------------------
def update(dataFileName, mosesAnswer, nukeV):
	dataPath = os.path.join(mosesAnswer['syspath'],nukeV+ '.dat')
	NukeUserPath = getNukeUserPath()
	if debug: print 'dataPath', dataPath
	try:
		copyFile(dataPath, dataFileName,test=0)
	except Exception, e:
		print e
		pass
	print 'Prometeus down to ' + os.getcwd()
	print 'Set Prometeus...'
	fullUserPath = os.path.join(NukeUserPath,nukeV)
	if os.path.exists(fullUserPath):
		shutil.rmtree(fullUserPath)
	extract2(dataFileName,NukeUserPath,nukeV)
	return os.path.join(NukeUserPath,nukeV)



def chkupdate(mosesAnswer, questionList):
	dataFileName = os.path.abspath(questionList[2] + '.dat')
	if debug: print 'dataFileName', dataFileName
	if os.path.exists(dataFileName):
		md5data = md5_file(dataFileName)
		if debug:
			print md5data
			print mosesAnswer['md5']
		if md5data != mosesAnswer['md5']:
			return update(dataFileName, mosesAnswer,questionList[2])
		else:
			print 'Prometeus is last Version. ',md5data
			return os.path.join(getNukeUserPath(),questionList[2])
	else:
		return update(dataFileName, mosesAnswer, questionList[2])


def NukeDo(MosesObject=Moses(host='10.0.0.135')):
	import nuke
	import sys

	questionList = NukeQuestionFinding()
	if debug:print questionList
	question = ','.join(questionList)
	mosesAnswer_og = MosesObject.getAnswer(question)
	global mosesAnswer
	mosesAnswer = NukeAnalysis(mosesAnswer_og)

	#old
	#sys.path.append(syspath)
	#nuke.pluginAddPath(syspath)

	#new

	global syspath
	syspath = chkupdate(mosesAnswer, questionList)
	if debug:print 'syspath',syspath
	sys.path.append(syspath)
	nuke.pluginAddPath(syspath)

def main():
	a = Moses(host='127.0.0.1')
	print a.getAnswer("nuke_system,Linux,7.0")


if __name__ == '__main__':
	main()
