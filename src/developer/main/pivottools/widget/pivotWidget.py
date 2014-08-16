# -- IMPORT ALL PACKAGES

try:
	reload(ui)
except:
	from developer.main.pivottools.widget.ui import pivotUI as ui
	
try:
	reload(pFn)
except:
	from developer.main.pivottools.fn import pivotFn as pFn

from PyQt4 import QtGui
from functools import partial

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py 

# -- FINISH IMPORT PACKAGE

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
		self.rdbXmin.clicked.connect(partial(self.execute, 9))
		self.rdbXmid.clicked.connect(partial(self.execute, 9))
		self.rdbXmax.clicked.connect(partial(self.execute, 9))
		self.rdbYmin.clicked.connect(partial(self.execute, 9))
		self.rdbYmid.clicked.connect(partial(self.execute, 9))
		self.rdbYmax.clicked.connect(partial(self.execute, 9))
		self.rdbZmin.clicked.connect(partial(self.execute, 9))
		self.rdbZmid.clicked.connect(partial(self.execute, 9))
		self.rdbZmax.clicked.connect(partial(self.execute, 9))
		self.rdbX.clicked.connect(partial(self.execute, 10))
		self.rdbY.clicked.connect(partial(self.execute, 10))
		self.rdbZ.clicked.connect(partial(self.execute, 10))
		
	def execute(self, param):
		if param == 0:
			pFn.setPivotToMidSelection()
			
		if param == 1:
			for node in py.ls(sl = True):
				pFn.setPivotToCenter(node)
				
		if param == 2:
			for node in py.ls(sl = True):
				pFn.setPivotToOrigin(node)
				
		if param == 3:
			pFn.setPivotToObject()
			
		if param == 4: # freeze transform except rotation
			for node in py.ls(sl = True):
				pFn.freezeTransform(node)
				
		if param == 5:
			for node in py.ls(sl = True):
				pFn.zeroPivotOffset(node)
				
		if param == 6:
			pFn.rotatePivot()
			
		if param == 7:
			pFn.pivotOnFace()
			
		if param == 8:
			pFn.setPivotOnLine(isTranslate, axis, node)
			
		if param == 9:
			if self.rdbXmin.isChecked():
				Xpos = 'Xmin'
			elif self.rdbXmid.isChecked():
				Xpos = 'Xmid'
			else:
				Xpos = 'Xmax'
			#=========================	
			if self.rdbYmin.isChecked():
				Ypos = 'Ymin'
			elif self.rdbYmid.isChecked():
				Ypos = 'Ymid'
			else:
				Ypos = 'Ymax'
			#=========================	
			if self.rdbXmin.isChecked():
				Zpos = 'Zmin'
			elif self.rdbXmid.isChecked():
				Zpos = 'Zmid'
			else:
				Zpos = 'Zmax'
			
			pFn.pivots_to_pos(Xpos, Ypos, Zpos)
			
		if param == 10:

			
			
		
		
		


	