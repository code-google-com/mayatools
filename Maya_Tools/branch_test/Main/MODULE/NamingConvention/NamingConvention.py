import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools, imp

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/NamingConvention.ui'

def loadModule(path ,moduleName):
    sys.path.append(path)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()

form_class, base_class = uic.loadUiType(dirUI)        

class NamingConvention(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Naming & Hierrachy Tools'
        self.cbbNameList = list()
        self.listObjs = list()
        self.scriptjobNaming = cmds.scriptJob(e = ['SelectionChanged',self.updateNodeName], protected = True)   
        self.edtNameStr.returnPressed.connect(functools.partial(self.excuteChangNaming, 0))
        self.edtNamePrefix.returnPressed.connect(functools.partial(self.excuteChangNaming, 1))
        self.edtNameSuffix.returnPressed.connect(functools.partial(self.excuteChangNaming, 2))
        self.edtReplaceStr.returnPressed.connect(functools.partial(self.excuteChangNaming, 3))
        self.edtSelectByName.returnPressed.connect(functools.partial(self.excuteChangNaming, 4))
        self.btnUpperCase.clicked.connect(functools.partial(self.excuteChangNaming, 5))
        self.btnLowerCase.clicked.connect(functools.partial(self.excuteChangNaming, 6))
        self.updateNodeName()

        if inputFile != '':
            project = inputFile.split('.')[0]
            customFn = inputFile.split('.')[1]
            customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
            instanceModule = loadModule(customPath + '/Project/' + project + '/python', customFn)
            form = instanceModule.main()
            self.customUI.addWidget(form)
              
    def updateNodeName(self):
        selObj = cmds.ls(sl= True, fl = True)
        if len(selObj) != 0:
            self.edtNameStr.setText(str(selObj[0]))
        if len(selObj) == 0:
            self.edtNameStr.setText('')
                
    def renaming(self, newStr):
        selObj = cmds.ls(sl= True, transforms = True)
        if len(selObj) == 1:
            try:
                cmds.rename(newStr)
            except RuntimeError:
                QtGui.QMessageBox.warning(self,'Error','Khong the rename do ten khong hop le. Khong duoc dat so o dau tien.',QtGui.QMessageBox.Ok)
                    
        elif len(selObj) > 1:
            QtGui.QMessageBox.warning(self,'Error','Chon mot objec de rename',QtGui.QMessageBox.Ok)

    def addPrefix(self, newStr):
        selObjs = cmds.ls(sl = True)
        for obj in selObjs:
            newname = newStr + obj 
            cmds.rename(obj, newname)
            
    def addSuffix(self, newStr):
        selObjs = cmds.ls(sl =True)
        for obj in selObjs:
            newname = obj + newStr
            cmds.rename(obj, newname)
            
    def replaceBy(self, searchStr, newStr):
        selObjs = cmds.ls(sl = True)
        if not self.chkHierrachy.isChecked():
            for i in selObjs:
                newName = i.split('|')[-1].replace(searchStr, newStr)
                cmds.rename(i, newName)
        else:
            childNodes = cmds.listRelatives(ad = True, pa = True)
            for node in childNodes:
                newname = node.split('|')[-1].replace(searchStr, newStr)
                cmds.rename(node, newname)
            # rename selected nodes
            for node in selObjs:
                newName = node.split('|')[-1].replace(searchStr, newStr)
                cmds.rename(node, newname)
    
    def upperCase(self):
        selObjs = cmds.ls(sl =True)
        for obj in selObjs:
            cmds.rename(obj, obj.upper())
            
    def lowerCase(self):
        selObjs = cmds.ls(sl =True)
        for obj in selObjs:
            cmds.rename(obj, obj.lower())
                
    def excuteChangNaming(self, param):
        if param == 0: # raname node
            self.renaming(str(self.edtNameStr.text()))
        if param == 1: # chang prefix
            self.addPrefix(str(self.edtNamePrefix.text()))
        if param == 2: # change suffix
            self.addSuffix(str(self.edtNameSuffix.text()))
        if param == 3: # replace a substr in name
            self.replaceBy(self.ldtFind.text(), self.edtReplaceStr.text())
        if param == 4: # replace a substr in name
            self.selectNode(str(self.edtSelectByName.text()))    
        if param == 5:
            self.upperCase()
        if param == 6:
            self.lowerCase()
        
    def selectNode(self, param):
        cmds.select(param)
        selObjects = cmds.ls(sl = True)
        print 'Co ' +  str(len(selObjects)) + ' object duoc chon.'
        
    def unParent(self):
        pass
        
        
def main(xmlnput):
    form = NamingConvention(xmlnput)
    return form 

