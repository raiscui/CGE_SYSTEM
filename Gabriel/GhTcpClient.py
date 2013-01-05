from socket import *
host = '127.0.0.1'
port = 2012
bufsiz = 1024
addr = (host, port)

tcps = socket(AF_INET, SOCK_STREAM)
tcps.connect(addr)

while True:
	data = "nuke_system,Linux,7.0"
	data = data
	if not data:
		break
	tcps.send(data)
	data = tcps.recv(bufsiz)
	if not data:
		break
	print data
	
tcps.close()