try:
    reload(clw)
except:
    import cleanerWidget as clw

from developer.main.common import commonFunctions as cf
from developer.main.common.dockWidget import *
from PyQt4 import QtGui, QtCore
import os

class cleanerGroup(DockWidget):
    def __init__(self, pkgName, filterList):
        super(DockWidget, self).__init__(pkgName)

        self.titleBar = DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(1)
        margins = QtCore.QMargins(1,1,1,1)
        self.layout.setContentsMargins(margins) 
        self.container = QtGui.QWidget()
        self.container.setLayout(self.layout)
        self.setWidget(self.container)

        if len(filterList) != 0 :
            contentCheck = [os.path.splitext(f)[0] for f in os.listdir(os.path.split(__file__)[0] + '\\' + pkgName) if f.endswith('py') and os.path.splitext(f)[0] in filterList]
        else: 
            contentCheck = [os.path.splitext(f)[0] for f in os.listdir(os.path.split(__file__)[0] + '\\' + pkgName) if f.endswith('py') if f != '__init__.py']
        
        for module in contentCheck:
            #print 'loading:' + pkgName + ' ......' + module
            widget = clw.cleanerWidget(pkgName + '.'+ module)
            self.layout.addLayout(widget.layout)
