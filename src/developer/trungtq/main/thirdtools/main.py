from developer.main.common import commonFunctions as cf
from PyQt4 import QtGui, QtCore
import os

class subWidget(QtGui.QWidget):
    def __init__(self, lstTools):
        super(QtGui.QWidget,self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        
        if len(lstTools) != 0 :
            contentLoad = [os.path.splitext(f)[0] for f in os.listdir(os.path.split(__file__)[0] + '\\widget\\') if f.endswith('py') and os.path.splitext(f)[0] in lstTools]
        else: 
            contentLoad = [os.path.splitext(f)[0] for f in os.listdir(os.path.split(__file__)[0] + '\\widget\\') if f.endswith('py') if f != '__init__.py']
        
        for i in range(len(contentLoad)):
            mod = cf.loadNestedModule('developer.main.thirdtools.widget.' + contentLoad[i])
            size = QtCore.QSize(200, 30)
            size.scale(200, 30, QtCore.Qt.KeepAspectRatio)
            icon = QtGui.QIcon(mod.icon)
            button = QtGui.QPushButton()
            button.setToolTip(mod.tooltip)
            button.setIconSize(size)
            button.setIcon(icon)
            button.clicked.connect(mod.main)
            self.layout.addWidget(button) 