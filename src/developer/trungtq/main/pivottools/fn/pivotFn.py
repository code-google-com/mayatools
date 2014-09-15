# -- import maya packages

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import pymel.core.datatypes as dt
from pymel.core.general import PyNode

# -- import python standard packages

import os, sys, inspect, decimal

# -- import 3rd packages

from PyQt4 import QtGui, QtCore

#-- ending import prerequisites

def zeroPivotOffset(node):
    '''
        Get world transformation of node, apply this button whenever export to game engine.
    '''
    currWorldPos = py.xform(node, q = True, scalePivot = True, ws = True)
    node.setAttr('translate', dt.Vector())
    currWorldPiv = py.xform(node, q = True, scalePivot = True, ws = True)
    node.setAttr('translate', -dt.Vector(currWorldPiv))
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
    node.setAttr('translate', dt.Vector(currWorldPos))
    
def setPivotToMidSelection():
    '''
        Set pivot to center of set selected vertexes. Auto convert to vertexes if edges or faces are chosen.
    '''
    vertexes = cmds.polyListComponentConversion(tv = True)
    cmds.select(vertexes)
    vertex = cmds.ls(sl=True,fl=True) 
    pivPos = [0,0,0]
    count = len(vertex)
    for i in vertex:
            iPos = cmds.pointPosition(i)
            pivPos[0] =  pivPos[0] + iPos[0]
            pivPos[1] =  pivPos[1] + iPos[1]
            pivPos[2] =  pivPos[2] + iPos[2]
    pivPos = [pivPos[0]/count,pivPos[1]/count,pivPos[2]/count]
        # get obj's component
    mainObj = cmds.ls(hilite=True)
    cmds.select(mainObj)
    cmds.xform(rp = pivPos, ws= True)
        
def setPivotToCenter(node):
    '''
        Set pivot to Center of selected mesh
    '''
    py.select(node)
    py.xform(cp=True)
        
def setPivotToOrigin(node):
    '''
        Set pivot to origin
    '''
    py.move(0,0,0,node+'.scalePivot',node+'.rotatePivot',a=True)
        
def setPivotToObject():
    selObj = cmds.ls(sl=True)
    target = cmds.xform(selObj[1],q=True,sp=True,ws=True)
    cmds.xform(selObj[0],piv=target, ws=True)
    
def setPivotOnLine(isTranslate = False, axis = 'y', node = None):
    '''
         set Pivot Along Edge
    '''
    cmds.select(cmds.polyListComponentConversion(tv = True))
    vertexes = py.ls(sl = True, fl = True)
    if len(vertexes) != 2:
        QtGui.QMessageBox.warning(None,'Error','Chi duoc chon 1 canh hoac 2 diem',QtGui.QMessageBox.Ok)
        return 
    
    #-- Apply translation to midle position.
    
    if isTranslate:
        setPivotToMidSelection()
    
    # get direction vector:

    pos0 = vertexes[0].getPosition(space = 'world') # -- get point's position in world coordinates
    pos1 = vertexes[1].getPosition(space = 'world') # -- get point's position in world coordinates
    vecDir = pos1 - pos0 # -- vector direction
    vecDir = vecDir.normal() # -- normalize vector dir
    print 'vector direction: '  + str(vecDir)
    
    # -- get mesh from select vertex
    
    nodeTransform = ''
    if node == None:
        nodeShape = PyNode(vertexes[0].split('.')[0])
        nodeTransform = nodeShape.listRelatives(p = True)[0]
    else:
        nodeTransform = node
     # -- get matrix transformation of mesh            
    
    m = nodeTransform.getMatrix()
    
    
def setPivotOnFace():
    pass
    
def setPivotRotation():
    pass

def pivots_to_pos(Xpos, Ypos, Zpos):
        cmds.xform(cp=True)
        #selObjs = cmds.ls(sl=True)
        bbox = cmds.xform(q=True,bb=True)
        pivot = cmds.xform(q=True,sp=True,ws=True)
        vector  = [0,0,0] 
        vectorX = [0,0,0]
        vectorY = [0,0,0]
        vectorZ = [0,0,0]
        ##
        if Xpos == 'Xmax':
            vectorX = [(bbox[3]-bbox[0])/2,0,0]
        if Xpos == 'Xmin':
            vectorX = [-(bbox[3]-bbox[0])/2,0,0]
        if Xpos == 'Xmid':
            vectorX = [0,0,0]
        ##   
        if Ypos == 'Ymax':
            vectorY = [0,(bbox[4]-bbox[1])/2,0]
        if Ypos == 'Ymin':
            vectorY = [0,-(bbox[4]-bbox[1])/2,0]
        if Ypos == 'Ymid':
            vectorY = [0,0,0]
        ##
        if Zpos == 'Zmax':
            vectorZ = [0,0,(bbox[5]-bbox[2])/2]
        if Zpos == 'Zmin':
            vectorZ = [0,0,-(bbox[5]-bbox[2])/2]
        if Zpos == 'Zmid':
            vectorZ = [0,0,0]
            
        vector[0] = pivot[0] + vectorX[0] + vectorY[0] + vectorZ[0]
        vector[1] = pivot[1] + vectorX[1] + vectorY[1] + vectorZ[1]
        vector[2] = pivot[2] + vectorX[2] + vectorY[2] + vectorZ[2]
        
        cmds.xform(piv = vector,ws=True, a=True)
        
def alignPivottoFace(mesh, face):
        if len(face) > 0:
            return False
        elif len(face) == 0:
            return False
        else:
            vertexes = cmds.polyListComponentConversion(face , ff = True, tv = True)
            pointA = vertexes[0]
            pointB = vertexes[1]
            pointC = vertexes[2]
            vectorAB = dt.Vector(pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2])
            vectorAC = dt.Vector(pointC[0] - pointA[0], pointC[1] - pointA[1], pointC[2] - pointA[2])
            normal = vectorAB.cross(vectorAC)
            x0 = normal.dot([1,0,0])*180/dt.pi
            y0 = normal.dot([0,1,0])*180/dt.pi
            z0 = normal.dot([0,0,1])*180/dt.pi
            
        cmds.xfom(mesh, roo = 'yzx', rp = [x0, y0,z0], ws = True)

def pivotOnAxis(axis):
        selObj = cmds.ls(sl=True)[0]
        oldPivot = cmds.xform(q=True,sp=True,ws=True)
        if axis == 'x':
            cmds.xform(piv=[0,oldPivot[1],oldPivot[2]],ws=True)
        if axis == 'y':
            cmds.xform(piv=[oldPivot[0],0,oldPivot[2]],ws=True)
        if axis == 'z':
            cmds.xform(piv=[oldPivot[0],oldPivot[1],0],ws=True)
    
def scaleMeshes(self):
        mesh = py.ls(sl = True)[0]
        currentScale = mesh.scaleX.get()
        
def freezeTransform(node):
    mel.eval('makeIdentity -apply true -t 1 -r 0 -s 1 -n 0 -pn 1;')
    

