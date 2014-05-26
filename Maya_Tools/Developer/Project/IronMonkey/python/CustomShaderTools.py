import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
from pymel.core import *
import functools, re
from xml.dom.minidom import *


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CustomShaderTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

class CustomShaderTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Shader Toolbox'
        self.material = list()
        self.commonTexturePath = os.path.split(fileDirCommmon)[0] + '/common_textures/'
        self.loadXML(os.path.split(fileDirCommmon)[0] + '/XMLfiles/IronMonkey_CustomNamingTool.xml')
        self.btnSetDamageShader.clicked.connect(self.tweakingDamageShader)

    def loadXML(self, xmlFile):
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        materialNode = root.getElementsByTagName('material')
        materialFromXML = [x.getAttribute('name') for x in materialNode if x.getAttribute('uvset') == '2_scratch']
        self.material = [x for x in materialFromXML if x in cmds.ls(materials = True)]
        

    def removeDebugShader(self):
        if cmds.objExists('restoreTechniqueNode'):
            cmds.scriptNode('restoreTechniqueNode', ea = True)
            cmds.delete('restoreTechniqueNode')
    
    def assignDebugShader(self, debugShader):
        restoreTechniqueScript = 'import maya.cmds as cmds\n'
        #commonPath = self.commonTexturePath
        shaders = [x for x in cmds.ls(materials = True)if x in self.material]#['lambert1','particleCloud1','shaderGlow1','TEMP_DEBUG_SHADER']]
        for shader in shaders:
            sgs = cmds.listConnections(shader,type = 'shadingEngine')
            for s in sgs:
                try:
                    cmds.connectAttr(debugShader + '.outColor', s + '.surfaceShader', f = True)
                except RuntimeError: # zero idea why Maya throw this error
                    pass
                restoreTechniqueScript += 'cmds.connectAttr(\'' + shader + '.outColor\',\'' + s + '.surfaceShader\', f = True)\n'
        restoreTechniqueScript += 'cmds.delete(\'' + debugShader + '\')\n'
        restoreTechniqueScript += 'cmds.delete(\'TEMP_DEBUG_TEXTURE\')\n'
        restoreTechniqueScript += 'glassTexturePath = \''  + self.commonTexturePath + 'car_glass_alpha.tif\'\n'
        restoreTechniqueScript += 'glassMat = cmds.ls(\'*glass_window_*\', materials = True)\n'
        restoreTechniqueScript += 'for s in glassMat:\n'
        restoreTechniqueScript += '\tfileNode = cmds.listConnections(s, s= True, t= \'file\')[0]\n'
        restoreTechniqueScript += '\tcmds.setAttr(fileNode + \'.fileTextureName\', glassTexturePath, type = \'string\')\n'
        print restoreTechniqueScript
        if cmds.objExists('restoreTechniqueNode'):
            cmds.delete('restoreTechniqueNode')
        else:
            cmds.scriptNode(st = 0, afterScript = restoreTechniqueScript, n = 'restoreTechniqueNode', stp = 'python')
                
    def tweakingDamageShader(self):
        cmds.undoInfo(openChunk = True)
        self.removeDebugShader()
        if self.btnSetDamageShader.isChecked():
            if cmds.objExists('TEMP_DEBUG_SHADER'):
                cmds.delete('TEMP_DEBUG_SHADER')
            else:
                mesh = list()
                sgs = [cmds.listConnections(x, type = 'shadingEngine') for x in self.material]
                for s in sgs:
                    print s
                    faceList = cmds.sets(s, q = True)
                    nodes = list(set([f.split('.')[0] for f in faceList])) 
                    mesh += nodes
                mesh = list(set(mesh))
                texturePath = self.commonTexturePath + 'car_scratch_mask.tif'
                glassTexture = self.commonTexturePath + 'car_glass_alpha_damage.tif'
                print glassTexture
                debugShader = cmds.shadingNode('lambert', n = 'TEMP_DEBUG_SHADER', asShader = True)
                texture = cmds.shadingNode('file',n = 'TEMP_DEBUG_TEXTURE', asTexture = True)
                cmds.setAttr(texture + '.fileTextureName', texturePath, type = 'string')
                cmds.connectAttr(texture + '.outColor',debugShader + '.color', f = True)
                glassMat = cmds.ls('*glass_window_*', materials = True)
                for s in glassMat:
                    try:
                        fileNode = cmds.listConnections(s, s= True, t= 'file')[0]
                        cmds.setAttr(fileNode + '.fileTextureName', glassTexture, type = 'string')
                    except:
                        pass
                for m in mesh:
                    try:
                        print m
                        id = cmds.polyUVSet(m, q= True, auv = True).index('2_scratch')              # avoid a bad case is two uvset are swapped to each other
                        result = cmds.uvLink(uvSet = m + '.uvSet[' + str(id) + '].uvSetName', t = texture)
                        print result
                    except ValueError:
                        print m + ' khong co uvset can co.'
                #cmds.undoInfo(openChunk = True)
                self.assignDebugShader(debugShader)
                #cmds.undoInfo(closeChunk = True)
        else:
            self.removeDebugShader()
        cmds.undoInfo(closeChunk = True)
            
def main():
    form = CustomShaderTools('')
    return form 

