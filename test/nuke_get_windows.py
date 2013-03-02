__author__ = 'Rais'
from PyQt4 import QtGui
a =QtGui.QWidget()
a.parent()

for widget in QtGui.qApp.allWidgets():
	x = widget.objectName()
	print x
