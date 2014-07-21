from developer.main.common import commonFunctions as cf
from PyQt4 import QtGui

class subWidget(QtGui.QWidget):
    def __init__(self, lstTools):
        super(QtGui.QWidget,self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        for i in range(len(lstTools)):
            button = QtGui.QPushButton()
            mod = cf.loadNestedModule('developer.main.thirdtools.widget.' + lstTools[i])
            button.clicked.connect(mod.main)
            self.layout.addWidget(button)