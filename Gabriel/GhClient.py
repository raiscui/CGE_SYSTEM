#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# Author:  rais --<CGE>
# Purpose: ask Gabriel horn in progrom
# Created: 2012/12/29


from PyQt4 import QtCore, QtGui, QtNetwork
import sys
class GhClient(QtCore.QObject):
	def __init__(self, parent=QtGui.QApplication(sys.argv), host = '127.0.0.1', port = 2012, question = "nuke_system中文,Linux,7.0"):
		super(GhClient, self).__init__()
		self.parent = parent
		self.blockSize = 0
		self.currentAnswer = ''
		self.questionResult_unicode =  ''
		#self.hostLineEdit = 'huangxf.sunupcg.cn'
		self.host = '127.0.0.1'
		self.port = 2012
		self.question = question #"['nuke_system中文','Linux','7.0']"

		self.tcpSocket = QtNetwork.QTcpSocket()

		#====--------------------  connect  --------------------====
		self.tcpSocket.readyRead.connect(self.readAnswer)
		self.tcpSocket.error.connect(self.displayError)
		self.tcpSocket.connected.connect(self.ask)
		#****************************************************************#
	def requestNewTalk(self):
		self.blockSize = 0
		self.tcpSocket.abort()
		self.tcpSocket.connectToHost(self.host,self.port)
		
	def ask(self):
		block = QtCore.QByteArray()
		out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
		out.setVersion(QtCore.QDataStream.Qt_4_0)
		out.writeUInt16(0)
		fortune = self.question

		try:
			# Python v3.
			fortune = bytes(fortune, encoding='ascii')
		except:
			# Python v2.
			pass

		out.writeString(fortune)
		out.device().seek(0)
		out.writeUInt16(block.size() -2)


		self.tcpSocket.write(block)


	def readAnswer(self):
		instr = QtCore.QDataStream(self.tcpSocket)
		instr.setVersion(QtCore.QDataStream.Qt_4_0)

		if self.blockSize == 0:
			if self.tcpSocket.bytesAvailable() < 2:
				print 'self.tcpSocket.bytesAvailable() < 2:'
				return

			self.blockSize = instr.readUInt16()

		if self.tcpSocket.bytesAvailable() < self.blockSize:
			print 'self.tcpSocket.bytesAvailable() < self.blockSize:'
			return

		nextAnswer = instr.readString()

		try:
			# Python v3.
			nextAnswer = str(nextAnswer, encoding='ascii')
		except TypeError:
			# Python v2.

			print 'TypeError,2'
			pass

		#if nextAnswer == self.currentAnswer:
			#print 'nextFortune == self.currentFortune'
			##QtCore.QTimer.singleShot(0, self.requestNewTalk)
			#return

		self.currentAnswer = nextAnswer
		self.questionResult_unicode=self.currentAnswer.decode('utf-8')
		print self.questionResult_unicode
		self.parent.exit()

	def displayError(self, socketError):
		if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
			pass
		elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
			print "Gabriel horn Client","The host was not found. Please check the host name and ", "port settings."
		elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
			print "Gabriel horn Client","The connection was refused by the peer. Make sure the ", "fortune server is running, and check that the host name ", "and port settings are correct."
		else:
			print "Gabriel horn Client","The following error occurred: %s." % self.tcpSocket.errorString()
			
			
if __name__ == '__main__':
	print QtGui.qApp
	client = GhClient(QtGui.qApp)
	client.requestNewTalk()

	sys.exit(client.parent.exec_())



