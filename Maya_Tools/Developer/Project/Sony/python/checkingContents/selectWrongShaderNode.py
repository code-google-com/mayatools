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

color_code = {'right':['00dc00', '00ff00'], 'wrong':['fa0000','ff0000'], 'missing':['ffdc00','ffff00']}

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
        #self._color = color
        self.setText(shader)
        self.clicked.connect(functools.partial(st.selectFaceByShaderPerMesh, self._mesh, self._shader))
        self.setStyleSheet('''QPushButton*
                            color: black;
                            background-color: #{color0};
                            border-color: #339;
                            border-style: solid;
                            border-radius: 5;
                            padding: 3px;
                            font-size: 14px;
                            padding-left: 2px;
                            padding-right: 2px;@
                            
                            QPushButton:hover*
                            color: black;
                            background-color: #{color1};
                            border-color: #339;
                            border-style: solid;
                            border-radius: 5;
                            padding: 3px;
                            font-size: 14px;
                            padding-left: 2px;
                            padding-right: 2px;@'''.format(color0 = color[0], color1 = color[1]).replace('*','{').replace('@','}'))
        
    def checkShader(self):
        pass
        
class shaderDockWidget(dW.DockWidget):
    def __init__(self, mesh):
        super(shaderDockWidget, self).__init__(mesh)
        self._mesh = mesh
        self._widget= QtGui.QWidget()
        self.setWidget(self._widget)
        self.load()
        
    def checkShader(self, mesh, shader):
        return 'wrong'
        
    def load(self):
        layout = QtGui.QVBoxLayout()
        margins = QtCore.QMargins(1,1,1,1)
        layout.setSpacing(1)
        layout.setContentsMargins(margins) 
        self._widget.setLayout(layout)
        shaders = st.getShadersFromMesh(self._mesh)
        for s in shaders:
            result = self.checkShader(self._mesh, s)
            button = shaderButton(self._mesh, s, color_code[result])
            layout.addWidget(button)
    
class shaderValidator(form_class, base_class):
    def __init__(self,parent = getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.startup()
        
    def startup(self):
        shapeNode = [node for node in py.ls(type = 'transform') if py.nodeType(node.listRelatives(c= True)[0]) == 'mesh'] 
        for node in shapeNode:
            dockWidget = shaderDockWidget(str(node))
            self.formLayout.addWidget(dockWidget)
            
    def reload(self):
        pass
        
    