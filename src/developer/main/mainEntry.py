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


    ## show asset content form
    
    def openAssetBrowser(self):
        if py.window('assetContentForm', q = True, ex= True):
            py.deleteUI('assetContentForm')
        form = asc.assetContentForm()
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
                
                # loading cleaner tab
                if mod.getAttribute('name') == 'cleanertools':
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
                #------------------
                else:
                    submods = list()
                    for widget in mod.getElementsByTagName('submodule'): # get all widgets in package
                        submods.append(widget.getAttribute('name'))
                    instMod = cf.loadNestedModule('developer.main.' + mod.getAttribute('name') + '.main')
                    dockWidget = instMod.subWidget(submods)
                    scrollWidget.loadWidgetCustomize(dockWidget)
            scrollWidget.addSpacer()
            self.tabWidget.insertTab(index, scrollWidget, pkgName)