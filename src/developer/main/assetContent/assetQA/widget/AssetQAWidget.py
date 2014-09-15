try:
	reload(ui)
except:
	from developer.main.assetContent.assetQA.widget.ui import AssetQAUI as ui
	
try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf

from PyQt4 import QtGui

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self, parent = cf.getMayaWindow()):
		super(QtGui.QMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName('assetQAForm')
