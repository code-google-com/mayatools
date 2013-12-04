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
    
class shaderButton(QtGui.QAbstractButton):
    def __init__(self, mesh, shader, color):
        super(QtGui.QWidget, self).__init__(shader)
        self._mesh = mesh
        self._shader = shader
        self._color = color
        
    def pressedEvent(self, event):
        if self.isEnabled():
            self.update()
        st.selectFaceByShaderPerMesh(self._mesh, self._shader)
        
    def paintEvent(self):
        pass
    
class shaderDockMesh(dW.DockWidget):
    def __init__(self, mesh):
        super(dW.DockWidget).__init__(mesh)
        self._mesh = mesh
        self._vLayout = QtGui.QVLayout()
        self.setWidget(self._vLayout)
        
    def load(self):
        shaders = st.getShadersFromMesh(self._mesh)
        for s in shaders:
            button = shaderButton(self._mesh, s, green)
            self._vLayout.addWidget(button)
    
class shaderValidator(form_class, base_class):
    def __init__(self,parent = getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        
    def startup(self):
        shapeNode = py.ls(type = 'mesh')
    
        
    