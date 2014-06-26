'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
from developer.main.common import commonFunctions as cf
from PyQt4 import QtGui, QtCore
from developer.main.polytools.mirrortools.fn import mirrorFunction as mFn
from developer.main.polytools.mirrortools.ui import mirrorUI
import os, inspect, functools

print '    Mirror Widget: Executing module ....'

class widget(QtGui.QMainWindow, mirrorUI.Ui_Form):
    '''
    Description: doing some mirror function.
    '''
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        self.setupUi(self)
        self.btnAxisX.clicked.connect(functools.partial(mFn.mirrorTool, 'x', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
        self.btnAxisY.clicked.connect(functools.partial(mFn.mirrorTool, 'y', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
        self.btnAxisZ.clicked.connect(functools.partial(mFn.mirrorTool, 'z', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
                                                                                                               
        self.btnPivotX.clicked.connect(functools.partial(mFn.mirrorTool, 'x', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))
        self.btnPivotY.clicked.connect(functools.partial(mFn.mirrorTool, 'y', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))
        self.btnPivotZ.clicked.connect(functools.partial(mFn.mirrorTool, 'z', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))  


print '    Mirror Widget: Finished module ....'