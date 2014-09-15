
from developer.main.cleanertools.cleanerGroup import *
from PyQt4 import QtGui

class subWidget(QtGui.QWidget):
    def __init__(self, nodeRoot):
        super(QtGui.QWidget,self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        
        # add content QA 
        for i in range(len(nodeRoot)):
            grpCheck = cleanerGroup(nodeRoot[i][0], nodeRoot[i][1])
            self.layout.addWidget(grpCheck)
        
        # add preset UI
        self.hLayout = QtGui.QHBoxLayout()
        self.btnSavePreset = QtGui.QPushButton('Save')
        self.btnSavePreset.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.cbbPresets = QtGui.QComboBox()
        self.hLayout.addWidget(self.btnSavePreset)
        self.hLayout.addWidget(self.cbbPresets)

        self.layout.addLayout(self.hLayout)
        
