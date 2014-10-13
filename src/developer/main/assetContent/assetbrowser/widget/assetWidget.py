try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf
	
try: 
	reload(fO)
except:
from developer.main.assetContent.assetbrowser.fn import fileObject as fO

from PyQt4 import QtGui, QtCore
import os, sys

status_dict = {'isLatestVersion':[0,1,0], 'isOutofDateVersion':[1,0,0],'isCheckedOutVersion':[1,0,0], 'isLocked':[0,0,0]}
mesh_type = ['ma', 'mb', 'fbx', 'obj', 'max']
texture_type = ['tga', 'tif', 'tiff', 'png', 'psd', 'jpg', 'jpeg']
shader_type = ['fx', 'hlsl', 'cgfx']
script_type = ['py', 'mel', 'ms']


class assetWidget(QtGui.QGraphicsWidget):
	
	# create signal for item
	
	clicked = QtCore.pyqtSignal('QString')
	changedStatus = QtCore.pyqtSignal()
	changedBG = QtCore.pyqtSignal()
	sizeX = 100
	
	def __init__(self, image = None, parent = None):
		super(assetWidget, self).__init__(parent)
		self._initSize = 100
		self._radIcon = 10
		# set up background
		QPixmapOpaque = QtGui.QBitmap(':/Project/mask_01.tif')
		if image:
			self._bg = QtGui.QPixmap(image)#.scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		else:
			self._bg = QtGui.QPixmap(':/Project/diffuse.png')#.scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		
		self._bg.setMask(QPixmapOpaque)
		self._bg = self._bg.scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		# set up status
		self._status = QtGui.QPixmap(':/Project/out.png').scaled(15, 15, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
	
	def boundingRect(self):
		return QtCore.QRectF(0, 0, self._bg.size().width(), self._bg.size().height())
		
	def paint(self, QPainter, styleOption, widget = None):
		
		# draw a background image.
		QPainter.drawPixmap(0, 0, self._bg)
		
		# draw mirror image
		QPainter.save()
		QPixmapMirror = QtGui.QPixmap(self._bg)
		QPixmapMask = QtGui.QPixmap(':/Project/mask.tif').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		QPixmapMirror.setAlphaChannel(QPixmapMask)
		QPainter.scale(1, -1)
		QPainter.setOpacity(0.1)
		QPainter.translate(0, -2 * self._bg.height())
		QPainter.drawPixmap(0, 0, QPixmapMirror)
		QPainter.restore()
		
		# draw reflection effect
		QPainter.save()
		QPainter.setOpacity(0.4)
		QPixmapReflection = QtGui.QPixmap(':/Project/mask_02.png').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		QPainter.drawPixmap(0, 0, QPixmapReflection)
		QPainter.restore()
		
 		# draw icon status
		QPainter.drawPixmap(self._bg.width() - (self._radIcon) , self._bg.height() - (self._radIcon), self._status)
		
	def updateIconStatus(self):
		pass
	
	def updateBackground(self):
		pass
	
	def animateOnHover(self):
		pass
	
	def animateOnClicked(self):
		pass
	
	def animateOnDoubleClicked(self):
		pass
	
	def _set_pos(self, pos):
		self.setPos(pos)
		
	def _set_Size(self, size):
		self.sizeX = size
		
	def _get_Size(self):
		return self.sizeX
	
	# create property for widget
	pos = QtCore.pyqtProperty(QtCore.QPointF, fset = _set_pos)
	
		
class AssetWidgetScene(QtGui.QGraphicsScene):
	
	def __init__(self, parent = None):
		super(AssetWidgetScene, self).__init__(parent)
		
	def drawBackground(self, painter, rect):
		rect = self.sceneRect()
		QBrush = QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.NoBrush)
		painter.fillRect(rect, QBrush)
		
	def mousePressEvent(self, mouseEvent):
		if mouseEvent.button() == QtCore.Qt.LeftButton:
			super(AssetWidgetScene, self).mousePressEvent(mouseEvent)
			
	def mouseMovingEvent(self, mouseEvent):
		super(AssetWidgetScene, self).mouseMovingEvent(mouseEvent)
		
class AssetWidgetView(QtGui.QGraphicsView):
	
	def __init__(self, parent = None):
		super(AssetWidgetView, self).__init__(parent)
		self.setRenderHint(QtGui.QPainter.Antialiasing)
		self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
		self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAsNeeded)
		self.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter) 
		self._layout = QtGui.QGraphicsGridLayout
	
	def resizeEvent(self, event):
		scene = self.scene()
		scene.setSceneRect(0, 0, event.size().width(), event.size().height())
		super(AssetWidgetView, self).resizeEvent(event)

			
		
		
	
