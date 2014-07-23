'''
Created on Jun 27, 2014

@author: Trung
'''
try:
    reload(mFn)
except:
    from developer.main.nametools.fn import namingFunction as mFn

try:
    reload(ui)
except:
    from developer.main.nametools.widget.ui import basicnameUI as ui

from PyQt4 import QtGui
import functools
import maya.cmds as cmds

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)
        self.setObjectName('basicnameWidget')
        
        # -- set ui controls:
        
        self.scriptjobNaming = cmds.scriptJob(e = ['SelectionChanged',self.updateNodeName], protected = True)  
         
        self.edtNameStr.returnPressed.connect(functools.partial(mFn.excuteChangeName, str(self.edtNameStr.text()), 0))
        self.edtNamePrefix.returnPressed.connect(functools.partial(mFn.excuteChangeName, str(self.edtNamePrefix.text()), 1))
        self.edtNameSuffix.returnPressed.connect(functools.partial(mFn.excuteChangeName, str(self.edtNameSuffix.text()), 2))
        self.edtReplaceStr.returnPressed.connect(functools.partial(mFn.excuteChangeName, self.ldtFind.text(), self.edtReplaceStr.text(), self.chkHierrachy.isChecked(), 3))
        self.edtSelectByName.returnPressed.connect(functools.partial(mFn.excuteChangeName, str(self.edtSelectByName.text()), 4))
        self.btnUpperCase.clicked.connect(functools.partial(mFn.excuteChangeName, 5))
        self.btnLowerCase.clicked.connect(functools.partial(mFn.excuteChangeName, 6))
        self.btnUpper1stLetter.clicked.connect(functools.partial(mFn.excuteChangeName, 7))
        
    def updateNodeName(self):
        selObj = cmds.ls(sl= True, fl = True)
        if len(selObj) != 0:
            self.edtNameStr.setText(str(selObj[0]))
        if len(selObj) == 0:
            self.edtNameStr.setText('')