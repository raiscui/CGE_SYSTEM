__author__ = 'rais'
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:  rais --<CGE>
# Purpose: CGE system md5 it
# Created: 2013/03/01
from hashlib import md5

def md5_file(name):
	m = md5()
	a_file = open(name, 'rb')
	m.update(a_file.read())
	a_file.close()
	return m.hexdigest()

if __name__ == '__main__':
	fpath ='/cifs/10.0.0.16/digitmovie_render/CGE_SYSTEM/nuke_system/nukePlugin/7.0.dat'
	print md5_file(fpath)