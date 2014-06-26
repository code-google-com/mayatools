'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
pkgname  = 'POLY TOOLS'

from PyQt4 import QtGui, QtCore, uic
from developer.main.common import commonFunctions as cf
import pkgutil, os

class mainWidget(QtGui.QWidget):
    def __init__(self, subpackages, parent = None):
        print 'loading Polytools module .........................'
        super(QtGui.QWidget, self).__init__(parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.vSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.setLayout(self.vLayout)

        #self.vLayout.setSizeConstraint(QtGui.QLayout.SetMaxSize)
        
        ## load widget
        for pkg_loader, pkg_name, is_pkg in pkgutil.walk_packages(os.path.split(__file__)):
            if is_pkg and pkg_name in subpackages:
                pkg = pkg_loader.find_module(pkg_name).load_module(pkg_name)
                for mod_loader, mod_name, is_mod in pkgutil.iter_modules(pkg.__path__):
                    if mod_name == 'main':
                        mod = mod_loader.find_module(mod_name).load_module(mod_name)
                        self.vLayout.addWidget(mod.subWidget())
                    
        self.vLayout.addItem(self.vSpacer)
        
        print 'finishing Polytools loading ..................... '