'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
__name__ = 'Poly Tools'

#import developer.main.dockWidget as dw
import inspect, os

from developer.main.common import commonFunctions as cf
from developer.main.common import dockWidget as dW

class mainForm(dockWidget.DockWidget):
    def __init__(self, parent = None):
        super(mainForm).__init__(parent)
        self.vLayout  = QtGui.QVBoxLayout()
        self.loadChildForm()
        
    def loadChildForm(self):
        childForms = [module for module in os.listdir(filedircommon) if 'Form' in module and module.end == '.py']
        for c in childForms:
            instance = CommonFunctions.loadModule(c)
            self.vLayout.addWidget(instance.main())


        