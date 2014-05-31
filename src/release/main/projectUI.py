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
    reload(GE_QA)
except: 
    import GE_QA

try:
    reload(AssetForm)
except:
    import AssetForm
    
try:
    reload(UploadForm)
except:
    import UploadForm 
    
try:
    reload(LibTextureUi)
except:
    import LibTextureUi 
    
try:
    reload(projectBase)
except:
    import ProjectBase
         
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ProjectForm.ui'
form_class, base_class = cf.loadUI(dirUI)

class ProjectUI(form_class,base_class):
    def __init__(self, XMLProject, parent = cf.getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.Proj = ProjectBaseClass(XMLProject)
        self.setWindowTitle(self.Proj.ProjectName)
        self.assetGroupModel = QtGui.QStringListModel()
        self.assetListModel = QtGui.QStringListModel()
        #cmds.scriptJob(killAll = True, f = True)
        self.xmlFile = XMLProject
        self.currentAsset = ''
        self.loadProjectData()
        #print self.Proj.projectData 
        
        #-------------- FUNCTION UI
        self.actionQA.triggered.connect(self.QAChecking)
        self.actionAsset_Tracking.triggered.connect(self.openAssetTracking)
        
    def combineString(self, strList, remove = 1):
        out = ''
        for i in range(len(strList)):
            if i != (len(strList) - 1):
                out += strList[i] + '_'
        return out    
        
    def loadProjectData(self):
        for index in range(len(self.Proj.moduleList[0])):
            try:
                instanceModule = loadModule(self.Proj.moduleList[0][index])
                form = instanceModule.main(self.Proj.moduleList[1][index])
                self.tabWidget.insertTab(index,form,form.__name__)
            except: 
                print 'Error to loading module:' + self.Proj.moduleList[0][index]
        #add dock widget
        self.AssetForm = AssetForm.AssetForm(self.xmlFile)
        self.currentAsset = self.AssetForm.currentAsset
        self.dockWidget = dockWidget.DockWidget('Asset from')
        self.dockWidget.setWidget(self.AssetForm)
        self.verticalLayout.addWidget(self.dockWidget)
             
    def QAChecking(self):
        self.QAform = GE_QA.GE_QA(self.Proj.projectData, [])
        self.QAform.show()
        
    def openAssetTracking(self):
        self.AssetTrackingform = AssetTracking.AssetTracking(self.xmlFile)
        self.AssetTrackingform.show()

