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
         
        self.edtNameStr.returnPressed.connect(functools.partial(self.excuteChangeName, 0))
        self.edtNamePrefix.returnPressed.connect(functools.partial(self.excuteChangeName, 1))
        self.edtNameSuffix.returnPressed.connect(functools.partial(self.excuteChangeName, 2))
        self.edtReplaceStr.returnPressed.connect(functools.partial(self.excuteChangeName, 3))
        self.edtSelectByName.returnPressed.connect(functools.partial(self.excuteChangeName, 4))
        self.btnUpperCase.clicked.connect(functools.partial(self.excuteChangeName, 5))
        self.btnLowerCase.clicked.connect(functools.partial(self.excuteChangeName, 6))
        self.btnUpper1stLetter.clicked.connect(functools.partial(self.excuteChangeName, 7))
        
    def excuteChangeName(self, param):
        if param == 0:
            mFn.renaming(str(self.edtNameStr.text()))
        elif param == 1:
            mFn.addPrefix(str(self.edtNamePrefix.text()))
        elif param == 2:
            mFn.addSuffix(str(self.edtNameSuffix.text()))
        elif param == 3:
            mFn.replacedBy(self.ldtFind.text(), self.edtReplaceStr.text(), self.chkHierrachy.isChecked())
        elif param == 4:
            mFn.selectNode(str(self.edtSelectByName.text()))
        elif param == 5:
            mFn.upperCase()
        elif param == 6:
            mFn.lowerCase()
        elif param == 7:
            mFn.upperCaseOnFirstLetter()
        
    def updateNodeName(self):
        selObj = cmds.ls(sl= True, fl = True)
        print selObj
        if len(selObj) != 0:
            self.edtNameStr.setText(str(selObj[0]))
        if len(selObj) == 0:
            self.edtNameStr.setText('')