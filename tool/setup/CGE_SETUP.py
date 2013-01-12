#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/env python

# Author:  rais --<cge>
# Purpose: setup for cge system
# Created: 2012/M/day


# PyQT4 API 2 SetUp. Comment on remove if you are using Python 3
import sip, os
######################           down           ###########################
from urlparse import urlsplit
import urllib2

def url2name(url):
	return os.path.basename(urlsplit(url)[2])


def down(url, localFileName=None):
	localName = url2name(url)
	if localFileName:
		localName = localFileName
	req = urllib2.Request(url)
	r = urllib2.urlopen(req)
	f = open(localName, 'wb')
	f.write(r.read())
	f.close()

##########################################################################
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QTime', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)

from PyQt4 import QtCore, uic
from PyQt4.QtGui import *


CGE_SETUP_form, CGE_SETUP_base = uic.loadUiType('CGE_SETUP.ui')


class MainWindow(CGE_SETUP_form, CGE_SETUP_base, object):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		#====--------------------  信号连接  --------------------====
		self.connect(self, QtCore.SIGNAL("sms"), self.toMessageTab)
		self.mayaPB.clicked.connect(self.__mayaInstall)
		self.nukePB.clicked.connect(self.__nukeInstall)

	#		self.nukePB.pressed.connect(self.nukeInstall)



	def __createButton(self, text, member):
		"""创建按钮包装"""
		button = QPushButton(text)
		button.clicked.connect(member)
		return button

	def __createMessageTable(self):
		"""创建文字框包装"""
		self.MessageTable = QPlainTextEdit()
		self.MessageTable.setReadOnly(True)

	def getNukeUserPath(self):
		import getpass

		userName = getpass.getuser()
		return os.path.join('c:/', 'users', userName, '.nuke')

	def toMessageTab(self, *string):
		for s in string: self.MessageTable.appendPlainText(unicode(s))


	def __mayaInstall(self):
		QMessageBox.about(None,
			u'CGEngine  -  Troy',
			u" <h2><font color='red'>" + u'还没有maya的安装！' + u' </font></h2><BR> '
		)

	def __nukePB_off(self):
		self.nukePB.setEnabled(0)

	def __nukePB_on(self):
		self.nukePB.setEnabled(1)

	def nukeInstall(self):
		self.__nukePB_off()
		path = self.getNukeUserPath()


		def no():
			self.emit(QtCore.SIGNAL("sms"), u'Nuke模块没有安装')

		def yes():

		#			toPath = os.path.join(path, 'init.py')
		#			os.remove(toPath)
			urls = 'http://huangxf.sunupcg.cn:8000/NUKE-setup/init.py'
			os.chdir(path)
			try:
				down(urls)
			except Exception, e:
				self.emit(QtCore.SIGNAL("sms"), e)
				self.emit(QtCore.SIGNAL("sms"), u'Nuke模块安装有问题')
			else:
				self.emit(QtCore.SIGNAL("sms"), u'Nuke模块安装完毕')

			#		if 'init.py' in files:
			#			reInstallQMB = QMessageBox(self)
			#
			#			reInstallQMB.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			#			reInstallQMB.setDefaultButton(QMessageBox.Ok)
			#			ret = reInstallQMB.exec_()
			#			{str(QMessageBox.Ok):yes,
			#			 str(QMessageBox.Cancel):no
			#			}.get(str(ret), None)()
			#		else:
			#			yes()

		yes()


if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())
