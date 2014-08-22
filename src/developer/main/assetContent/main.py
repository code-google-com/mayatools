'''
Created on Jun 18, 2014

@author: trungtran
@desciption: asset content form
'''
from PyQt4 import QtGui, QtCore

try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf
    
try:
    reload(acw)
except:
    from developer.main.assetContent.widget import AssetContentWidget as acw

try:
    reload(ui)
except:
    from developer.main.assetContent.widget.ui import AssetContentUI as ui

from PyQt4 import QtGui

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)

        
        