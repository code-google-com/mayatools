'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''

import pymel.core as py
from xml.dom.minidom import *
from PyQt4 import QtGui, QtCore

try:
    reload(dw)
except:
    from developer.main.common import dockWidget as dw 

try:
    reload(projb)
except:
    from developer.main.common import projectBase as projb
    
try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf
    
try:
    reload(asc)
except:
    from developer.main.assetContent import main as asc
    
try:
    reload(pjc)
except:
    from developer.main.projectcreator import main as pjc
#-- get ui dir 

try:
    reload(ProjectForm)
except:
    from developer.main.source.ui import ProjectForm
    
from developer.main.common.QtMainWidget import *
    
#-- generate form_class and base_class to load Ui

class projectUI(QtGui.QMainWindow, ProjectForm.Ui_ProjectMainForm):
    def __init__(self, XMLProject, parent = cf.getMayaWindow()):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.proj = projb.projectBase(XMLProject)
        self.setWindowTitle(self.proj.ProjectName)
        self.loadUI()
        # -- set ui controller
        self.actionAsset.triggered.connect(self.openAssetBrowser)
        self.actionNew_Project.triggered.connect(self.openProjectCreator)

    def openAssetBrowser(self):
        if py.window('assetContentForm', q = True, ex= True):
            py.deleteUI('assetContentForm')
        form = asc.main.assetContentForm()
        form.show()
        
    def openProjectCreator(self):
        if py.window('projectCreatorForm', q = True, ex= True):
            py.deleteUI('projectCreatorForm')
        form = pjc.main.projectCreatorForm()
        form.show()    
        
    def loadUI(self):
        packages = self.proj.moduleLoader.getElementsByTagName('tab')
        for index in range(len(packages)):
            scrollWidget = QtMainWidget()
            pkgName = packages[index].getAttribute('name')
            modules = packages[index].getElementsByTagName('module')
            for mod in modules:
                submods = list()
                for widget in mod.getElementsByTagName('submodule'):
                    submods.append(widget.getAttribute('name'))
                instMod = cf.loadNestedModule('developer.main.' + mod.getAttribute('name') + '.main')
                print mod.getAttribute('name')
                dockWidget = instMod.subWidget(submods)
                scrollWidget.loadWidgetCustomize(dockWidget)
            scrollWidget.addSpacer()
            self.tabWidget.insertTab(index, scrollWidget, pkgName)

        
             
            