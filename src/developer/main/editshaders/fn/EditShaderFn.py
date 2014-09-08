import maya.cmds as cmds
import maya.mel as mel
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
import pymel.core as py
import pymel.core.datatypes as dt
import functools, imp

checkerList = ['Custom_checker','IronMonkey_checker','Sony_checker_01', 'Sony_checker_02']

def getShadersFromMesh(mesh):                    
        # get shader from nodes
        shapeNode = mesh.listRelatives(c = True, f = True)[0]
        sgs = shapeNode.listConnections(t = 'shadingEngine')
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
    if len(selectedFaces) == cmds.polyEvaluate(mesh, f = True):# in case selected faces is equal to the number of  faces
        if condition:
            cmds.select(mesh, add = True)
        else:
            cmds.select(mesh, r = True)
    else:
        if condition:
            cmds.select(selectedFaces, add = True)
        else:
            cmds.select(selectedFaces, r = True)

def selectFaceByShaderAllMesh(shader):
    # get shading group from shader
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



