#import maya.cmds as cmds
#import maya.mel as mel
import os, sys, re, inspect , imp, shutil
import math
#from pymel.core import *
from PyQt4 import QtGui, QtCore, uic
import sip
import functools

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/Decal_Form.ui'

try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class Decal(QtGui.QGraphicsPixmapItem):
    lostFosus = QtCore.pyqtSignal(QtGui.QGraphicsItem)
    selectedChanged = QtCore.pyqtSignal(QtGui.QGraphicsItem)
    def __init__(self, path, parent = None):
        super(Decal, self).__init__(parent)
        self.setPixmap(QtGui.QPixmap(path))
        self.size = 1
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, enabled = True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, enabled = True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, enabled = True)
        self.scaleFactor = 1
        
    def wheelEvent(self, event):
        self.scaleFactor += event.delta() / 720.0
        if self.scaleFactor < 0.35 or self.scaleFactor > 2:
            return  
        self.setScale(self.scaleFactor)
        self.resetTransform()
        print self.boundingRect().width() * self.scaleFactor
        
        print self.boundingRect().height() * self.scaleFactor
        
    def setSignalPos(self, dx, dy):
        pos = QtCore.QPointF(dx * 550 / 100.0, dy * 550 / 100.0)
        self.setPos(pos)
        
    def boundingRectCustom(self):
        rect = QtCore.QRectF()
        rect.setWidth(self.boundingRect().width() * self.scaleFactor)
        rect.setHeight(self.boundingRect().height() * self.scaleFactor)
        return rect
    
    def posCustom(self):
        posF = QtCore.QPointF()
        posF.setX(self.pos().x() + self.boundingRectCustom().width()/2)
        posF.setY(self.pos().y() + self.boundingRectCustom().height()/2)
        return posF

class DecalScene(QtGui.QGraphicsScene):
    insertDecal, moveDecal = range(2)
    
    decalInserted = QtCore.pyqtSignal(Decal)
    
    decalMoved = QtCore.pyqtSignal(QtCore.QPointF)
    
    def __init__(self, bg, decal, parent = None):
        super(DecalScene, self).__init__(0, 0, 550, 550, parent)
        self._backgroundImage = QtGui.QPixmap(bg).scaled(self.sceneRect().width(), self.sceneRect().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self._decalImage = QtGui.QPixmap(decal)
        self.myMode = self.insertDecal
        self.cursorPos = QtCore.QPointF()
        self.decal = Decal(self._decalImage)
        #self.addPixmap(self._backgroundImage)
        
    def setMode(self, mode):
        self.myMode = mode
        
    def drawBackground(self, QPainter, QRect):
         QRect = self.sceneRect()
         QPoint = QtCore.QPointF(QRect.top(), QRect.left())
         QPainter.drawPixmap(QPoint, self._backgroundImage, QRect)
        
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != QtCore.Qt.LeftButton:
            return
        if self.myMode == self.insertDecal:
            self.addItem(self.decal)
            insertedPos = QtCore.QPointF(mouseEvent.scenePos().x() - self.decal.boundingRect().width()/2, mouseEvent.scenePos().y() - self.decal.boundingRect().height()/2)
            self.decal.setPos(insertedPos)
            #self.decalInserted.emit(decal)
            self.setMode(self.moveDecal)
        super(DecalScene, self).mousePressEvent(mouseEvent)
        
    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.moveDecal:
            if self.decal.isSelected() and mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.decalMoved.emit(self.cursorPos)    
            super(DecalScene, self).mouseMoveEvent(mouseEvent)
            #self.cursorPos = QtCore.QPointF(mouseEvent.scenePos())
            self.cursorPos = QtCore.QPointF(self.decal.posCustom())
            
    def mouseReleaseEvent(self, mouseEvent):
        super(DecalScene, self).mouseReleaseEvent(mouseEvent)
    
    def resizeEvent(self, event):
        print event.width()
            
    def updateScene(self):
        print self.sceneRect().width()

class DecalsForm(form_class,base_class):
    def __init__(self, backgroundImage, decalImage, parent = None):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.scene = DecalScene(backgroundImage, decalImage)
        self.graphicsView.setScene(self.scene)
        self.scene.decalMoved.connect(self.setValueSlider)
        self.graphicsView.show()
        
    def setValueSlider(self, QPointF):
        self.vSlider.setValue(QPointF.y()/550.0 * 100)
        self.hSlider.setValue(QPointF.x()/550.0 * 100)
        
    #def on_vSlider_valueChanged(self, value):
    #    hSlider = self.hSlider.value()
    #    self.scene.decal.setSignalPos(hSlider, value)
        
def __main__():
    app = QtGui.QApplication(sys.argv)
    backgroundImage = 'Z:/3D_Works/maya/Dropbox/wireframe.tif'
    decalsImage = 'Z:/3D_Works/maya/Dropbox/logo.tif'
    form = DecalsForm(backgroundImage, decalsImage)
    form.show()
    sys.exit(app.exec_())
    
__main__()