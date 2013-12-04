import inspect, os
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as OpenMayaUI
import sip

from MODULE.ShaderTools import ShaderTools as st
reload(st)

from MODULE.PolyTools import PolyTools as pt
reload(pt)

import CommonFunctions as cf
reload(cf)

import dockWidget as dW
reload(dW)

description = 'Select Mesh using wrong shader'
name = 'selectWrongShaderNode'

fileDirCommmon = os.path.split(os.path.split(inspect.getfile(inspect.currentframe()))[0])[0]
dirUI= fileDirCommmon +'/UI/shader_Validator.ui'
try:    
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found.')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def execute():
    form = shaderValidator()
    form.show()
    
class shaderButton(QtGui.QWidget):
    def __init__(self, mesh, shader, color):
        super(shaderButton, self).__init__()
        self._mesh = mesh
        self._shader = shader
        self._color = color
        self.setText(shader)
        
    def enterEvent(self, event):
        if self.isEnabled():
            self.update()
        QAbstractButton.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.update()
        QAbstractButton.leaveEvent(self, event)
        
    def paintEvent(self, event):
        p = QPainter(self)
        r = self.rect()
        opt = QStyleOptionToolButton()
        opt.init(self)
        opt.state |= QStyle.State_AutoRaise
        if self.isEnabled() and self.underMouse() and \
           not self.isChecked() and not self.isDown():
            opt.state |= QStyle.State_Raised
        if self.isChecked():
            opt.state |= QStyle.State_On
        if self.isDown():
            opt.state |= QStyle.State_Sunken
        self.style().drawPrimitive(
            QStyle.PE_PanelButtonTool, opt, p, self)
        opt.icon = self.icon()
        opt.subControls = QStyle.SubControls()
        opt.activeSubControls = QStyle.SubControls()
        opt.features = QStyleOptionToolButton.None
        opt.arrowType = Qt.NoArrow
        size = self.style().pixelMetric(QStyle.PM_SmallIconSize, None, self)
        opt.iconSize = QSize(size, size)
        self.style().drawComplexControl(QStyle.CC_ToolButton, opt, p, self)
        
        
class shaderDockWidget(dW.DockWidget):
    def __init__(self, mesh):
        super(shaderDockWidget, self).__init__(mesh)
        self._mesh = mesh
        self._widget= QtGui.QWidget()
        self.setWidget(self._widget)
        self.load()
        
    def load(self):
        layout = QtGui.QVBoxLayout()
        margins = QtCore.QMargins(1,1,1,1)
        layout.setSpacing(1)
        layout.setContentsMargins(margins) 
        self._widget.setLayout(layout)
        shaders = st.getShadersFromMesh(self._mesh)
        for s in shaders:
            #button = shaderButton(self._mesh, s, "green")
            button = QtGui.QPushButton(s)
            layout.addWidget(button)
    
class shaderValidator(form_class, base_class):
    def __init__(self,parent = getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.startup()
        
    def startup(self):
        shapeNode = [node for node in py.ls(type = 'transform') if py.nodeType(node.listRelatives(c= True)) == 'mesh'] 
        for node in shapeNode:
            dockWidget = shaderDockWidget(str(node))
            self.formLayout.addWidget(dockWidget)
    
        
    