import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
import pymel.core as py
import functools, imp

import Source.IconResource_rc

checkerList = ['Custom_checker','IronMonkey_checker','Sony_checker_01', 'Sony_checker_02']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/ShaderTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

def getShadersFromMesh(mesh):                    
        # get shader from nodes
        shapeNode = cmds.listRelatives(mesh, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        if not sgs:
            print mesh
            return
        shaders = list()
        for sg in sgs:
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                shaders.append(shader)
        return list(set(shaders))
    
def setShaderToSelectedFaces(selFaces, shader):
    # get shadingGroup from shader
    sg = cmds.connectionInfo(shader + '.outColor', dfs = True).split('.')[0]
    cmds.sets(selFaces, e = True, forceElement = sg)

def selectFaceByShaderPerMesh(mesh, shader):
    # get shading group from shader
    try:
        shape = cmds.listRelatives(mesh, shapes = True)[0]
    except ValueError:
        return
    shadingGroups = py.listConnections(shader, type = 'shadingEngine')
    #print shadingGroups
    faceList = py.sets(shadingGroups, q = True)
    #print faceList
    selectedFaces = []
    for f in faceList:
        shapefromFace = f.split('.')[0]
        if shapefromFace == shape:
            selectedFaces.append(f)
    #print selectedFaces
    if shape not in selectedFaces:
        cmds.select(selectedFaces)
        if len(cmds.ls(sl = True, fl = True)) == cmds.polyEvaluate(mesh, f = True):# in case selected faces is equal to the number of  faces
            cmds.select(mesh)
        else:
            cmds.select(selectedFaces)
    else: # object has only one material
        #print 'select: ' + mesh
        cmds.select(mesh)  

def reassignShaderToFace(mesh, shader):
    selectFaceByShaderPerMesh(mesh, shader)
    isFaces = py.ls(sl = True)

def loadModule(path ,moduleName):
    sys.path.append(path)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()

cmds.loadPlugin('cgfxShader.mll')  

class shaderDebug(QtGui.QPushButton):
    def __init__(self, ):
        pass
    
class ShaderTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Shader&Color Toolbox'
        self._textures = [texture for texture in os.listdir(fileDirCommmon + '/textures/') if texture.endswith('tif') ]
        self._shaders = fileDirCommmon + '/shaders/'
        self.statusScene = 1
        
        self.btnShowAOOnly.clicked.connect(self.switchStatusScene)
        self.btnCheckerView.clicked.connect(self.tweakingCheckerShader)
        self.btnNormalView.clicked.connect(self.tweakingNormalView)
        self.btnReflectionView.clicked.connect(self.tweakingShininessView)
        
        self.btnCheckerView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        if inputFile != '':
            project = inputFile.split('.')[0]
            customFn = inputFile.split('.')[1]
            customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
            instanceModule = loadModule(customPath + '/Project/' + project + '/python', customFn)
            form = instanceModule.main()
            self.customUI.addWidget(form)
       
        # add Combobox to change checker texture
        self.combobox = QtGui.QComboBox(self)
        for c in self._textures:
            icon = QtGui.QIcon(':/Project/' + os.path.split(c)[1])
            self.combobox.addItem(icon, os.path.splitext(os.path.split(c)[1])[0])
        self.combobox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.actionSwitch = QtGui.QWidgetAction(self.combobox)
        self.actionSwitch.setDefaultWidget(self.combobox)
        self.btnCheckerView.addAction(self.actionSwitch)
        
         # add slider to adjust checker size    
        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation (QtCore.Qt.Horizontal)
        self.slider.setMaximum(10)
        self.slider.setMinimum(1)
        self.actionSlide = QtGui.QWidgetAction(self.slider)
        self.actionSlide.setDefaultWidget(self.slider)
        self.btnCheckerView.addAction(self.actionSlide)
        
        #----------
        self.combobox.currentIndexChanged.connect(self.updateChecker)
        self.slider.valueChanged.connect(self.updateTilingChecker)
        
    def removeDebugShader(self):
        if cmds.objExists('restoreTechniqueNode'):
            cmds.scriptNode('restoreTechniqueNode', ea = True)
            cmds.delete('restoreTechniqueNode')
            
    def assignDebugShader(self):
        restoreTechniqueScript = ''
        #commonPath = self.commonTexturePath
        shaders = [x for x in cmds.ls(materials = True)if x not in ['particleCloud1','shaderGlow1','TEMP_DEBUG_SHADER']]
        for shader in shaders:
            try:
                sgs = cmds.listConnections(shader,type = 'shadingEngine')
                for s in sgs:
                    try:
                        cmds.connectAttr('TEMP_DEBUG_SHADER' + '.outColor', s + '.surfaceShader', f = True)
                    except RuntimeError: # zero idea why Maya throw this error
                        pass
                    restoreTechniqueScript += 'cmds.connectAttr(\'' + shader + '.outColor\',\'' + s + '.surfaceShader\', f = True)\n'
            except:
                pass
        restoreTechniqueScript += 'cmds.select(\'*TEMP_DEBUG*\')\n'
        restoreTechniqueScript += 'cmds.delete()\n'
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
            utilityNode = cmds.shadingNode('place2dTexture', n = 'TEMP_DEBUG_UTILITY', asUtility = True)
            cmds.setAttr('TEMP_DEBUG_TEXTURE.fileTextureName',fileDirCommmon + '/textures/Custom_checker.tif', type = 'string')
            #---
            cmds.connectAttr(utilityNode + '.outUV', textureNode +  '.uvCoord')
            cmds.connectAttr(utilityNode + '.outUvFilterSize', textureNode + '.uvFilterSize')
            cmds.connectAttr(utilityNode + '.coverage', textureNode + '.coverage') 
            cmds.connectAttr(utilityNode + '.translateFrame', textureNode + '.translateFrame') 
            cmds.connectAttr(utilityNode + '.rotateFrame', textureNode + '.rotateFrame') 
            cmds.connectAttr(utilityNode + '.mirrorU', textureNode + '.mirrorU') 
            cmds.connectAttr(utilityNode + '.mirrorV', textureNode + '.mirrorV') 
            cmds.connectAttr(utilityNode + '.stagger', textureNode + '.stagger') 
            cmds.connectAttr(utilityNode + '.wrapU', textureNode + '.wrapU')
            cmds.connectAttr(utilityNode + '.wrapV', textureNode + '.wrapV') 
            cmds.connectAttr(utilityNode + '.repeatUV', textureNode + '.repeatUV')
            cmds.connectAttr(utilityNode + '.vertexUvOne', textureNode + '.vertexUvOne')
            cmds.connectAttr(utilityNode + '.vertexUvTwo', textureNode + '.vertexUvTwo') 
            cmds.connectAttr(utilityNode + '.vertexUvThree', textureNode + '.vertexUvThree')
            cmds.connectAttr(utilityNode + '.vertexCameraOne', textureNode  + '.vertexCameraOne')
            cmds.connectAttr(utilityNode + '.noiseUV', textureNode + '.noiseUV')
            cmds.connectAttr(utilityNode + '.offset', textureNode + '.offset')
            cmds.connectAttr(utilityNode + '.rotateUV', textureNode + '.rotateUV')
            #---
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
        
            
    def tweakingShininessView(self):
        self.removeDebugShader()
        if self.btnReflectionView.isChecked():
            debugShader = cmds.shadingNode('cgfxShader', n = 'TEMP_DEBUG_SHADER', asShader = True)
            textureNode = cmds.shadingNode('file',n = 'TEMP_DEBUG_TEXTURE', asTexture = True)
            cmds.cgfxShader('TEMP_DEBUG_SHADER', fx = self._shaders + 'GenericBRDF_1-0.cgfx', e = True)
            cmds.setAttr('TEMP_DEBUG_SHADER.SpecFactor', 0.903226)
            cmds.setAttr('TEMP_DEBUG_SHADER.EmissiveFactor', 0.154839)
            cmds.setAttr('TEMP_DEBUG_SHADER.EmissiveColor', 0, 0, 0, type = 'double3')
            cmds.setAttr('TEMP_DEBUG_SHADER.FresnelPower', 0.01)
            cmds.setAttr('TEMP_DEBUG_SHADER.ReflectionBlurFactor', 1.806452)
            cmds.setAttr('TEMP_DEBUG_SHADER.AmbientFactor', 0.296774)
            cmds.setAttr('TEMP_DEBUG_SHADER.AmbientBlurFactor', 1.612903)
            cmds.setAttr('TEMP_DEBUG_SHADER.ReflectionBlurFactor', 1.806452)
            cmds.setAttr('TEMP_DEBUG_SHADER.SpecularFresnelPower', -0.143)
            cmds.setAttr('TEMP_DEBUG_SHADER.GlossFactor', 0.419355)
            cmds.setAttr('TEMP_DEBUG_SHADER.EmissiveColor', 0, 0.940394, 1, type = 'double3')
            #cmds.setAttr('TEMP_DEBUG_SHADER.vertexAttributeSource', ['position', 'normal', '', 'uv:map1', 'tangent:map1', 'binormal:map1'], type = 'stringArray')
            fileNode = cmds.connectionInfo('TEMP_DEBUG_SHADER.diffuseSampler', sfd = True).split('.')[0]
            #cmds.setAttr(fileNode + '.fileTextureName',fileDirCommmon + '/textures/BasketballCourt_3k.hdr', type = 'string')
            self.assignDebugShader()
        else:
            self.removeDebugShader()
            
    def updateTilingChecker(self):
        value = self.slider.value()
        if cmds.objExists('TEMP_DEBUG_UTILITY'):
            node = py.ls('TEMP_DEBUG_UTILITY')[0]
            node.setAttr('repeatU', value)
            node.setAttr('repeatV', value)
            
    def updateChecker(self):
        texture = self.combobox.currentText() 
        if cmds.objExists('TEMP_DEBUG_TEXTURE'):
            node = py.ls('TEMP_DEBUG_TEXTURE')[0]
            cmds.setAttr('TEMP_DEBUG_TEXTURE.fileTextureName', fileDirCommmon + '/textures/' + texture + '.tif', type = 'string')
        
def main(xmlnput):
    form = ShaderTools(xmlnput)
    return form 

