try:
	reload(ui)
except:
	from developer.main.assetContent.assetbrowser.widget.ui import assetUI as ui

from PyQt4 import QtGui, QtCore
import os

status_dict = {'isLatestVersion':[0,1,0], 'isOutofDateVersion':[1,0,0],'isCheckedOutVersion':[1,0,0], 'isLocked':[0,0,0]}
mesh_type = ['ma', 'mb', 'fbx', 'obj', 'max']
texture_type = ['tga', 'tif', 'tiff', 'png', 'psd', 'jpg', 'jpeg']
shader_type = ['fx', 'hlsl', 'cgfx']
script_type = ['py', 'mel', 'ms']

class IconStat(QtGui.QGraphicsItem):
	def __init__(self, rad):
		self._color = color
		self._rad = rad
		super(IconStat, self).__init__()
	
	def paint(self, painter, styleOptions, widget = None):
		painter.begin()
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		for id, status in list(enumerate(self._icons)):
			QColor = QtGui.QColor(QtCore.Qt.red)
			painter.setBackground(QColor)
			#center = QtGui.QPoint(self.sceneRect().right() - self._rad * (2 * self._icons.__len__() - 1 ) , self.sceneRect().bottom() - self._rad)
			center = QtGui.QPoint(self._rad/2.0, self._rad/2.0)
			painter.drawEllipse(center, self._rad, self._rad)
		painter.end()
		
	def boundingRect(self):
		return QtGui.QRectF(0, 0, 2 * self._rad, 2 * self._rad)

class AssetWidgetScene(QtGui.QGraphicsScene):
	
	def __init__(self, bg, parent = None):
		super(AssetWidgetScene, self).__init__()
		self._backgroundImage = QtGui.QPixmap(bg).scaled(self.sceneRect().width(), self.sceneRect().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self._rad = 10
		self._icons = icons
		
	def drawBackground(self, QPainter, QRect):
		QRect = self.sceneRect()
		QPoint = QtCore.QPointF(QRect.top(), QRect.left())
		QPainter.drawPixmap(QPoint, self._backgroundImage, QRect)
		icon = IconStat(10.0)
		self.addItem(icon)
		
class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self, file, isLocked = True, status = list()):
		super(QtGui.QMainWindow, self).__init__(parent = None)
		self.setupUi(self)
		self.file = file # full name on local disk.
		self.scene = AssetWidgetScene(':/Project/empty.tif')
		self.setScene(self.scene)


class assetWidget(QtGui.QListWidgetItem):
	
	def __init__(self):
		super(assetWidget, self).__init__()bua 
			
		
		
	
