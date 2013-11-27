import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import maya.mel as mel
import imp
import functools

#BGColors = [[202,202,202],[255,255,255]]
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CleanerTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def loadModule(path ,moduleName):
    sys.path.append(path)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()
        
class ClearTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Cleaner Tools'
        self._contentCleanUp = list()
        self._customCheck = inputFile
        self.btnCheckAll.clicked.connect(self.executeAll)
        self.loadFunction()
        
    def loadFunction(self):
        #idColor = 0
        contentToCleanUpCommon = [f for f in os.listdir(fileDirCommmon + '/python/') if f.endswith('py')]
        contentToCleanUpProject = ''
        if self._customCheck != '':
            project = self._customCheck.split('.')[0]
            customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
            print customPath
            contentToCleanUpProject = [f for f in os.listdir(customPath + '/Project/' + project + '/python/checkingContents/')if f.endswith('py')]
        for module in contentToCleanUpCommon + contentToCleanUpProject:
            try:
                instanceModule = loadModule(fileDirCommmon + '/python/', module.split('.')[0])
            except ImportError:
                instanceModule = loadModule(customPath + '/Project/' + project + '/python/checkingContents/', module.split('.')[0])
            label = QtGui.QLabel(instanceModule.description)
            button = QtGui.QPushButton('Execute')
            chkbox = QtGui.QCheckBox()
            layout = QtGui.QHBoxLayout()
            layout.addWidget(chkbox)
            layout.addWidget(label)
            layout.addStretch(1)
            layout.addWidget(button)
            if module in contentToCleanUpCommon:
                self.CommonLayout.addLayout(layout)
            if module in contentToCleanUpProject:
                self.CustomLayout.addLayout(layout)
            chkbox.setChecked(True)
            button.clicked.connect(instanceModule.execute)
            chkbox.clicked.connect(functools.partial(self.updateContent, chkbox,instanceModule.name))
        
            
    def updateContent(self, chkbContent, content):
        if chkbContent.isChecked():
            #print 'add'
            self._contentCleanUp.append(content)
        else:
            #print 'remove'
            self._contentCleanUp.remove(content)
        
    def executeAll(self):
        #print self._contentCleanUp
        for module in self._contentCleanUp:
            instanceModule = loadModule(fileDirCommmon + '/python/', module)
            instanceModule.execute()

def main(xmlFile):
    form = ClearTools(xmlFile)
    return form   

