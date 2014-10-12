try:
	reload(ui)
except:
	from developer.main.uvtools.widget.ui import moveuvUI as ui
	
try:
	reload(uFn)
except:
	from developer.main.uvtools.fn import uvtoolsFn as uFn

from PyQt4 import QtGui
import functools

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
			
		self.btnUp.clicked.connect(functools.partial(self.execute, 0))
		self.btnDown.clicked.connect(functools.partial(self.execute, 1))
		self.btnLeft.clicked.connect(functools.partial(self.execute, 2))
		self.btnRight.clicked.connect(functools.partial(self.execute, 3))
		self.btnMirrorU.clicked.connect(functools.partial(self.execute, 4))
		self.btnMirrorV.clicked.connect(functools.partial(self.execute, 5))
	
	def execute(self, params):
		if params == 0: # move uv up
			uFn.moveUVShell(float(self.lineEdit.text()), 'up')
		if params == 1: # move uv down
			uFn.moveUVShell(float(self.lineEdit.text()), 'down')
		if params == 2: # move uv left
			uFn.moveUVShell(float(self.lineEdit.text()), 'left')
		if params == 3: # move uv right
			uFn.moveUVShell(float(self.lineEdit.text()), 'right')
		if params == 4: # mirror horizontal UV shells base on origin 
			uFn.mirrorUV('H')
		if params == 5: # mirror vertical UV shells base on origin
			uFn.mirrorUV('V')




