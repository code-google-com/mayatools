import maya.cmds as cmds

try:
	reload(ui)
except:
	from developer.main.setupscene.widget.ui import setupsceneUI as ui

from PyQt4 import QtGui, QtCore

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		self.btnSetupAxis.clicked.connect(self.changeAxis)
		self.btnSetupBackground.clicked.connect(self.changColorBackGround)
		
		# -- add slider to normal size button
		self.slider = QtGui.QSlider(self)
		self.slider.setOrientation (QtCore.Qt.Horizontal)
		self.slider.setMaximum(100)
		self.slider.setMinimum(1)
		self.actionSlide = QtGui.QWidgetAction(self.slider)
		self.actionSlide.setDefaultWidget(self.slider)
		self.btnSetNormalSize.addAction(self.actionSlide)
		
		# -- add ui to display option buttons
		self.chkBorderEdge = QtGui.QCheckBox('Show Border Edges')
		self.actionShowBorderEdges = QtGui.QWidgetAction(self.chkBorderEdge)
		self.actionShowBorderEdges.setDefaultWidget(self.chkBorderEdge)
		
		self.chkTextureEdge = QtGui.QCheckBox('Show UV Seams')
		self.actionShowUVSeams = QtGui.QWidgetAction(self.chkTextureEdge)
		self.actionShowUVSeams.setDefaultWidget(self.chkTextureEdge)
		
		self.chkSoftHardEdge = QtGui.QCheckBox('Show SoftEdges/ HardEdges')
		self.actionShowSoftHardEdges = QtGui.QWidgetAction(self.chkSoftHardEdge)
		self.actionShowSoftHardEdges.setDefaultWidget(self.chkSoftHardEdge)
		
		self.sldEdgeSize = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.sldEdgeSize.setMaximum(100)
		self.sldEdgeSize.setMinimum(1)
		self.actionEdgeSize = QtGui.QWidgetAction(self.sldEdgeSize)
		self.actionEdgeSize.setDefaultWidget(self.sldEdgeSize)
		self.btnSetNormalSize.addAction(self.actionEdgeSize)
		
		self.btnDisplayOptions.addAction(self.actionShowBorderEdges)
		self.btnDisplayOptions.addAction(self.actionShowUVSeams)
		self.btnDisplayOptions.addAction(self.actionShowSoftHardEdges)
		self.btnDisplayOptions.addAction(self.actionEdgeSize)
		
		self.slider.valueChanged.connect(self.changeNormalSize)
		self.btnSetNormalSize.clicked.connect(self.switchToNormalView)
		self.startUp()
		
	def startUp(self):
		up = cmds.upAxis(q = True, ax = True)
		if up == 'y':
			self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Y_up.png'))
		else:
			self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Z_up.png'))
			
		self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_off.png'))
		
	def changeAxis(self):
		up = cmds.upAxis(q = True, ax = True)
		if up == 'y':
			cmds.upAxis(ax = 'z')
			self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Z_up.png'))
		else:
			cmds.upAxis(ax = 'y')
			self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Y_up.png'))
			
	def changColorBackGround(self):
		if cmds.displayPref(q=True, displayGradient=True) == False: 
			cmds.displayRGBColor( 'background', 0.5, 0.5, 0.5 )
			cmds.displayPref(displayGradient=True)
		else:
			cmds.displayRGBColor( 'background', 1, 0, 1 )
			cmds.displayPref(displayGradient=False)
			
	def changeNormalSize(self):
		isNormalShowup = self.btnSetNormalSize.isChecked()
		if not isNormalShowup:
			return
		else:
			cmds.polyOptions(gl = True, dn = isNormalShowup, pt = True, sn = self.slider.value()/10.0)
		
	def switchToNormalView(self):
		selObjs = cmds.ls(sl = True)
		if len(selObjs) == 0:
			cmds.error('Please select one mesh')
			return
		else:
			isNormalShowup = cmds.polyOptions(selObjs[0], q = True, dn = True)[0]
			cmds.polyOptions(gl = True, dn = not isNormalShowup, pt = True, sn = self.slider.value()/10.0)
			self.btnSetNormalSize.setChecked(not isNormalShowup)
			if isNormalShowup:	
				self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_off.png'))
			else:
				self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_small.png'))
