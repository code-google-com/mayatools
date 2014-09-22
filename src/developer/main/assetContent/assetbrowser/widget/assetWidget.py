try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf
	
try: 
	reload(fO)
except:
	from developer.main.assetContent.assetbrowser.widget import fileObject as fO

from PyQt4 import QtGui, QtCore
import os, sys

status_dict = {'isLatestVersion':[0,1,0], 'isOutofDateVersion':[1,0,0],'isCheckedOutVersion':[1,0,0], 'isLocked':[0,0,0]}
mesh_type = ['ma', 'mb', 'fbx', 'obj', 'max']
texture_type = ['tga', 'tif', 'tiff', 'png', 'psd', 'jpg', 'jpeg']
shader_type = ['fx', 'hlsl', 'cgfx']
script_type = ['py', 'mel', 'ms']


class assetWidget(QtGui.QGraphicsWidget):
	# create property for widget
	# create signal for item
	
	clicked = QtCore.pyqtSignal('QString')
	changedStatus = QtCore.pyqtSignal()
	changedBG = QtCore.pyqtSignal()

	def __init__(self, image = None, parent = None):
		super(assetWidget, self).__init__(parent)
		self._initSize = 100
		self._radIcon = 10
		
		
		if image:
			self._bg = QtGui.QPixmap(image).scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		else:
			self._bg = QtGui.QPixmap(':/Project/diffuse.png').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

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
		QPixmapReflect = QtGui.QPixmap(self._bg)
		QPixmapMask = QtGui.QPixmap(':/Project/mask.tif').scaled(self._initSize, self._initSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		QPixmapReflect.setAlphaChannel(QPixmapMask)
		QPainter.scale(1, -1)
		QPainter.setOpacity(0.1)
		QPainter.translate(0, -2 * self._bg.height())
		QPainter.drawPixmap(0, 0, QPixmapReflect)
		QPainter.restore()
		
		# draw reflection effect
		QPainter.save()
		
		QPainter.restore()
		
		# draw clipping rounded rectangle
		
 		# draw icon status
		QPen = QtGui.QPen(QtCore.Qt.NoPen)
		QBrush = QtGui.QBrush(QtGui.QColor(0,204,0), QtCore.Qt.SolidPattern)
		QPainter.setBrush(QBrush)
		QPainter.setPen(QPen)
		QPainter.drawEllipse(self._bg.width() - (self._radIcon + 5) , self._bg.height() - (self._radIcon + 5), self._radIcon, self._radIcon)
		
	def updateIconStatus(self):
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
		self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
		self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAsNeeded)
	
	def resizeEvent(self, event):
		super(AssetWidgetView, self).resizeEvent(event)

			
		
		
	
