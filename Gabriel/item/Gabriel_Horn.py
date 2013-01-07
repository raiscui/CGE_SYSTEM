#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# Author:  rais --<CGE>
# Purpose: CGE system Gabriel horm service, add md5
# Created: 2012/12/28


from PyQt4 import QtCore, QtGui, QtNetwork
from collections import defaultdict
import hashlib as hl
def tree(): return defaultdict(tree)
def dicts(t):
	if type(t) ==  defaultdict:
		return {k: dicts(t[k]) for  k in t}
	else:
		return t
########################################################################
class gabrielHornThread(QtCore.QThread):
	"""CGE system Gabriel horm answer Thread"""
	error = QtCore.pyqtSignal(QtNetwork.QTcpSocket.SocketError)
	#----------------------------------------------------------------------
	def __init__(self, socketDescriptor, parent):
		"""Constructor"""
		super(gabrielHornThread, self).__init__(parent)
		self.sockDescriptor =  socketDescriptor
		self.tcpSocket = None
		
		self.results = tree()
		self.results['nuke_system']['Windows']['6.3'] = '1'
		self.results['nuke_system']['Windows']['7.0'] = '2'
		self.results['nuke_system']['Linux']['6.3'] = '3'
		self.results['nuke_system']['Linux']['7.0'] = '4中文'
		self.results['nuke_system中文']['Linux']['7.0'] = '中文文4中文文4中文文4中文'
	#----------------------------------------------------------------------
	def run(self):
		""""""
		self.tcpSocket = QtNetwork.QTcpSocket()
		if not self.tcpSocket.setSocketDescriptor(self.sockDescriptor):
			self.error.emit(self.tcpSocket.error())
			return
		#self.tcpSocket.readyRead.connect(self.readQuestion)
		self.tcpSocket.waitForReadyRead()
		self.readQuestion()
		self.tcpSocket.disconnectFromHost()
		if self.tcpSocket.waitForDisconnected():
			print 'disconnected'		
		

	#----------------------------------------------------------------------
	def readQuestion(self):
		print 'connected, readQuestion'

		data =  None
		try:
			bsize =  int(self.tcpSocket.read(4))
			md5_remote =  self.tcpSocket.read(32)
			data = self.tcpSocket.read(bsize)
			md5_loc = hl.md5(data).hexdigest()
			
		except:
			print 'can not got question'
			return
		if md5_loc == md5_remote:
			print data
		else:
			return



		try:
			currentQuestion =  data.split(',')
		except AttributeError:
			currentQuestion = None
			
			
		
	#====--------------------  thinking  --------------------====
		

		answerResult  =  self.results
		try:
			for x in currentQuestion:
				answerResult  =  answerResult[x]			
		except TypeError:
			answerResult = None

		if type(answerResult) is defaultdict:
			answerResult = None
		#self.sleep(1)



	#====--------------------  answer  --------------------====

		try:

			bsize = len(answerResult)
			str_bs = '0' * (4 - len(str(bsize))) + str(bsize)
			md5 = hl.md5(answerResult).hexdigest()
			self.tcpSocket.write(str_bs)
			self.tcpSocket.write(md5)
			self.tcpSocket.write(answerResult)
		except:
			#self.tcpSocket.write('None')
			pass
		
		
	
		




########################################################################
class gabrielHornSer(QtNetwork.QTcpServer):
	"""CGE system Gabriel horm answer service """

	#----------------------------------------------------------------------
	def __init__(self, parent=None):
		"""Constructor"""
		super(gabrielHornSer, self).__init__(parent)

 

	#----------------------------------------------------------------------
	def incomingConnection(self, socketDescriptor):
		""""""
		thread =  gabrielHornThread(socketDescriptor, self)
		thread.finished.connect(thread.deleteLater)
		thread.start()

########################################################################
class mainwin(QtGui.QDialog):
	def __init__(self, parent=None):
		super(mainwin, self).__init__(parent)

		statusLabel = QtGui.QLabel()
		quitButton = QtGui.QPushButton("Quit")
		quitButton.setAutoDefault(False)

		self.tcpServer =  gabrielHornSer()

		if not self.tcpServer.listen(QtNetwork.QHostAddress.Any, 2012):
			QtGui.QMessageBox.critical(self, "CGE Gabriel horm Server",
						               "Unable to start the server: %s." % self.tcpServer.errorString())
			self.close()
			return

		statusLabel.setText("The server is running on port %d." % self.tcpServer.serverPort())





		#====--------------------  connect  --------------------====

		quitButton.clicked.connect(self.close)

		#****************************************************************#

		buttonLayout = QtGui.QHBoxLayout()
		buttonLayout.addStretch(1)
		buttonLayout.addWidget(quitButton)
		buttonLayout.addStretch(1)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(statusLabel)
		mainLayout.addLayout(buttonLayout)
		self.setLayout(mainLayout)

		self.setWindowTitle("CGE Gabriel horm Server")



if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	server = mainwin()

	sys.exit(server.exec_())