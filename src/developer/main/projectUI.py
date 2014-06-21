'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
import os, sys, re, inspect , imp, shutil
import pymel.core as py
from xml.dom.minidom import *
from PyQt4 import QtGui, QtCore, uic

try:
    reload(dockWidget)
except:
    from developer.main.common import dockWidget as dw 

try:
    reload(projectBase)
except:
    from developer.main.common import projectBase as proj
    
try:
    reload(commonFunctions)
except:
    from developer.main.common import commonFunctions as cf
    
try:
    reload(__main__)
except:
    from developer.main.assetContent import __main__  

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
        self.proj = proj.projectBase(XMLProject)
        
        # -- set ui controller
        
        self.actionAsset.triggered.connect(self.openAssetBrowser)
        
    def openAssetBrowser(self):
        if py.window('assetContentForm', q = True, ex= True):
            py.deleteUI('assetContentForm')
        form = __main__.assetContentForm()
        form.show()  
             
            