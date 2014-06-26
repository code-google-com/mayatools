'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
modName = 'MIRROR TOOLS'

import inspect, os
from developer.main.common import commonFunctions as cf
from developer.main.common import dockWidget as dW

from widget import *

class mainWidget(dW.DockWidget):
    def __init__(self, parent = None):
        super(mainForm, self).__init__(modName)
        # create some item to store widget
        self.vLayout  = QtGui.QVBoxLayout()
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vLayout)
        # add widget
        for loader, module_name, is_pkg in pkgutil.walk_packages(widget.__path__):
            if not is_pkg:
                module = loader.find_module(module_name).load_module(module_name)
                print module.__name__
                self.vLayout.addWidget(module.widget())
        #--
        self.setWidget(self.widget)
        


        
        
        