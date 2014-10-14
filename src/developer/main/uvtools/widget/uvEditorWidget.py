try:
	reload(ui)
except:
	from developer.main.uvtools.widget.ui import uvEditorUI as ui

from PyQt4 import QtGui

try:
	reload(uFn)
except:
	from developer.main.uvtools.fn import uvtoolsFn as uFn

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		
	def openUVEditor(self):
		pass
		
