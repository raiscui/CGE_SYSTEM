#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# Author:  rais --<CGE>
# Purpose: gh tcp
# Created: 2013/1/5


from socket import *
host = '127.0.0.1'
port = 2012
bufsiz = 1024
addr = (host, port)




while True:
	tcps = socket(AF_INET, SOCK_STREAM)
	tcps.connect(addr)
	data = "nuke_system中文,Linux,7.0"
	data = data
	if not data:
		break
	tcps.send(data)
	print '-------------'
	try:
		
		data = tcps.recv(bufsiz)
	except:
		print 'nnnnnnnnnnnn'
		tcps.close()
		continue
	
	if data == '':
		print 'xx'
	
	
	print data.decode('utf-8')

	tcps.close()