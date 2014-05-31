'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''

import developer.main.CommonFunctions as cf
cf.importQtPlugin()
cf.importMayaModule()


import os, sys, re, inspect , imp, shutil

from xml.dom.minidom import *

try:
    reload(dockWidget)
except:
    import dockWidget

try:
    reload(projectBase)
except:
    import projectBase
         
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ProjectForm.ui'
form_class, base_class = cf.loadUI(dirUI)

class ProjectUI(form_class,base_class):
    def __init__(self, XMLProject, parent = cf.getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.Proj = projectBase(XMLProject)
        self.setWindowTitle(self.Proj.ProjectName)
        self.xmlFile = XMLProject
        self.loadProjectData()
        
        #-------------- FUNCTION UI
        self.actionQA.triggered.connect(self.QAChecking)
        self.actionAsset_Tracking.triggered.connect(self.openAssetTracking)
        
    def loadProjectData(self):
        for index in range(len(self.Proj.moduleList[0])):
            try:
                instanceModule = loadModule(self.Proj.moduleList[0][index])
                form = instanceModule.main(self.Proj.moduleList[1][index])
                self.tabWidget.insertTab(index,form,form.__name__)
            except: 
                print 'Error to loading module:' + self.Proj.moduleList[0][index]
        #add dock widget
        #self.AssetForm = AssetForm.AssetForm(self.xmlFile)
        #self.currentAsset = self.AssetForm.currentAsset
        #self.dockWidget = dockWidget.DockWidget('Asset from')
        #self.dockWidget.setWidget(self.AssetForm)
        #self.verticalLayout.addWidget(self.dockWidget)
             
    def QAChecking(self):
        self.QAform = GE_QA.GE_QA(self.Proj.projectData, [])
        self.QAform.show()
        
    def openAssetTracking(self):
        self.AssetTrackingform = AssetTracking.AssetTracking(self.xmlFile)
        self.AssetTrackingform.show()

