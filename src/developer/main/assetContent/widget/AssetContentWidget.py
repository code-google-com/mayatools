try:
	reload(ui)
except:
	from developer.main.assetContent.widget.ui import AssetContentUI as ui

from PyQt4 import QtGui

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
