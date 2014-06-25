'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
modName = 'MIRROR TOOLS'

import inspect, os
from developer.main.common import commonFunctions as cf
from developer.main.common import dockWidget as dW

class mainForm(dW.DockWidget):
    def __init__(self, parent = None):
        super(mainForm, self).__init__(modName)
        # create some item to store widget
        self.vLayout  = QtGui.QVBoxLayout()
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vLayout)
        # add widget
        self.setWidget(self.widget)
        


        
        
        