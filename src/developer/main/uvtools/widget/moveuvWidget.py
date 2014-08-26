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
			

		self.btnUp.clicked.connect(functools.partial(self.moveUVShell,'up'))
		self.btnDown.clicked.connect(functools.partial(self.moveUVShell,'down'))
		self.btnLeft.clicked.connect(functools.partial(self.moveUVShell,'left'))
		self.btnRight.clicked.connect(functools.partial(self.moveUVShell,'right'))
		self.btnMirrorU.clicked.connect(functools.partial(uFn.mirrorUV,'H'))
		self.btnMirrorV.clicked.connect(functools.partial(uFn.mirrorUV,'V'))
    
	def moveUVShell(self, direction):
		if direction == 'down':
			cmds.polyEditUVShell( u = 0, v = -float(self.lineEdit.text()))
		if direction == 'up':
			cmds.polyEditUVShell( u = 0, v = float(self.lineEdit.text()))
		if direction == 'left':
			cmds.polyEditUVShell( u = -float(self.lineEdit.text()), v = 0)
		if direction == 'right':
			cmds.polyEditUVShell( u = float(self.lineEdit.text()), v = 0)