'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
pkgname  = 'POLY TOOLS'

from PyQt4 import QtGui, QtCore, uic
from developer.main.common import commonFunctions
import pkgutil, os

class mainWidget(QtGui.QWidget):
    def __init__(self, subpackages, parent = None):
        print 'loading Polytools module .........................'
        super(mainWidget, self).__init__(parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.vSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.setLayout(QtGui.QVBoxLayout())

        
        ## load widget
        for loader, module_name, is_pkg in pkgutil.walk_packages(os.path.split(__file__)):
            if is_pkg and module_name in subpackages:
                pkg = loader.find_module(module_name).load_module(module_name)
                for mod_loader, name, is_mod in pkgutil.iter_modules(pkg.__path__):
                    if name == 'main':
                        mod = mod_loader.find_module(name).load_module(name)
                        self.vLayout.addWidget(mod.mainWidget())
        
        print 'finishing Polytools loading ..................... '