'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
modName = 'MIRROR TOOLS'

import inspect, os, pkgutil
from PyQt4 import QtGui
from developer.main.common import commonFunctions as cf
from developer.main.common import dockWidget as dW

class mainWidget(dW.DockWidget):
    def __init__(self, parent = None):
        super(mainWidget, self).__init__(modName)
        # create some item to store widget
        self.vLayout  = QtGui.QVBoxLayout()
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vLayout)
        self.setWidget(self.widget)
        # add widget
        for pkg_loader, pkg_name, is_pkg in pkgutil.walk_packages(os.path.split(__file__)):
            if is_pkg and pkg_name == 'widget':
                pkg = pkg_loader.find_module(pkg_name).load_module(pkg_name)
                for mod_loader, mod_name, is_mod in pkgutil.iter_modules(pkg.__path__):
                    if mod_name != '__init__':
                        mod = mod_loader.find_module(mod_name).load_module(mod_name)
                        self.vLayout.addWidget(mod.widget())
        #--
        
        


        
        
        