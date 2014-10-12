try:
	reload(ui)
except:
	from developer.main.uvtools.widget.ui import setuvratioUI as ui
	
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
		# Them GUI tao event action
		self.btnSetUVScale.clicked.connect(functools.partial(self.execute, 0))
		self.btnGetUVScale.clicked.connect(functools.partial(self.execute, 1))
		#self.btnSetTexel.clicked.connect(functools.partial(self.setUVScale))
		self.btn64.clicked.connect(functools.partial(self.updateTexel, self.btn64.property('texel')))
		self.btn96.clicked.connect(functools.partial(self.updateTexel, self.btn96.property('texel')))
		self.btn128.clicked.connect(functools.partial(self.updateTexel, self.btn128.property('texel')))
		self.btn256.clicked.connect(functools.partial(self.updateTexel, self.btn256.property('texel')))
		self.btn512.clicked.connect(functools.partial(self.updateTexel, self.btn512.property('texel')))
		self.btn1024.clicked.connect(functools.partial(self.updateTexel, self.btn1024.property('texel')))
		
	def execute(self, param):
		if param == 0:
			uFn.setUVScale(float(self.ldtRatio.text()))
		elif param == 1:
			ratio = uFn.getUVScale()
			self.ldtRatio.setText(str(ratio))
			
	def updateTexel(self, texel):
		self.ldtTexel.setText(texel.toString())