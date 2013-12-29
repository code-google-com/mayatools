import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import maya.mel as mel
import imp
import functools
import dockWidget as dW

#BGColors = [[202,202,202],[255,255,255]]
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CleanerTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def loadModule(moduleName):
    sys.path.append(os.path.split(moduleName)[0])
    file, pathname, description = imp.find_module(os.path.split(moduleName)[1].split('.')[0])
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()

class cleanerWidget(QtGui.QWidget):
    checkedContent = QtCore.pyqtSignal('QString', name = 'tooggledStatus')
    def __init__(self, module = None):
        super(QtGui.QWidget, self).__init__()
        instanceModule = loadModule(module)
        self.label = QtGui.QLabel(instanceModule.description)
        self.button = QtGui.QPushButton('Execute')
        self.chkbox = QtGui.QCheckBox()
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.chkbox)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.button)
        self.name = instanceModule.name
        self.chkbox.setChecked(True) 
        self.button.clicked.connect(instanceModule.execute)
        self.chkbox.clicked.connect(self.emitSignal)
        
    def toogleCheckBox(self):
        flag = self.chkbox.isChecked()
        self.chkbox.setChecked(not flag)
        #return self.chkbox
        
    def emitSignal(self):
        self.checkedContent.emit(str(self.chkbox.isChecked()) + '_' + self.name)
        print self.name

class ClearTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Tech Tools'
        self._contentCleanUp = list()
        self._customCheck = inputFile
        self.btnCheckAll.clicked.connect(self.executeAll)
        margins = QtCore.QMargins(1,1,1,1)
        
        self.commonDock = dW.DockWidget('COMMON TESTING')
        self.projectDock = dW.DockWidget('PROJECT TESTING')
        
        self.contents.addWidget(self.commonDock)
        self.contents.addWidget(self.projectDock)
        
        self._widgetCommon = QtGui.QWidget()
        self._widgetProject = QtGui.QWidget()
        
        self._layoutCommon = QtGui.QVBoxLayout()
        self._layoutCommon.setSpacing(1)
        self._layoutCommon.setContentsMargins(margins) 
        self._layoutProject = QtGui.QVBoxLayout()
        self._layoutProject.setSpacing(1)
        self._layoutProject.setContentsMargins(margins) 
    
        self._widgetCommon.setLayout(self._layoutCommon)
        self._widgetProject.setLayout(self._layoutProject)
        
        self.commonDock.setWidget(self._widgetCommon)
        self.projectDock.setWidget(self._widgetProject)
        
        self.loadFunction()
        
    def loadFunction(self):
        #idColor = 0
        contentToCleanUpCommon = [(fileDirCommmon + '/python/' + f) for f in os.listdir(fileDirCommmon + '/python/') if f.endswith('py')]
        contentToCleanUpProject = []
        project = self._customCheck.split('.')[0]
        print project
        customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
        try:
            contentToCleanUpProject = [(customPath + '/Project/' + project + '/python/checkingContents/' + f) for f in os.listdir(customPath + '/Project/' + project + '/python/checkingContents/')if f.endswith('py')]
        except:
            pass
        print contentToCleanUpProject
        for module in contentToCleanUpCommon + contentToCleanUpProject:
            widget = cleanerWidget(module)
            if module in contentToCleanUpCommon:
                self._layoutCommon.addLayout(widget.layout)
            if module in contentToCleanUpProject:
                self._layoutProject.addLayout(widget.layout)
            self._contentCleanUp.append(widget.name)
            widget.tooggledStatus.connect(self.updateContent)
            
    def updateContent(self, strResult):
        if bool(strResult.split('_')[0]):
            self._contentCleanUp.append(strResult.split('_')[1])
        else:
            self._contentCleanUp.remove(strResult.split('_')[1])
        print self._contentCleanUp
        
    def executeAll(self):
        for module in self._contentCleanUp:
            instanceModule = loadModule(fileDirCommmon + '/python/', module)
            instanceModule.execute()

def main(xmlFile):
    form = ClearTools(xmlFile)
    return form   

