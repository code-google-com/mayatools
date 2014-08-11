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

# -- end import packages

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		
		# -- set up ui controls
		
		self.btnPivottoCenterElement.clicked.connect(partial(self.execute, 0))
		self.btnCenterPivot.clicked.connect(partial(self.execute, 1))
		self.btnPivottoOrigin.clicked.connect(partial(self.execute, 2))
		self.btnPivottoanotherObj.clicked.connect(partial(self.execute, 3))
		self.btnFreezeTransform.clicked.connect(partial(self.execute, 4))
		self.btnZeroOffset.clicked.connect(partial(self.execute, 5))
		self.btnRotatePivot.clicked.connect(partial(self.execute, 6))
		self.btnPivotOnFace.clicked.connect(partial(self.execute, 7))
		self.btnSetPivotAlongEdge.clicked.connect(partial(self.execute, 8))
		
	def execute(self, param):
		if param == 0:
			pFn.setPivotToMidSelection()
		if param == 1:
			pFn.setPivotToCenter()
		if param == 2:
			pFn.setPivotToOrigin()
		if param == 3:
			pFn.setPivotToObject()
		if param == 4: # freeze transform except rotation
			pFn.freezeTransform(isTranslate = False, axis  = 'y', node = None)
		if param == 5:
			pFn.zeroPivotOffset()
		if param == 6:
			pFn.rotatePivot()
		if param == 7:
			pFn.pivotOnFace()
		if param == 8:
			pFn.setPivotOnLine(isTranslate, axis, node)

			
			
		
		
		


	