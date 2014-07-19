
from developer.main.cleanertools.cleanerGroup import *
from PyQt4 import QtGui

class subWidget(QtGui.QWidget):
    def __init__(self, nodeRoot):
        super(QtGui.QWidget,self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        for i in range(len(nodeRoot)):
            grpCheck = cleanerGroup(nodeRoot[i][0], nodeRoot[i][1])
            self.layout.addWidget(grpCheck)

