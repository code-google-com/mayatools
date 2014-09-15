try:
	reload(ui)
except:
	from developer.main.uvtools.widget.ui import setuvratioUI as ui
	
try:
	reload(ui)
except:
	from developer.main.uvtools.fn import boltUvRatio as boltUvRatio

from PyQt4 import QtGui
import functools


class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		# Them GUI tao event action
		self.btnSetUVScale.clicked.connect(self.setUVScale)
		self.btnGetUVScale.clicked.connect(self.getUVScale)
		self.btnSetTexel.clicked.connect(functools.partial(self.setUVScale))
	def setUVScale(self):
		boltUvRatio.collect_shells_and_set_shells_UV_ratio(float(self.ldtRatio.text()))
	def getUVScale(self):
		ratio = boltUvRatio.get_sel_faces_UV_ratio(1)
		self.ldtRatio.setText(str(1/ratio))