import maya.cmds as cmds

from PyQt4 import QtGui, QtCore, uic
import sip
import os, sys, inspect
import maya.OpenMayaUI as OpenMayaUI
from pymel.core import *
import functools 
import math, re
import pymel.core as py
import xml.dom.minidom as xml
import CommonFunctions as cf
import boltUvRatio
reload (boltUvRatio)
import Source.IconResource_rc
reload(Source.IconResource_rc)

#import PolyTools.ExporterandImporter
#reload(PolyTools.ExporterandImporter)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/UVRatio.ui'

form_class, base_class = uic.loadUiType(dirUI)

def getShaderFromNodes(node):
    try:
        shape = cmds.listRelatives(node, shapes = True)[0]
        #print 'listRelatives'
    except:
        shape = cmds.pickWalk(node, d = 'down')[0]
        #print 'pickWwalk'
    shadingGroups = list(set(py.listConnections(shape, type = 'shadingEngine')))
    if len(shadingGroups) == 0: # neu object khong co shader duoc gan thi khong can luu thong tin
        return False
    else:
        shadersList = []
        for shading in shadingGroups:
            if cmds.connectionInfo(shading + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(shading + '.surfaceShader', sfd = True).split('.')[0]
                shadersList.append(shader)
        return shadersList
    
def getFaceFromSelectedShaderAndSelectedMesh(shader, mesh):
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
            #attachFileSource = fileDirCommmon + '/detachComponent.mel'
            #mel.eval('source \"{f}\";'.format(f = attachFileSource))
            cmds.select(selectedFaces)
    else: # object has only one material
        #print 'select: ' + mesh
        cmds.select(mesh)
        
def getUVratioStatus(xmlPath):
    fStream = open(xmlPath)
    lines = fStream.readlines()
    for i in lines:
        result = re.search('(.*)bolt_uratio="(.*)', i, re.I)
        if result:
            return int(result.group(2)[0]) 
        
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class UVRatio(form_class,base_class):
     def __init__(self,parent = getMayaWindow()):
         super(base_class,self).__init__(parent)
         self.setupUi(self)
         self.btnGetUVRatio.clicked.connect(self.setUVratioOnUI)
         self.btnSetDefaultRatio.clicked.connect(self.setDefaultRatio)
         self.btnSetUVRatio.clicked.connect(self.setRatioToSelected)
         self.btnCheckUVRatio.clicked.connect(self.checkRatioOnScene)
         self.loadForm()
         
     def loadForm(self):
        self.listWidget.clear()
        nodes = cmds.ls(transforms = True)
        #mesh = []
        for n in nodes:
            try:
                childNode = cmds.listRelatives(n, shapes = True)
                if cmds.nodeType(childNode) not in ['camera','evoamboccvollocator']:
                    item = QtGui.QListWidgetItem(n)
                    self.listWidget.addItem(item)
            except:
                pass
                
     def on_listWidget_itemClicked(self, itemListWidget):
        self.listIcon.clear()
        mesh = itemListWidget.text()
        shaders = getShaderFromNodes(str(mesh))
        for shader in shaders:
            xmlPath = cmds.getAttr(shader + '.RawPath')
            iconPath = xmlPath.replace('.xml','_swatch_' + str(128) + '.bmp')
            #name = os.path.split(os.path.splitext(iconPath)[0])[1].replace('_swatch_' + str(128),'')
            icon = QtGui.QIcon(iconPath)
            paletteShaderItem = QtGui.QListWidgetItem(icon,shader,self.listIcon, QtGui.QListWidgetItem.Type)
            self.listIcon.addItem(paletteShaderItem)
            
     def on_listIcon_itemClicked(self, itemListWidget):
         shader = itemListWidget.text()
         mesh = self.listWidget.currentItem().text()
         getFaceFromSelectedShaderAndSelectedMesh(str(shader), str(mesh))
         
     def getUVRatio(self):
     	ratio = boltUvRatio.get_sel_faces_UV_ratio(1)
        return ratio
    
     def setUVratioOnUI(self):
         ratio = self.getUVRatio()
         self.ldtRatio.setText(str(1/ratio))
     	
     def setDefaultRatio(self):
     	self.ldtRatio.setText(str(25))
     	
     def setRatioToSelected(self):
     	boltUvRatio.collect_shells_and_set_shells_UV_ratio(float(self.ldtRatio.text()))
         
     def checkRatioOnScene(self):
         xmlDoc = xml.Document()
         root = xmlDoc.createElement('UVRatio')
         xmlDoc.appendChild(root)
         num = self.listWidget.count()
         for i in range(num):
             mesh = str(self.listWidget.item(i).text())
             meshNode = xmlDoc.createElement('mesh')
             meshNode.setAttribute('name', mesh)
             xmlDoc.appendChild(meshNode)
             shaders = getShaderFromNodes(mesh)
             for shader in shaders:
                 getFaceFromSelectedShaderAndSelectedMesh(str(shader), str(mesh))
                 xmlPath = cmds.getAttr(shader + '.RawPath')
                 if getUVratioStatus(xmlPath):
                     shaderNode = xmlDoc.createElement('shader')
                     shaderNode.setAttribute('name', shader)
                     if getUVratioStatus(xmlPath):# check if shader need to correct UV ratio
                         ratio = self.getUVRatio()
                     else:
                         ratio = 0
                 shaderNode.setAttribute('ratio', ratio)
                 meshNode.appendChild(shaderNode)
         cf.writeXML(xmlDoc,'C:\UvratioCheck.xml')
          
