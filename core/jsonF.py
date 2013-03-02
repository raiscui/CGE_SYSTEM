__author__ = 'rais'
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:  rais --<CGE>
# Purpose: CGE system json f
# Created: 2012/12/28

import json
import os

########################################################################
class jsonF(object):
	def __init__(self, DBpath = None):
		super(jsonF, self).__init__()
		self.DBpath = None
		if DBpath:
			self.initDB(DBpath)
		self.js_data = None


	def proDataSave(self,fpath=None):
		if fpath:
			self.initDB(fpath)
		assert self.DBpath !=None
		assert self.js_data !=None
		jn_data = json.dumps(self.js_data,indent=4, separators=(',', ': '))

		f = open(self.DBpath,'w')
		f.write(jn_data)
		f.close()

	def proDataLoad(self,fpath=None):
		if fpath:
			self.initDB(fpath)
		assert self.DBpath !=None
		f = open(self.DBpath,'r')
		self.js_data = json.loads(f.read())
		f.close()
		return self.js_data

	def initDB(self,fpath):
		self.setDBpath(fpath)
		assert self.DBpath !=None


	def setDBpath(self,fpath):
		import os.path
		if not os.path.exists(os.path.dirname(fpath)):
			os.makedirs(fpath)
		self.DBpath = fpath

if __name__ == '__main__':

	selfconfobj = jsonF('./'+__name__+'.conf')
	selfconf = selfconfobj.proDataLoad()
	from pprint import pprint
	pprint(selfconf)
	Proconfpath = selfconf['CGE_SYSTEM']['conf_object']['Prometeus']

	httpconfobj = jsonF(Proconfpath)
	httpconf = httpconfobj.proDataLoad()
	httpconf['nuke_system']['Windows']['6.3'] =[httpconf['nuke_system']['Windows']['6.3'],'9e57e9b5c5c75298b65342d25b9b7bf4']
	httpconf['nuke_system']['Linux']['6.3']= [httpconf['nuke_system']['Linux']['6.3'],'9e57e9b5c5c75298b65342d25b9b7bf4']
	httpconfobj.proDataSave()
	pprint(httpconfobj.proDataLoad())