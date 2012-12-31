#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# Author:  rais --<CGE>
# Purpose: CGE system Gabriel horm service - ask and read
# Created: 2012/12/28



from PyQt4 import QtCore, QtGui, QtNetwork


class Client(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)

        self.blockSize = 0
        self.currentAnswer = ''

        hostLabel = QtGui.QLabel("&Server name:")
        portLabel = QtGui.QLabel("S&erver port:")

        self.hostLineEdit = QtGui.QLineEdit('Localhost')
        self.portLineEdit = QtGui.QLineEdit()
        self.portLineEdit.setValidator(QtGui.QIntValidator(1, 65535, self))
        
        self.askLineEdit = QtGui.QLineEdit(u"['nuke_system中文','Linux','7.0']")

        hostLabel.setBuddy(self.hostLineEdit)
        portLabel.setBuddy(self.portLineEdit)

        self.statusLabel = QtGui.QLabel("This examples requires that you run "
                "the Fortune Server example as well.")

        self.getFortuneButton = QtGui.QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)

        quitButton = QtGui.QPushButton("Quit")

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.tcpSocket = QtNetwork.QTcpSocket(self)
        
        #====--------------------  connect  --------------------====
        
        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewTalk)

        quitButton.clicked.connect(self.close)
        self.tcpSocket.readyRead.connect(self.readAnswer)
        self.tcpSocket.error.connect(self.displayError)
        self.tcpSocket.connected.connect(self.ask)
        #****************************************************************#

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.askLineEdit, 2, 0)

        mainLayout.addWidget(self.statusLabel, 3, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 4, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Client")
        self.portLineEdit.setFocus()

    def requestNewTalk(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(self.hostLineEdit.text(),
                int(self.portLineEdit.text()))
        
    def ask(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        fortune = self.askLineEdit.text()

        try:
            # Python v3.
            fortune = bytes(fortune, encoding='ascii')
        except:
            # Python v2.
            pass

        out.writeString(fortune.toUtf8())
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
        self.statusLabel.setText(self.currentAnswer.decode('utf-8'))
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QtGui.QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(bool(self.hostLineEdit.text() and
                self.portLineEdit.text()))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
