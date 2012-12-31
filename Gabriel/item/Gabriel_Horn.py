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

class Server(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton("Quit")
        quitButton.setAutoDefault(False)

        self.tcpServer = QtNetwork.QTcpServer(self)
        self.blockSize = 0
        self.clientConnection=None
        self.currentQuestion = ''
        self.answerResult =  ''

        if not self.tcpServer.listen(QtNetwork.QHostAddress.Any, 2012):
            QtGui.QMessageBox.critical(self, "CGE Gabriel horm Server",
                    "Unable to start the server: %s." % self.tcpServer.errorString())
            self.close()
            return

        statusLabel.setText("The server is running on port %d." % self.tcpServer.serverPort())

        self.results = tree()
        self.results['nuke_system']['Windows']['6.3'] = '1'
        self.results['nuke_system']['Windows']['7.0'] = '2'
        self.results['nuke_system']['Linux']['6.3'] = '3'
        self.results['nuke_system']['Linux']['7.0'] = '4中文'
        self.results['nuke_system中文']['Linux']['7.0'] = '中文4中文'


        
        #====--------------------  connect  --------------------====
        
        quitButton.clicked.connect(self.close)
        self.tcpServer.newConnection.connect(self.slotNewConnect)
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
    def slotNewConnect(self):
        self.blockSize = 0
        self.clientConnection = self.tcpServer.nextPendingConnection()
        self.clientConnection.disconnected.connect(self.clientConnection.deleteLater)
        self.clientConnection.readyRead.connect(self.readQuestion)
    def thinking(self):
        self.answerResult  =  self.results
        for x in self.currentQuestion:
            self.answerResult  =  self.answerResult[x]
        if type(self.answerResult) is defaultdict:
            self.answerResult = "None"
        self.answer()
        #self.answerResult =  self.results[self.currentQuestion[0]][self.currentQuestion[1]][self.currentQuestion[2]]
    def answer(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        fortune = self.answerResult

        try:
            # Python v3.
            fortune = bytes(fortune, encoding='ascii')
        except:
            # Python v2.
            pass

        out.writeString(fortune)
        out.device().seek(0)
        out.writeUInt16(block.size() -2)


        self.clientConnection.write(block)
        self.clientConnection.disconnectFromHost()
        self.clientConnection.waitForDisconnected()
    def readQuestion(self):
        instr = QtCore.QDataStream(self.clientConnection)
        instr.setVersion(QtCore.QDataStream.Qt_4_0)

        if self.blockSize == 0:
            if self.clientConnection.bytesAvailable() < 2:
                print 'self.clientConnection.bytesAvailable() < 2:'
                return

            self.blockSize = instr.readUInt16()

        if self.clientConnection.bytesAvailable() < self.blockSize:
            print 'self.clientConnection.bytesAvailable() < self.blockSize:'
            return

        nextQuestion = instr.readString()

        try:
            # Python v3.
            nextQuestion = str(nextQuestion, encoding='ascii')
        except TypeError:
            # Python v2.
            #nextQuestion=nextQuestion.decode('utf-8')
            print 'TypeError,2'
            pass
        
        #nextQuestion = eval(nextQuestion)
        nextQuestion =  nextQuestion.split(',')
        if nextQuestion == self.currentQuestion:
            print 'nextQuestion == self.currentQuestion'
            QtCore.QTimer.singleShot(0, self.answer)
            return

        self.currentQuestion = nextQuestion
        self.thinking()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    server = Server()

    sys.exit(server.exec_())
