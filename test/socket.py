__author__ = 'Administrator'
import socket
import struct


HOST = socket.gethostbyname(socket.gethostname())

#noinspection PyCallingNonCallable
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


buf = s.recvfrom(65565)
print len(buf[0])
xx = len(buf[0])
src_ip11 = struct.unpack(''+str(xx)+'s', buf[0])
print type(src_ip11)
for x,y in enumerate(src_ip11):
	try:
		print 'keyU',x.decode('utf-8')
	except Exception, e:
		print e
		print 'key',x
	try:
		print 'vU',y.decode('utf-8')
	except Exception, e:
		print e
		print 'v',y

src_ip = "%s.%s.%s.%s"%struct.unpack('4B', buf[0][12:16])
dest_ip ="%s.%s.%s.%s"%struct.unpack('4B', buf[0][16:20])
print src_ip11
print src_ip, dest_ip
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)