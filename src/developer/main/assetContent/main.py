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
    reload(AssetContent)
except:
    from developer.main.assetContent.ui import AssetContent

class assetContentForm(QtGui.QMainWindow, AssetContent.Ui_MainWindow):
    def __init__(self, parent = cf.getMayaWindow()):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('assetContentForm')
        
        