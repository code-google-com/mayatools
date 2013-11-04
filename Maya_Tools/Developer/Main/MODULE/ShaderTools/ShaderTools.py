import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
from pymel.core import *
import functools, imp


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/ShaderTools.ui'

form_class, base_class = uic.loadUiType(dirUI)  

def loadModule(path ,moduleName):
    sys.path.append(path)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()

cmds.loadPlugin('cgfxShader.mll')  

class ShaderTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Shader Toolbox'
        self._textures = fileDirCommmon + '/textures/'
        self._shaders = fileDirCommmon + '/shaders/'
        self.statusScene = 1
        self.btnShowAOOnly.clicked.connect(self.switchStatusScene)
        self.btnCheckerView.clicked.connect(self.tweakingCheckerShader)
        self.btnNormalView.clicked.connect(self.tweakingNormalView)
        if inputFile != '':
            project = inputFile.split('.')[0]
            customFn = inputFile.split('.')[1]
            customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
            instanceModule = loadModule(customPath + '/Project/' + project + '/python', customFn)
            form = instanceModule.main()
            self.customUI.addWidget(form)
        
    def removeDebugShader(self):
        if cmds.objExists('restoreTechniqueNode'):
            cmds.scriptNode('restoreTechniqueNode', ea = True)
            cmds.delete('restoreTechniqueNode')
            
    def assignDebugShader(self):
        restoreTechniqueScript = ''
        #commonPath = self.commonTexturePath
        shaders = [x for x in cmds.ls(materials = True)if x not in ['lambert1','particleCloud1','shaderGlow1','TEMP_DEBUG_SHADER']]
        for shader in shaders:
            sgs = cmds.listConnections(shader,type = 'shadingEngine')
            for s in sgs:
                try:
                    cmds.connectAttr('TEMP_DEBUG_SHADER' + '.outColor', s + '.surfaceShader', f = True)
                except RuntimeError: # zero idea why Maya throw this error
                    pass
                restoreTechniqueScript += 'cmds.connectAttr(\'' + shader + '.outColor\',\'' + s + '.surfaceShader\', f = True)\n'
        restoreTechniqueScript += 'cmds.delete(\'TEMP_DEBUG_SHADER\')\n'
        restoreTechniqueScript += 'cmds.delete(\'TEMP_DEBUG_TEXTURE\')\n'
        print restoreTechniqueScript
        if cmds.objExists('restoreTechniqueNode'):
            cmds.delete('restoreTechniqueNode')
        else:
            cmds.scriptNode(st = 0, afterScript = restoreTechniqueScript, n = 'restoreTechniqueNode', stp = 'python')
            
    def switchStatusScene(self):
        mesh = cmds.ls(type = 'mesh')[0]
        selObjs = cmds.ls(sl = True) 
        if self.statusScene == 0: # display AO only
            cmds.polyOptions(mesh, gl = True, cs = True, cm = 'none', mb = 'Overwrite')
            self.btnShowAOOnly.setIcon(QtGui.QIcon(':/Project/AO.png'))
            self.statusScene = 1
        elif self.statusScene == 1: # display Abedo not include AO
            cmds.polyOptions(mesh, gl = True, cs = False, cm = 'none', mb = 'Overwrite')
            self.btnShowAOOnly.setIcon(QtGui.QIcon(':/Project/diffuse.png'))
            self.statusScene = 2
        elif self.statusScene == 2: # display Abedo include AO
            cmds.polyOptions(mesh, gl = True, cs = True, cm = 'ambientDiffuse', mb = 'Multiply')
            self.btnShowAOOnly.setIcon(QtGui.QIcon(':/Project/DiffuseAO.png'))
            self.statusScene = 0
            
    def tweakingCheckerShader(self):
        self.removeDebugShader()
        if self.btnCheckerView.isChecked():
            debugShader = cmds.shadingNode('lambert', n = 'TEMP_DEBUG_SHADER', asShader = True)
            textureNode = cmds.shadingNode('file',n = 'TEMP_DEBUG_TEXTURE', asTexture = True)
            #tilingNode = cmds.
            cmds.setAttr('TEMP_DEBUG_TEXTURE.fileTextureName',self._textures + 'custom_uv_diag.png', type = 'string')
            cmds.connectAttr(textureNode + '.outColor', debugShader + '.color')
            self.assignDebugShader()
        else:
            self.removeDebugShader()
            
    def tweakingNormalView(self):
        self.removeDebugShader()
        if self.btnNormalView.isChecked():
            debugShader = cmds.shadingNode('cgfxShader', n = 'TEMP_DEBUG_SHADER', asShader = True)
            textureNode = cmds.shadingNode('file',n = 'TEMP_DEBUG_TEXTURE', asTexture = True)
            cmds.cgfxShader('TEMP_DEBUG_SHADER', fx = self._shaders + 'KoddeShader_v0.7.cgfx', e = True)
            cmds.setAttr('TEMP_DEBUG_SHADER.Display_Camera_Normals', True)
            self.assignDebugShader()
        else:
            self.removeDebugShader()

def main(xmlnput):
    form = ShaderTools(xmlnput)
    return form 

