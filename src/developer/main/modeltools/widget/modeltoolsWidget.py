'''
Created on Jun 27, 2014

@author: Trung
'''

from developer.main.modeltools.fn import modeltoolsFn as mFn

try:
    reload(ui)
except:
    from developer.main.modeltools.widget.ui import modeltoolsUI as ui

from PyQt4 import QtGui
from functools import partial

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py 


class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)
        self.setObjectName('modelingToolbox')
        
        # THEM UI DE TAO EVENT
        self.btnAttach.clicked.connect(partial(self.execute, 0))
        self.btnDetach.clicked.connect(partial(self.execute, 1))
        self.btnDuplicate.clicked.connect(partial(self.execute, 2))
        #self.btnLoopEdges.clicked.connect(partial(self.execute, 3))
        #self.btnRingEdges.clicked.connect(partial(self.execute, 4))
        self.btnSmartCollapse.clicked.connect(partial(self.execute, 5))
        self.btnSnapVertexTool.clicked.connect(partial(self.execute, 6))
        
        
    def execute(self, param):
        if param ==0 :
            mFn.attachMesh()
            
        if param == 1:
            mFn.detachMesh()
                
        if param == 2:
            mFn.extractMesh()
                
        if param == 3:
            spnLoop = self.spnLoop.value()
            mFn.LoopEdges(spnLoop)
            
        if param == 4: # freeze transform except rotation
            spnRing = self.spnRing.value()
            mFn.RingEdges(spnRing)
                
        if param == 5:
            mFn.smartCollapsing()
                
        if param == 6:
            tolerance = str(self.spnTolerance.value())
            mFn.snapTool(tolerance)
            
        