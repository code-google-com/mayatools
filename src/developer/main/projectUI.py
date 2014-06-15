'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
try:
    reload(CommonFunctions)
except:
    from developer.main.common import CommonFunctions 
    
import os, sys, re, inspect , imp, shutil

from xml.dom.minidom import *

try:
    reload(dockWidget)
except:
    from developer.main.common import dockWidget 

try:
    reload(projectBase)
except:
    from developer.main.common import projectBase
         
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ProjectForm_test.ui'

try:
    form_class, base_class = CommonFunctions.loadUIPySide(dirUI)
    print 'PySide'
except:
    form_class, base_class = CommonFunctions.loadUIPyQt(dirUI)
    print 'PyQt'

class projectUI(form_class,base_class):
    def __init__(self, XMLProject, parent = CommonFunctions.getMayaWindow()):
        super(projectUI, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')