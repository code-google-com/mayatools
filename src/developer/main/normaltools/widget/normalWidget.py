'''
Created on Jun 27, 2014

@author: Trung
'''
try:
    reload(mFn)
except:
    from developer.main.normaltools.fn import normaltoolsFn as mFn

try:
    reload(ui)
except:
    from developer.main.normaltools.widget.ui import normalUI as ui

from PyQt4 import QtGui
from functools import partial


class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)
        self.setObjectName('normalWidgetToolbox')
        
        # Them control vao de tao event
        
        self.btnLockToLargeFace.clicked.connect(partial(self.execute, 0))
        self.btnLockToSmallFace.clicked.connect(partial(self.execute, 1))
        self.btnCopyNormal.clicked.connect(partial(self.execute, 2))
        self.btnCopyAverageNormal.clicked.connect(partial(self.execute, 3))
        self.btnPasteNormal.clicked.connect(partial(self.execute, 4))
        self.btnSmoothBevel.clicked.connect(partial(self.execute, 5))
        self.btnmatchSeamNormal.clicked.connect(partial(self.execute, 6))
        self.btnUnlock.clicked.connect(partial(self.execute, 7))
        self.btnSmoothAdjacentEdges.clicked.connect(partial(self.execute, 8))
        self.btnTransferNormalWithoutDetachMesh.clicked.connect(partial(self.execute, 9))
        self.btnMirrorTools.clicked.connect(partial(self.execute, 10))
        
    def execute(self, param):
        if param == 0:
            mFn.lockNormalToLargeFace()
        if param == 1:
            mFn.lockNormalToSmallFace()
        if param == 2:
            mFn.copyNormal()
        if param == 3:
            mFn.copyAverageNormal()
        if param == 4:
            mFn.pasteNormal()
        if param == 5:
            mFn.smoothBevelNormal()
        if param == 6:
            mFn.matchseamNormal()
        if param == 7:
            mFn.lockUnLocked()
        if param == 8:
            tolerance = str(self.spnSmoothEdges.value())
            mFn.smoothBorderEdges(tolerance)
        if param == 9:
            mFn.transferNormalWithoutDetachMesh()
        if param == 10:
            mFn.mirrorNormalTool()