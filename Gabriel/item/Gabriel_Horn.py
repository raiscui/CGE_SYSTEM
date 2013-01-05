#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# Author:  rais --<CGE>
# Purpose: CGE system Gabriel horm service
# Created: 2012/12/28


from PyQt4 import QtCore, QtGui, QtNetwork
from collections import defaultdict
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
		super(FortuneThread, self).__init__(parent)
		self.sockDescriptor =  socketDescriptor
		
		self.results = tree()
		self.results['nuke_system']['Windows']['6.3'] = '1'
		self.results['nuke_system']['Windows']['7.0'] = '2'
		self.results['nuke_system']['Linux']['6.3'] = '3'
		self.results['nuke_system']['Linux']['7.0'] = '4中文'
		self.results['nuke_system中文']['Linux']['7.0'] = '中文4中文'     		

	#----------------------------------------------------------------------
	def run(self):
		""""""
		tcpSocket = QtNetwork.QTcpSocket()
		if not tcpSocket.setSocketDescriptor(self.sockDescriptor):
			self.error.emit(tcpSocket.error())
			return
		tcpSocket.readyRead.connect(readQuestion)
		tcpSocket.waitForReadyRead()

		#----------------------------------------------------------------------
		def readQuestion(self):
			instr = QtCore.QDataStream(tcpSocket)
			instr.setVersion(QtCore.QDataStream.Qt_4_0)
	
	
			if tcpSocket.bytesAvailable() < 2:
				print 'tcpSocket.bytesAvailable() < 2:'
				return
	
			blockSize = instr.readUInt16()
	
			if tcpSocket.bytesAvailable() < blockSize:
				print 'tcpSocket.bytesAvailable() < self.blockSize:'
				return
	
			nextQuestion = instr.readString()
	
			try:
				# Python v3.
				nextQuestion = str(nextQuestion, encoding='ascii')
			except TypeError:
				# Python v2.
				#nextQuestion=nextQuestion.decode('utf-8')
				#print 'TypeError,2'
				pass
	
			currentQuestion =  nextQuestion.split(',')
	
			thinking(currentQuestion)
	
		#----------------------------------------------------------------------
		def thinking(self, currentQuestion):
			answerResult  =  self.results
			for x in currentQuestion:
				answerResult  =  answerResult[x]
			if type(answerResult) is defaultdict:
				answerResult = "None"
			answer(answerResult)
	
		#----------------------------------------------------------------------
		def answer(self, answerResult):
			block = QtCore.QByteArray()
			out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
			out.setVersion(QtCore.QDataStream.Qt_4_0)
			out.writeUInt16(0)
	
	
			try:
				# Python v3.
				answerResult = bytes(answerResult, encoding='ascii')
			except:
				# Python v2.
				pass
	
			out.writeString(answerResult)
			out.device().seek(0)
			out.writeUInt16(block.size() -2)
	
	
			tcpSocket.write(block)
			tcpSocket.disconnectFromHost()
			tcpSocket.waitForDisconnected()




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
	server = Server()

	sys.exit(server.exec_())