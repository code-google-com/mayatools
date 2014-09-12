try:
	reload(ui)
except:
	from developer.main.modeltools.widget.ui import selecttoolsUI as ui
	
try:
	reload(sLn)
except:
	from developer.main.modeltools.fn import selectionFn as sLn

from PyQt4 import QtGui
from functools import partial

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		self.btnLoopEdges.clicked.connect(partial(self.execute, 1))
		self.btnRingEdges.clicked.connect(partial(self.execute, 2))
		self.btnSelectHardEdges.clicked.connect(partial(self.execute, 3))
		self.btnSelectSoftEdges.clicked.connect(partial(self.execute, 4))

	def execute(self, param):  
		if param == 1:
			spnLoop = self.spnLoop.value()
			sLn.LoopEdges(spnLoop)
			
		if param == 2: # freeze transform except rotation
			spnRing = self.spnRing.value()
			sLn.RingEdges(spnRing)
			
		if param == 3:
			sLn.selectEdgesOption(1)
		
		if param == 4:
			sLn.selectEdgesOption(0)