'''
Created on Jun 21, 2014

@author: Trung
'''

pkgname = 'SHADER TOOLS'

from PyQt4 import QtGui, QtCore
import pkgutil, os

class mainWidget(QtGui.QScrollArea):
    def __init__(self, subpackages, parent = None):
        super(QtGui.QScrollArea, self).__init__(parent)
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
        pkg_contents = list(pkgutil.walk_packages(os.path.split(__file__)))
        for pkg_name in subpackages:
            for i in range(len(pkg_contents)): 
                if pkg_name == pkg_contents[i][1]:
                id = pkg_names.index(pkg_name)
                if is_pkgs[id]:
                    pkg = pkg_loaders[id].find_module(pkg_name).load_module(pkg_name)
                    for mod_loader, mod_name, is_mod in pkgutil.iter_modules(pkg.__path__):
                        if mod_name == 'main':
                            mod = mod_loader.find_module(mod_name).load_module(mod_name)
                            widgetLayout = QtGui.QVBoxLayout()
                            self.vsubLayout.addLayout(widgetLayout)
                            widgetLayout.addWidget(mod.subWidget())
        self.vsubLayout.addItem(self.vSpacer)
        self.setWidget(self.widget)
