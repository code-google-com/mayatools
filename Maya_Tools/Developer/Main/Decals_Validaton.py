import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI
import os, sys, re, inspect , imp, shutil
import math
from pymel.core import *
from PySide import QtGui, QtCore
import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO
import shiboken
import functools

#fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
#dirUI= fileDirCommmon +'/UI/Decal_Form.ui'
dirUI = 'D:/maya_Tools/Maya_Tools/Developer/Main/UI/Decal_Form.ui'

def wrapinstance(ptr, base=None):
    if ptr is None:
        return None
    ptr = long(ptr) #Ensure type
    if globals().has_key('shiboken'):
        if base is None:
            qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(long(ptr), base)
    elif globals().has_key('sip'):
        base = QtCore.QObject
        return sip.wrapinstance(long(ptr), base)
    else:
        return None


def loadUiType(uiFile):

        parsed = xml.parse(uiFile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text
    
        with open(uiFile, 'r') as f:
            o = StringIO()
            frame = {}
            
            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame
            
            #Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('QtGui.%s'%widget_class)
        return form_class, base_class

try:
    #form_class, base_class = uic.loadUiType(dirUI)
    form_class, base_class = loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapinstance(long(ptr), QtGui.QWidget)

class Decal(QtGui.QGraphicsPixmapItem):
    
    decalScaled = QtCore.Signal(QtCore.QPointF)
        
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
        if self.scaleFactor < 0.35: 
            self.scaleFactor = 0.5
        if self.scaleFactor > 2:
            self.scaleFactor = 2
        self.setScale(self.scaleFactor)
        self.decalScaled.emit(self.scaleFactor)
        
    def setSignalPos(self, dx, dy):
        pos = QtCore.QPointF(dx * 550 / 100.0 - self.boundingRectCustom().width()/2, dy * 550 / 100.0 - self.boundingRectCustom().height()/2)
        self.setPos(pos)
        
    def getCenter(self):
        return self.transformOriginPoint() 
        
    def setCenter(self):
        pos = QtCore.QPointF()
        pos.setX(self.boundingRectCustom().width()/2)
        pos.setY(self.boundingRectCustom().height()/2)
        return pos        
        
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
    
    decalMoved = QtCore.Signal(QtCore.QPointF)
    
    def __init__(self, bg, dc, parent = None):
        super(DecalScene, self).__init__(0, 0, 550, 550, parent)
        self._backgroundImage = QtGui.QPixmap(bg).scaled(self.sceneRect().width(), self.sceneRect().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self._decalImage = QtGui.QPixmap(dc)
        self.myMode = self.insertDecal
        self.cursorPos = QtCore.QPointF()
        self.decal = Decal(self._decalImage)
        self.originRatio = 550.0/self.decal.boundingRect().height()
        
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
            self.setMode(self.moveDecal)
        super(DecalScene, self).mousePressEvent(mouseEvent)
        
    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.moveDecal:
            if self.decal.isSelected() and mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.decalMoved.emit(self.cursorPos)    
            super(DecalScene, self).mouseMoveEvent(mouseEvent)
            self.cursorPos = QtCore.QPointF(self.decal.posCustom())
            
    def mouseReleaseEvent(self, mouseEvent):
        super(DecalScene, self).mouseReleaseEvent(mouseEvent)


class DecalsForm(form_class,base_class):
    def __init__(self, backgroundImage, decalImage, parent = getMayaWindow()):
        super(DecalsForm,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.scene = DecalScene(backgroundImage, decalImage)
        self.graphicsView.setScene(self.scene)
        self.scene.decalMoved.connect(self.setValueSlider)
        self.scene.decal.decalScaled.connect(self.setScaleDecal)
        self.hSlider.valueChanged.connect(self.updateDecalPos)
        self.vSlider.valueChanged.connect(self.updateDecalPos)
        self.graphicsView.show()
        self.startup()
        
    def startup(self):
        if cmds.objExists('DEBUG_UTILITY'):
            cmds.setAttr('DEBUG_UTILITY.repeatV', self.scene.originRatio)
            cmds.setAttr('DEBUG_UTILITY.repeatU', self.scene.originRatio)
        
    def setValueSlider(self, QPointF):
        self.vSlider.setValue(QPointF.y()/550.0 * 100)
        self.hSlider.setValue(QPointF.x()/550.0 * 100)
        cmds.setAttr('DEBUG_UTILITY.offsetU', -QPointF.x()/self.scene.decal.boundingRectCustom().width() + 0.5)
        cmds.setAttr('DEBUG_UTILITY.offsetV', -(550 - QPointF.y())/self.scene.decal.boundingRectCustom().width() + 0.5)
        
    def setScaleDecal(self, factor):
        cmds.setAttr('DEBUG_UTILITY.repeatV', 550.0/float(factor))
        cmds.setAttr('DEBUG_UTILITY.repeatU', 550.0/float(factor))
        
    def updateDecalPos(self):
        hValue = self.hSlider.value()
        vValue = self.vSlider.value()
        self.scene.decal.setSignalPos(hValue, vValue)
        

backgroundImage = 'D:/3D_Works/Dropbox/wireframe.tif'
decalsImage = 'D:/3D_Works/Dropbox/logo.tif'
form = DecalsForm(backgroundImage, decalsImage)
form.show()
    