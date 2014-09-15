import pymel.core as py
import getpass
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
    reload(pjc)
except:
    from developer.main.projectcreator import main as pjc
#-- get ui dir 

try:
    reload(ProjectForm)
except:
    from developer.main.source.ui import ProjectForm
    
from developer.main.common.QtMainWidget import *

try:
    reload(serverPub)
except:
    from developer.main.common import serverPub
    
try:
    reload(clientSub)
except:
    from developer.main.common import clientSub
    
try:
    reload(aBw)
except:
    from developer.main.assetContent.assetbrowser.widget import AssetBrowserWidget as aBw
    
try:
    reload(aQa)
except:
    from developer.main.assetContent.assetQA.widget import AssetQAWidget as aQa
    
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
        
        self.actionAssetBrowser.triggered.connect(self.openAssetBrowser)
        self.actionAssetQA.triggered.connect(self.openAssetQA)
        self.actionNew_Project.triggered.connect(self.openProjectCreator)
        
        # -- create socket linked project name:
        # ------ only Technician can publish and edit code
        
        #if getpass.getuser() in self.proj.Technician(): 
        #    self.soc = serverPub.socketPublishProjectInfo(os.environ.get('PROJECT_DIR') + '\\projects\\' + self.proj.ProjectName)
        # ------ artist can only subscribe and edit code
        
        #elif getpass.getuser() == 'trungtran':
        #    self.soc = clientSub.socketSubscribeProjectInfo()

    ## show asset content form
    
    def openAssetBrowser(self):
        if py.window('assetBrowserForm', q = True, ex= True):
            py.deleteUI('assetBrowserForm')
        form = aBw.QtWidget()
        form.show()
        
    def openAssetQA(self):
        if py.window('assetQAForm', q = True, ex= True):
            py.deleteUI('assetQAForm')
        form = aQa.QtWidget()
        form.show()
                
    ## show project creator form  
      
    def openProjectCreator(self):
        if py.window('projectCreatorForm', q = True, ex= True):
            py.deleteUI('projectCreatorForm')
        form = pjc.projectCreatorForm()
        form.show()    
        
    def loadUI(self):
        packages = self.proj.moduleLoader.getElementsByTagName('tab') # create tab in mainform base on name
        for index in range(len(packages)):
            scrollWidget = QtMainWidget()
            pkgName = packages[index].getAttribute('name')   
            modules = packages[index].getElementsByTagName('module') # get package name --> assign this to a QtMainWidget inherited from DockWidget 
            for mod in modules:
                
                # loading 3rd tools
                
                if mod.getAttribute('name') == 'thirdtools':
                    #print 'loading:---------------------- Third Tools---------------------------------'
                    lstTools = list()
                    thirdtools = mod.getElementsByTagName('submodule')
                    for submod in thirdtools:
                        lstTools.append(submod.getAttribute('name'))
                    instMod = cf.loadNestedModule('developer.main.thirdtools.main')
                    dockWidget = instMod.subWidget(lstTools)
                    scrollWidget.loadWidgetCustomize(dockWidget)
                    
                # loading cleaner tab
                
                elif mod.getAttribute('name') == 'cleanertools':
                    #print 'loading:---------------------- Cleaner Tools---------------------------------'
                    itemChecks = list()
                    for sub in mod.getElementsByTagName('submodule'):
                        tmp = list()
                        tmp.append(sub.getAttribute('name'))
                        itemTmp = list()
                        for item in sub.getElementsByTagName('item'):
                            itemTmp.append(item.getAttribute('name'))
                        tmp.append(itemTmp)
                        itemChecks.append(tmp)
                    instMod = cf.loadNestedModule('developer.main.cleanertools.main')
                    dockWidget = instMod.subWidget(itemChecks)
                    scrollWidget.loadWidgetCustomize(dockWidget)
                    
                # loading functional tabs
                
                else:
                    #print 'loading:---------------------- Functional Tools---------------------------------'
                    submods = list()
                    for widget in mod.getElementsByTagName('submodule'): # get all widgets in package
                        submods.append(widget.getAttribute('name'))
                    instMod = cf.loadNestedModule('developer.main.' + mod.getAttribute('name') + '.main')
                    dockWidget = instMod.subWidget(submods)
                    scrollWidget.loadWidgetCustomize(dockWidget)
                    
                #-------------------------------
            scrollWidget.addSpacer()
            self.tabWidget.insertTab(index, scrollWidget, pkgName)
    
   