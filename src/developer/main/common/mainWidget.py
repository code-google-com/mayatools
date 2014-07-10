'''
Created on Jul 10, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
from PyQt4 import QtGui, QtCore
import pkgutil, os

class QtMainWidget(QtGui.QScrollArea):
    def __init__(self, subpackages, module_dir):
        QtGui.QScrollArea.__init__(self)
        self.vsubLayout = QtGui.QVBoxLayout()
        self.vmainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.vmainLayout)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vsubLayout)
        self.vSpacer = QtGui.QSpacerItem(40, 2000, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)

        ## load widget
        pkg_contents = list(pkgutil.walk_packages(os.path.split(module_dir)))
        for pkg_name in subpackages:
            for id in range(len(pkg_contents)): 
                if pkg_name == pkg_contents[id][1]:
                    if pkg_contents[id][2]:
                        pkg = pkg_contents[id][0].find_module(pkg_name).load_module(pkg_name)
                        for mod_loader, mod_name, is_mod in pkgutil.iter_modules(pkg.__path__):
                            if mod_name == 'main':
                                mod = mod_loader.find_module(mod_name).load_module(mod_name)
                                widgetLayout = QtGui.QVBoxLayout()
                                self.vsubLayout.addLayout(widgetLayout)
                                widgetLayout.addWidget(mod.subWidget())
        self.vsubLayout.addItem(self.vSpacer)
        self.setWidget(self.widget)
