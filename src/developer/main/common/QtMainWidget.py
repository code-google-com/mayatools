'''
Created on Jul 10, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
from PyQt4 import QtGui, QtCore
import pkgutil, os

class QtMainWidget(QtGui.QScrollArea):
    def __init__(self):
        QtGui.QScrollArea.__init__(self)
        self.vsubLayout = QtGui.QVBoxLayout()
        self.vmainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.vmainLayout)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vsubLayout)
        self.setWidget(self.widget)
        
    def loadWidgetCustomize(self, pkgDockWidget):
        widgetLayout = QtGui.QVBoxLayout()
        self.vsubLayout.addLayout(widgetLayout)
        widgetLayout.addWidget(pkgDockWidget)
        
    def addSpacer(self):
        self.vSpacer = QtGui.QSpacerItem(40, 2000, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.vsubLayout.addItem(self.vSpacer)
