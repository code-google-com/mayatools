from PyQt4 import QtGui, QtCore

class installWindow(QtGui.QTableWidget):
    def __init__(self, pluginsPath):
        super(self).__init__(self, parent = None)
        self.path = pluginsPath
        self.tableWidget = QtGui.QTableWidget()
        
    def getPlugins(self):
        pass
        