'''
Created on May 26, 2014

@author: trungtran
@description: ''

'''
cf.importQtPlugin()
import developer.main.dockWidget as dw

class mainForm(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(mainForm).__init__(parent)
        
    def loadUI(self):
        