#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:  rais --<CGE>
# Purpose: Moses, gh tcp client, have md5
# Created: 2013/1/5

from socket import *
import hashlib as hl


class Moses(object):
	"""docstring for Moses"""
	def __init__(self, host = '127.0.0.1', port = 2012):
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

	def __do(self,):
		self.__tcp_connect()
		self.__say(self.question)
		self.answer = self.__tcp_adv_recv()
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
		bsize = int(self.__tcp_recv(4))

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
	q = ','.join(['nuke_system', ostype, nukev])
	print 'os:',ostype,'version:',nukev
	return q

#----------------------------------------------------------------------
def NukeDo(MosesObject):
	import nuke
	import sys
	
	mosesAnswer_og = MosesObject.getAnswer(NukeQuestionFinding())
	global mosesAnswer
	mosesAnswer = NukeAnalysis(mosesAnswer_og)
	syspath = mosesAnswer['syspath']
	sys.path.append(syspath)
	nuke.pluginAddPath(syspath)

def NukeAnalysis(mosesAnswer_og):
	mosesAnswer_list = mosesAnswer_og.split(',')
	return {'syspath':mosesAnswer_list[0]}


def main():
	a = Moses()
	print a.getAnswer("nuke_system,Linux,7.0")

if __name__ == '__main__':
	main()
