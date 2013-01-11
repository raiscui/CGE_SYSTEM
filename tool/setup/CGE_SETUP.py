#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/env python

# Author:  rais --<cge>
# Purpose: setup for cge system
# Created: 2012/M/day


# PyQT4 API 2 SetUp. Comment on remove if you are using Python 3
import sip,os

sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QTime', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)

from PyQt4 import QtCore, QtGui,uic
import CGE_SETUP_rc
CGE_SETUP_form, CGE_SETUP_base = uic.loadUiType('CGE_SETUP.ui')



class MainWindow(CGE_SETUP_form,CGE_SETUP_base,object):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		self.mayaPB.clicked.connect(self.__mayaInstall)
		self.nukePB.clicked.connect(self.__nukeInstall)


	def createButton(self, text, member):
		"""创建按钮包装"""
		button = QtGui.QPushButton(text)
		button.clicked.connect(member)
		return button

	def createMessageTable(self):
		"""创建文字框包装"""
		self.MessageTable = QtGui.QPlainTextEdit()
		self.MessageTable.setReadOnly(True)
		
	def getNukeUserPath(self):
		import getpass 
		userName = getpass.getuser()
		return os.path.join(userName,'.nuke')

	def __mayaInstall(self):
		QtGui.QMessageBox.about(None,
			u'CGEngine  -  Troy',
			u" <h2><font color='red'>" +u'还没有maya的安装！' +u' </font></h2><BR> '
		)

	def __nukeInstall(self):
		path = self.getNukeUserPath()

		


if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())
