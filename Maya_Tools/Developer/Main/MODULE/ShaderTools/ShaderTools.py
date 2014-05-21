import maya.cmds as cmds
import maya.mel as mel
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
import pymel.core as py
import functools, imp

import Source.IconResource_rc
import CommonFunctions as cf

checkerList = ['Custom_checker','IronMonkey_checker','Sony_checker_01', 'Sony_checker_02']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/ShaderTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

def getShadersFromMesh(mesh):                    
        # get shader from nodes
        shapeNode = cmds.listRelatives(mesh, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        if not sgs:
            return
        shaders = list()
        for sg in sgs:
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                shaders.append(shader)
        return list(set(shaders))
    
def getMeshfromShader(shader):
    sg = cmds.connectionInfo(shader + '.outColor', dfs = True).split('.')[0]
    members = cmds.sets(sg, q = True)
    
def getShaderFromSelectedFace(face):
        sg = cmds.listSets(type = 1, object = face)[0]
        shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
        return shader
        
    
def setShaderToSelectedFaces(shader):
    # get shadingGroup from shader
    selIns = cmds.ls(sl = True)
    cmds.select(cl = True)
    sg = cmds.connectionInfo(shader + '.outColor', dfs = True)
    if len(sg) == 0:#.split('.')[0]
        #sg = cmds.createNode('shadingEngine', n = shader + 'SG')
        sg = cmds.sets(r = True, nss = True,  n = shader + 'SG')
        #print sg
        cmds.connectAttr(shader + '.outColor', sg + '.surfaceShader', f = True )
        cmds.sets(selIns,e = True, forceElement = sg)
    else:
        sg = sg[0].split('.')[0]
    #cmds.select(selIns)
        cmds.sets(selIns, e = True, forceElement = sg)
    cmds.select(selIns)

def selectFaceByShaderPerMesh(mesh, shader, condition = False):
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
            if condition:
                cmds.select(mesh, a = True)
            else:
                cmds.select(mesh, r = True)
        else:
            if condition:
                cmds.select(selectedFaces, a = True)
            else:
                cmds.select(selectedFaces, r = True)
    else: # object has only one material
        #print 'select: ' + mesh
        if condition:
            cmds.select(mesh, a = True)
        else:
            cmds.select(mesh, r = True)
        
def selectFaceByShaderAllMesh(mesh, shader):
    # get shading group from shader
    try:
        shape = cmds.listRelatives(mesh, shapes = True)[0]
    except ValueError:
        return
    shadingGroups = py.listConnections(shader, type = 'shadingEngine')
    #print shadingGroups
    faceList = py.sets(shadingGroups, q = True)
    cmds.select(faceList)  
        
def selectMeshesUseShaderOnScene(shader):
    shadingGroups = py.listConnections(shader, type = 'shadingEngine')
    #print shadingGroups
    faceList = py.sets(shadingGroups, q = True)
    selectedMeshes = []
    for f in faceList:
        shapes = f.split('.')[0]
        selectedMeshes.append(shapes)
    return list(set(selectedMeshes))

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
        #self.chkRed.clicked.connect(self.updateSliderColorSet)
        #self.chkGreen.clicked.connect(self.updateSliderColorSet)
        #self.chkBlue.clicked.connect(self.updateSliderColorSet)
        #self.chkAlpha.clicked.connect(self.updateSliderColorSet)
        
        self.btnAssignMat.clicked.connect(self.assignMaterialToSelected)
        
        self.sldRed.valueChanged.connect(functools.partial(self.changeColorSet, 'r'))
        self.sldRed.sliderReleased.connect(self.fixColorSet)
        
        self.sldGreen.valueChanged.connect(functools.partial(self.changeColorSet, 'g'))
        self.sldGreen.sliderReleased.connect(self.fixColorSet)
        
        self.sldBlue.valueChanged.connect(functools.partial(self.changeColorSet, 'b'))
        self.sldBlue.sliderReleased.connect(self.fixColorSet)
        
        self.sldAlpha.valueChanged.connect(functools.partial(self.changeColorSet, 'a'))
        self.sldAlpha.sliderReleased.connect(self.fixColorSet)
        
        self.btnGetRed.clicked.connect(functools.partial(self.getVertexColor, 'r'))
        self.btnSetRed.clicked.connect(functools.partial(self.setVertexColor, 'r'))
        
        self.btnGetGreen.clicked.connect(functools.partial(self.getVertexColor, 'g'))
        self.btnSetGreen.clicked.connect(functools.partial(self.setVertexColor, 'g'))
        
        self.btnGetBlue.clicked.connect(functools.partial(self.getVertexColor, 'b'))
        self.btnSetBlue.clicked.connect(functools.partial(self.setVertexColor, 'b'))
        
        self.btnGetAlpha.clicked.connect(functools.partial(self.getVertexColor, 'a'))
        self.btnSetAlpha.clicked.connect(functools.partial(self.setVertexColor, 'a'))
        
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
        
        #self.updateSliderColorSet()
        
        attachFileSource = fileDirCommmon + '/mel/fixVertexColor.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        
        self.updateShaderOnFaceSelected = cmds.scriptJob(e = ['SelectionChanged',self.updateShaderName], protected = True)
        self.updateShaderOnScene = cmds.scriptJob(e = ['SceneOpened',self.updateShaderScene], protected = True)
        
        self.updateShaderScene()
        
    def updateShaderName(self):
        obj = cmds.ls(sl = True,fl = True)
        if len(obj) == 1:
            if '.f[' in obj[0]:
                shader = getShaderFromSelectedFace(obj[0])
                index = self.cbbShadersScene.model().stringList().indexOf(shader)
                print index
                if index == -1:
                    print 'No found'
                    self.cbbShadersScene.setCurrrentIndex(0)
                else:
                    print 'Found'
                    self.cbbShadersScene.setCurrrentIndex(index)

                
#     def updateSliderColorSet(self):
#         if self.chkRed.isChecked():
#             self.sldRed.setEnabled(True)
#         else:
#             self.sldRed.setEnabled(False)
#             
#         if self.chkGreen.isChecked():
#             self.sldGreen.setEnabled(True)
#         else:
#             self.sldGreen.setEnabled(False)
#             
#         if self.chkBlue.isChecked():
#             self.sldBlue.setEnabled(True)
#         else:
#             self.sldBlue.setEnabled(False)
#             
#         if self.chkAlpha.isChecked():
#             self.sldAlpha.setEnabled(True)
#         else:
#             self.sldAlpha.setEnabled(False)
        
        
    def removeDebugShader(self):
        if cmds.objExists('restoreTechniqueNode'):
            cmds.scriptNode('restoreTechniqueNode', ea = True)
            cmds.delete('restoreTechniqueNode')
            
    def assignDebugShader(self):
        restoreTechniqueScript = 'import maya.cmds as cmds\n'
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
        cmds.undoInfo(openChunk = True)
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
            #cmds.undoInfo(openChunk = True)
            self.assignDebugShader()
            #cmds.undoInfo(closeChunk = True)
        else:
            self.removeDebugShader()
        cmds.undoInfo(closeChunk = True)
            
    def tweakingNormalView(self):
        cmds.undoInfo(openChunk = True)
        self.removeDebugShader()
        if self.btnNormalView.isChecked():
            debugShader = cmds.shadingNode('cgfxShader', n = 'TEMP_DEBUG_SHADER', asShader = True)
            textureNode = cmds.shadingNode('file',n = 'TEMP_DEBUG_TEXTURE', asTexture = True)
            cmds.cgfxShader('TEMP_DEBUG_SHADER', fx = self._shaders + 'KoddeShader_v0.7.cgfx', e = True)
            cmds.setAttr('TEMP_DEBUG_SHADER.Display_Camera_Normals', True)
            #cmds.undoInfo(openChunk = True)
            self.assignDebugShader()
            #cmds.undoInfo(closeChunk = True)
        else:
            self.removeDebugShader()
        cmds.undoInfo(closeChunk = True)
            
    def tweakingShininessView(self):
        cmds.undoInfo(openChunk = True)
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
            cmds.undoInfo(openChunk = True)
            self.assignDebugShader()
            cmds.undoInfo(closeChunk = True)
        else:
            self.removeDebugShader()
        cmds.undoInfo(closeChunk = True)
            
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
            
    def changeColorSet(self, channel = None):
        #colorSet = str(self.cbbColorSet.currentText())
        
        currentValue = self.sldRed
        cmds.polyColorSet(cs = 'colorSet1', ccs = True)
        cmds.polyColorPerVertex(cla = True)
        if channel == 'r':
            value = (-self.sldRed.value()/100.00)
            #print value
            cmds.polyColorPerVertex(r = value)
        if channel == 'g':
            value = self.sldGreen.value()
            cmds.polyColorPerVertex( g = value)
        if channel == 'b':
            value = self.sldBlue.value()
            cmds.polyColorPerVertex(b = value)
        if channel == 'a':
            value = self.sldAlpha.value()
            cmds.polyColorPerVertex( a = value)
            
    def fixColorSet(self):
        mel.eval('boltSCV.fixVertexColours')
    
    def updateShaderScene(self):
        self.cbbShadersScene.clear()
        shaderList = cmds.ls(mat = True)
        self.cbbShadersScene.addItems(sorted(shaderList))
        
    def assignMaterialToSelected(self):
        shader = str(self.cbbShadersScene.currentText())
        setShaderToSelectedFaces(shader)
    
    def getVertexColor(self, channel):
        selVertexes = cmds.ls(sl = True)
        value = 0.0
        for v in selVertexes:
            if channel == 'r':
                value += cmds.polyColorPerVertex(q= True, r = True)[0]
            if channel == 'g':
                value += cmds.polyColorPerVertex(q= True, g = True)[0]
            if channel == 'b':
                value += cmds.polyColorPerVertex(q= True, b = True)[0]
            if channel == 'a':
                value += cmds.polyColorPerVertex(q= True, a = True)[0]
        value /= len(selVertexes)
        cf.setDataToClipboard(str(value))
    
    def setVertexColor(self, channel):
        try:
            value = float(cf.getDataFromClipboard())
        except ValueError:
            QtGui.QMessageBox.information(self,'Invalid number','Khong the gan vertex color voi gia tri mau dang chon.',QtGui.QMessageBox.Ok)
            return
        if channel == 'r':
            cmds.polyColorPerVertex(r = value)
        if channel == 'g':
            cmds.polyColorPerVertex(g = value)
        if channel == 'b':
            cmds.polyColorPerVertex(b = value)
        if channel == 'a':
            cmds.polyColorPerVertex(a = value)
  
def main(xmlnput):
    form = ShaderTools(xmlnput)
    return form 

