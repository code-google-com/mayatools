'''
Created on Jun 18, 2014

@author: trungtran
@desciption: asset content form
'''

pkgname  = 'CLEAN UP TOOLS'

import functools
import os, sys, inspect
import developer.main.common.commonFunctions as cf
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore 

mayaVersion = cf.getMayaVersion()

try:
    reload(dW)
except:
    from developer.main.common import dockWidget as dW

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CleanerTools.ui'

form_class, base_class = cf.loadUI(dirUI)

class cleanerWidget(QtGui.QWidget):
    #checkedContent = QtCore.pyqtSignal('QString', name = 'tooggledStatus')
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
        
class cleanerSetWidget(dW.DockWidget):
    def __init__(self, folderName):
        super(dockWidget.DockWidget, self).__init__(os.path.split(folderName)[-1])
        self.titleBar = dockWidget.DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        self._dir = folderName
        margins = QtCore.QMargins(1,1,1,1)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(margins) 
        self._container = QtGui.QWidget()
        self._container.setLayout(self._layout)
        self.setWidget(self._container)
        self.loadChildrenTesting()
        
    def loadChildrenTesting(self):
        contentToCleanUpCommon = [(self._dir + '/' + f) for f in os.listdir(self._dir) if f.endswith('py')]
        for module in contentToCleanUpCommon:
            widget = cleanerWidget(module)
            self._layout.addLayout(widget.layout)

class ClearTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Tech Tools'
        self._contentCleanUp = list()
        self._customCheck = inputFile
        self.btnCheckAll.clicked.connect(self.executeAll)
        
        self.loadFunction()
        
    def loadFunction(self):
        contentToCleanUpCommon = [(fileDirCommmon + '/' + f) for f in os.listdir(fileDirCommmon) if os.path.isdir(fileDirCommmon + '/' + f) and f not in ['UI']]#,'Technical Setup','Fix issues per mesh']]
        contentToCleanUpProject = []
        project = self._customCheck.split('.')[0]
        customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
        try:
             contentToCleanUpProject = [(customPath + '/Project/' + project + '/python/' + f) for f in os.listdir(customPath + '/Project/' + project + '/python/')if os.path.isdir(customPath + '/Project/' + project + '/python/' + f) and f != 'UI']
        except:
             pass
        for f in contentToCleanUpCommon + contentToCleanUpProject:
            self.contents.addWidget(cleanerSetWidget(f))
            
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


