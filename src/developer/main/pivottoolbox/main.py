'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
pkgname  = 'PIVOT TOOLS'

from PyQt4 import QtGui, QtCore

from developer.main.common import commonFunctions as cf

class polytoolsForm(QtGui.QWidget):
    def __init__(self, subpackages, parent = None):
        super(polytoolsForm, self)._init__(parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.vSpacer = QtGui.QSpacer()
        self.setLayout(QtGui.QVBoxLayout)
        
    def loadSubPacks(subs):
        for p in subs:
            pass
        