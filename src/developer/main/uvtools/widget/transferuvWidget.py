import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools 
#import boltUvRatio
import math


try:
	reload(ui)
except:
	from developer.main.uvtools.widget.ui import transferuvUI as ui

import CommonFunctions as cf
reload(cf)

from developer.main.modeltools.fn import modeltoolsFn as pt
reload(pt)

from developer.main.editshaders.fn import EditShaderFn as st
reload(st)

from PyQt4 import QtGui

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		
		self.cbbSourceMat.addItems(['Materials from source'])
		self.cbbTargetMat.addItems(['Materials from target'])
		self.btnTransferUV.clicked.connect(self.transferUV)
	
	def transferUV(self):
		isAttached = False
        isDeleted = False
        # testing if node just have one shader
        shaders = st.getShadersFromMesh(str(self.ldtSource.text()))
        if len(shaders) > 1:
            st.selectFaceByShaderPerMesh(str(self.ldtSource.text()), str(self.cbbSourceMat.currentText()))
            pt.extractMesh()
            sourceMesh = py.ls(sl = True)[0]
            isDeleted = True
        elif len(shaders) == 1: 
            sourceMesh = str(self.ldtSource.text())
        elif len(shaders) == 0:
            QtGui.QMessageBox.critical(None, 'No shader found', 'Exit!', QtGui.QMessageBox.Ok)
            return
        #------------------------------------
        shaders = st.getShadersFromMesh(str(self.ldtTarget.text()))
        if len(shaders) > 1:
            st.selectFaceByShaderPerMesh(str(self.ldtTarget.text()), str(self.cbbTargetMat.currentText()))
            pt.detachMesh()
            targetMesh = py.ls(sl = True)[0]
        elif len(shaders) == 1:
            isAttached = False 
            targetMesh = str(self.ldtTarget.text())
        elif len(shaders) == 0:
            QtGui.QMessageBox.critical(None, 'No shader found', 'Exit!', QtGui.QMessageBox.Ok)
            return
        # transfer source mesh to target
        cmds.transferAttributes(sourceMesh, targetMesh, uvs = 2)
        # post-processing 
        cmds.select(targetMesh)
        mel.eval('DeleteHistory;')
        
        cmds.select(str(self.ldtTarget.text()))
        cmds.select(targetMesh, add = True)
        if isAttached:
            pt.attachMesh()
        if isDeleted:
            cmds.delete(sourceMesh)