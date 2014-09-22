try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf

from PyQt4 import QtGui, QtCore
from P4 import P4, P4Exception
import os, sys

status_dict = {'isLatestVersion':[0,1,0], 'isOutofDateVersion':[1,0,0],'isCheckedOutVersion':[1,0,0], 'isLocked':[0,0,0]}
mesh_type = ['ma', 'mb', 'fbx', 'obj', 'max']
texture_type = ['tga', 'tif', 'tiff', 'png', 'psd', 'jpg', 'jpeg']
shader_type = ['fx', 'hlsl', 'cgfx']
script_type = ['py', 'mel', 'ms']


class assetWidget(QtGui.QGraphicsWidget):
	# create property for widget
	NoSC, AddSC, UpSC, OutSC, CheckinSC, OtherSC = range(6) 
	# create signal for item
	
	clicked = QtCore.pyqtSignal('QString')
	changedStatus = QtCore.pyqtSignal()
	changedBG = QtCore.pyqtSignal()

	def __init__(self, image = None, lock = True,  parent = None):
		super(assetWidget, self).__init__(parent)
		self._initSize = 100
		if image:
			self._bg = QtGui.QPixmap(image).scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		else:
			self._bg = QtGui.QPixmap(':/Project/diffuse.png').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)

		
	def paint(self, QPainter, styleOption, widget = None):
		
		# draw a background image.
		QPainter.drawPixmap(0, 0, self._bg)
		
		# draw reflection effect
		QPainter.save()
		QPixmapReflect = QtGui.QPixmap(self._bg)
		QPixmapMask = QtGui.QPixmap(':/Project/mask.tif').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		QPixmapReflect.setAlphaChannel(QPixmapMask)
		QPainter.scale(1, -1)
		QPainter.setOpacity(0.1)
		QPainter.translate(0, -2 * self._bg.height())
		QPainter.drawPixmap(0, 0, QPixmapReflect)
		QPainter.restore()
		
 		# draw icon status
		QPen = QtGui.QPen(QtCore.Qt.NoPen)
		QBrush = QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern)
		QPainter.setBrush(QBrush)
		QPainter.setPen(QPen)
		QPainter.drawEllipse(self._bg.width() - 20, self._bg.height() - 20, 15, 15)
		
	def updateIconStatus(self, newstatus):
		pass
		
class AssetWidgetScene(QtGui.QGraphicsScene):
	
	def __init__(self, parent = None):
		super(AssetWidgetScene, self).__init__(parent)
		
	def drawBackground(self, painter, rect):
		rect = self.sceneRect()
		QBrush = QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.NoBrush)
		painter.fillRect(rect, QBrush)
		
	def resizeEvent(self, event):
		super(AssetWidgetScene, self).resizeEvent(event)
		
	def mousePressEvent(self, mouseEvent):
		if mouseEvent.button() == QtCore.Qt.LeftButton:
			super(AssetWidgetScene, self).mousePressEvent(mouseEvent)
			
	def mouseMovingEvent(self, mouseEvent):
		super(AssetWidgetScene, self).mouseMovingEvent(mouseEvent)
		
			
class AssetWidgetView(QtGui.QGraphicsView):
	
	def __init__(self, parent = None):
		super(AssetWidgetView, self).__init__(parent)
		self.setRenderHint(QtGui.QPainter.Antialiasing)
	
	def resizeEvent(self, event):
		print event.size()
			

			
		
		
	
