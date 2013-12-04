import inspect, os
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as OpenMayaUI
import sip
import functools

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
    
class shaderButton(QtGui.QPushButton):
    def __init__(self, mesh, shader, color):
        super(shaderButton, self).__init__()
        self._mesh = mesh
        self._shader = shader
        self._color = color
        self.setText(shader)
        self.clicked.connect(functools.partial(st.selectFaceByShaderPerMesh, self._mesh, self._shader))
        self.setStyleSheet('''QPushButton{
                            \ncolor: white;
                            \nbackground-color: qlineargradient(spread:pad, x1:0.478, y1:1, x2:0.467662, y2:0, stop:0 rgba(200, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
                            \nborder-color: #339;
                            \nborder-style: solid;
                            \nborder-radius: 5;
                            \npadding: 3px;
                            \nfont-size: 14px;
                            \npadding-left: 2px;
                            \npadding-right: 2px;}
                            
                            QPushButton:hover{
                            \ncolor: white;
                            \nbackground-color: qlineargradient(spread:pad, x1:0.478, y1:1, x2:0.467662, y2:0, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
                            \nborder-color: #339;
                            \nborder-style: solid;
                            \nborder-radius: 5;
                            \npadding: 3px;
                            \nfont-size: 14px;
                            \npadding-left: 2px;
                            \npadding-right: 2px;}
                        ''')

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
            button = shaderButton(self._mesh, s, "green")
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
            
    def reload(self):
        pass
        
    