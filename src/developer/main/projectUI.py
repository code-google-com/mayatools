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
    reload(main)
except:
    from developer.main.assetContent import main

#-- get ui dir 

try:
    reload(ProjectForm)
except:
    from developer.main.ui import ProjectForm
    
#-- generate form_class and base_class to load Ui

class projectUI(QtGui.QMainWindow, ProjectForm.Ui_ProjectMainForm):
    def __init__(self, XMLProject, parent = cf.getMayaWindow()):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.proj = projb.projectBase(XMLProject)
        self.setWindowTitle(self.proj.ProjectName)
        #print len(self.proj.moduleList)
        self.loadUI()
        # -- set ui controller
        
        self.actionAsset.triggered.connect(self.openAssetBrowser)
        
    def openAssetBrowser(self):
        if py.window('assetContentForm', q = True, ex= True):
            py.deleteUI('assetContentForm')
        form = main.assetContentForm()
        form.show()  
        
    def loadUI(self):
        for index in range(len(self.proj.moduleList)):
            ##-- load pkg
            #try: 
                pkgName = 'developer.main.' + self.proj.moduleList[index][0] + '.main'
                pkg = cf.loadNestedModule(pkgName)
                self.tabWidget.insertTab(index, pkg.mainWidget(['mirrortools']), pkg.pkgname)
            #except: 
             #   print 'Error to loading module:' + self.proj.moduleList[index][0]
        
             
            