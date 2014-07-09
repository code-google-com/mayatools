import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as py
import maya.mel as mel
import os, sys, inspect, re
import functools
from xml.dom.minidom import *
import pymel.core as pm
import pymel.core.datatypes as dt
from math import *
import sip

import CommonFunctions as cf


import ExporterandImporter
reload(ExporterandImporter)

import Source.IconResource_rc
reload(Source.IconResource_rc)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CommonTab.ui'

form_class, base_class = uic.loadUiType(dirUI)

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def isIdentity(transform):
    return cmds.xform(transform, query=True, matrix=True) == [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

presetNameforLeft = ['_L_','L_','left','LEFT','_FL_','_BL_','_RL_']
presetNameforRight = ['_R_','R_','right','RIGHT','_FR_','_BR_','_RR_']

def rearrangeEdgeList(edgeList, edge_01):
    orderedList = list()
    edge = edge_01
    stop = False
    while not stop:
        vertexes = cmds.polyListComponentConversion(edge, tv = True)
        connEdges_00 = cmds.polyListComponentConversion(vertex[0], te = True)
    
def attachMesh():
        # check shader assigned to faces before attaching
        attachFileSource = fileDirCommmon + '/mel/flattenCombine.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))

def detachMesh():
        attachFileSource = fileDirCommmon + '/mel/detachComponent.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        
def extractMesh():
        desMesh = cmds.ls(sl = True)[0].split('.')[0]
        midMesh = cmds.duplicate(desMesh, n = desMesh + '_duplicated' ,rr = True)[0]
        selectFaces = [x.replace(desMesh,midMesh) for x in cmds.ls(sl = True)]
        cmds.select(cl = True)
        cmds.select(selectFaces)
        mel.eval('InvertSelection')
        cmds.delete()
        cmds.select(midMesh)
        
def mirrorTool(axis, isKeepHistory, isClone, method):
        selObjs = cmds.ls(sl = True)
        for obj in selObjs:
            if axis == 'x':
                matchName = [x for x in presetNameforLeft if re.search(r'(.*)\{pattern}(\.*)'.format(pattern = x), obj)]
                if len(matchName):
                    index = presetNameforLeft.index(matchName[0])
                    newname = obj.replace(matchName[0], presetNameforRight[index])
                else:
                    matchName = [x for x in presetNameforRight if re.search(r'(.*)\{pattern}(\*.)'.format(pattern = x), obj)]
                    if len(matchName):
                        index = presetNameforRight.index(matchName[0])
                        newname = obj.replace(matchName[0], presetNameforLeft[index])
                    
            if isClone == 'Clone':
                if isKeepHistory:
                    try: 
                        dupMesh = cmds.duplicate(n = newname, ic = True)
                    except NameError:
                        dupMesh = cmds.duplicate(n = obj + '_mirrored', ic = True)
                else:
                    try:
                        dupMesh = cmds.duplicate(n = newname, ic = True)
                    except NameError:
                        dupMesh = cmds.duplicate(n = obj + '_mirrored', ic = False)
            elif isClone == 'Instance':
                try:
                    dupMesh = cmds.duplicate(n = newname, ilf = True)
                except NameError:
                    dupMesh = cmds.duplicate(n = obj + '_mirrored', ilf = True)
            else:
                dupMesh = [obj]
            if method == 'By axis':
                locator = cmds.spaceLocator()
                cmds.parent(dupMesh, locator)
                if axis == 'x':   
                    cmds.setAttr(locator[0] + '.scaleX', -1)
                if axis == 'y':   
                    cmds.setAttr(locator[0] + '.scaleY', -1)
                if axis == 'z':   
                    cmds.setAttr(locator[0] + '.scaleZ', -1)
                cmds.parent(dupMesh,world = True)
                cmds.delete(locator[0])
            elif method == 'By pivot':
                if axis == 'x':   
                    cmds.setAttr(dupMesh[0] + '.scaleX', -1)
                if axis == 'y':   
                    cmds.setAttr(dupMesh[0] + '.scaleY', -1)
                if axis == 'z':   
                    cmds.setAttr(dupMesh[0] + '.scaleZ', -1)
            #mel.eval('FreezeTransformations')
            cmds.makeIdentity(a = True, t = 1, r = 0, s = 1, n = 0)
            mel.eval('DeleteHistory')
            
            cmds.polyNormal(dupMesh, nm = 0, userNormalMode = 0)
            dupMeshShape = cmds.listRelatives(dupMesh, type = 'mesh', fullPath = True)
            cmds.setAttr(dupMeshShape[0] + '.opposite', False)
            cmds.select(cl = True)
            cmds.select(dupMesh)
            
def exportMesh():
        exp = ExporterandImporter.exporterShader()
        exp.exportMaya()
        
def importMesh():
        imp = ExporterandImporter.importerShader()
        imp.importMaya()

def editFlowEdges(edgeList):
    vertexes = cmds.polyListComponentConversion(edgeList, tv = True)
    #conjugateEdges = cmds.polyListComponentConversion(vertexes, te = True)
    #vertexesExpanding = cmds.polyListComponentConversion(conjugateEdges, tv = True)
    # filter 
    for v in vertexes:
        conjugateEdges = cmds.polyListComponentConversion(v, te = True)
        conjugateVertexes = cmds.polyListComponentConversion(conjugateEdges, te = True)
        filteredVertexes = [v for v in conjugateVertexes if v not in vertexes]
        interpolatePosition(v, filteredVertexes)
            
class CommonTab(form_class,base_class):
    closeTransferTool = QtCore.pyqtSignal('QString', name = 'closeTransferTool')
    def __init__(self, inputFile, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.__name__ = 'Poly tools'
        
    
                  
def main(xmlnput):
    form = CommonTab(xmlnput)
    return form 



    
