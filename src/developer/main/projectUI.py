'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
import os, sys, re, inspect , imp, shutil

from xml.dom.minidom import *
import source.IconResource_rc

try:
    reload(dockWidget)
except:
    from developer.main.common import dockWidget 

try:
    reload(projectBase)
except:
    from developer.main.common import projectBase
    
try:
    reload(CommonFunctions)
except:
    from developer.main.common import CommonFunctions

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/ui/ProjectForm_test.ui'
print dirUI

form_class, base_class = CommonFunctions.loadUIPyQt(dirUI)

class projectUI(form_class,base_class):
    def __init__(self, XMLProject, parent = CommonFunctions.getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')