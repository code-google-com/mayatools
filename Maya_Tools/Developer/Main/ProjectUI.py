import maya.cmds as cmds
import maya.mel as mel
import os, sys, re, inspect , imp, shutil
from pymel.core import *
from PyQt4 import QtGui, QtCore, uic
import sip
from xml.dom.minidom import *
import maya.OpenMayaUI as OpenMayaUI

try:
    reload(Source.IconResource_rc)
except:
    import Source.IconResource_rc
    
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
    reload(ProjectBaseClass)
except:
    import ProjectBaseClass
    
try:
    reload(GETeamWork)
except:
    from GETeamWork import *
    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ProjectForm.ui'
try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def loadModule(moduleName):
    sys.path.append(fileDirCommmon + '/MODULE/' + moduleName)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()
    
class ProjectUI(form_class,base_class):
    def __init__(self, XMLProject, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.Proj = ProjectBaseClass(XMLProject)
        self.setWindowTitle(self.Proj.ProjectName)
        self.assetGroupModel = QtGui.QStringListModel()
        self.assetListModel = QtGui.QStringListModel()
        cmds.scriptJob(killAll = True, f = True)
        self.xmlFile = XMLProject
        self.loadProjectData()
        #print self.Proj.projectData 
        
        #-------------- FUNCTION UI
        self.actionQA.triggered.connect(self.QAChecking)
        self.actionAsset_Tracking.triggered.connect(self.AssetTracking)
        
    def combineString(self, strList, remove = 1):
        out = ''
        for i in range(len(strList)):
            if i != (len(strList) - 1):
                out += strList[i] + '_'
        return out    
        
    def loadProjectData(self):
        print 'okie'
        print self.Proj.projectData 
        print 'okie'
        for index in range(len(self.Proj.moduleList[0])):
            #try:
                instanceModule = loadModule(self.Proj.moduleList[0][index])
                form = instanceModule.main(self.Proj.moduleList[1][index])
                self.tabWidget.insertTab(index,form,form.__name__)
            #except: 
                print 'Error to loading module:' + self.Proj.moduleList[0][index]
        #add dock widget
        self.AssetForm = AssetForm.AssetForm(self.xmlFile)
        self.dockWidget = dockWidget.DockWidget('Asset from')
        self.dockWidget.setWidget(self.AssetForm)
        self.formLayout.addWidget(self.dockWidget)
             
    def QAChecking(self):
        self.QAform = GE_QA.GE_QA(self.Proj.projectData, self.Proj.checkList)
        self.QAform.show()
        
    def AssetTracking(self):
        self.AssetTracking = AssetTracking.AssetTracking(self.xmlFile)
        self.AssetTracking.show()

        

    
                
            
        
                
            
            
        
                    
        
            
                
        
            
                  
             
        
            
               
            
                
    

        

                
