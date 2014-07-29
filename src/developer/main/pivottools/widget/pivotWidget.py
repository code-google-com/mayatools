# -- import custom packages

try:
	reload(ui)
except:
	from developer.main.pivottools.widget.ui import pivotUI as ui
	
try:
	reload(pFn)
except:
	from developer.main.pivottools.fn import pivotFn as pFn

# -- import 3rd packages

from PyQt4 import QtGui

# -- import standard package

from functools import partial

# -- import maya packages

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py 

# -- ending import packages

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		
		# -- set up ui controls
		
		self.btnSetPivotAlongEdge.clicked.connect(partial(self.execute, 0))
		self.btnZeroOffset.clicked.connect(partial(self.execute, 1))
		
	def execute(self, param):
		if param == 0:
			pFn.setPivotOnLine(isTranslate = False, axis  = 'y', node = None)
		if param == 1:
			pFn.zeroPivotOffset(py.ls(sl = True)[0])
		
		


	