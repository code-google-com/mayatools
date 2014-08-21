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
    reload(AssetContentUI)
except:
    from developer.main.assetContent.widget.ui import AssetContentUI

class assetContentForm(QtGui.QMainWindow, AssetContentUI.Ui_MainWindow):
    def __init__(self, parent = cf.getMayaWindow()):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('assetContentForm')
        
    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap('Z:/ge_Tools/src/developer/main/source/icons/window_bg.png')
        region = QtGui.QRegion(pixmap.mask())
        self.setMask(region)
        
        