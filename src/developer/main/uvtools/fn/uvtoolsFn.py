'''
Created on May 31, 2014

@author: quoctrung
'''

#-- import dependencies

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools 
import boltUvRatio
import math

def mirrorUV(direction):#, pivotPoint = setPivotMirror()):
    meshes = cmds.ls(hl = True)
    UVs = cmds.ls(sl = True)
    filterMesh = []
    for i in meshes:
        temp = []
        for j in UVs:
            if j.split('.')[0] == i:
                temp.append(j)
        filterMesh.append(temp)
        cmds.select(cl = True)
    for l in filterMesh:
        try:
            cmds.select(l)
            if direction == 'V':
                cmds.polyMoveUV(pivot = [0,0], scaleV = -1)
            if direction == 'H':
                cmds.polyMoveUV(pivot = [0,0], scaleU = -1)
        except:
            pass
        
def setUVScale(ratio):
        boltUvRatio.collect_shells_and_set_shells_UV_ratio(ratio)

def getUVScale():
        ratio = boltUvRatio.get_sel_faces_UV_ratio(1)
        return 1/ratio
    
def moveUVShell(dist, direction):
        if direction == 'down':
            cmds.polyEditUVShell( u = 0, v = -dist)
        if direction == 'up':
            cmds.polyEditUVShell( u = 0, v = dist)
        if direction == 'left':
            cmds.polyEditUVShell( u = -dist, v = 0)
        if direction == 'right':
            cmds.polyEditUVShell( u = dist, v = 0)
        if direction == 'upleft':
            pass
        if direction == 'upright':
            pass
        if direction == 'downleft':
            pass
        if direction == 'downright':
            pass
        
def unwrapPipe(listSeam, faceSet):
    cmds.polyForceUV(faceSet, utilize = True)
    listEdges = cmds.polyListComponentConversion(te = True) - listSeam
    cmds.select(listEdges)
    cmds.polyMapSewMove()
    

def openUVEditor():
    try:
        uvPanel = cmds.paneLayout('textureEditorPanel', panelSize=[1, 220, 1], cn = 'vertical2', swp = 1)
    except:
        uvPanel = cmds.paneLayout('textureEditorPanel', panelSize=[1, 220, 1], cn = 'vertical2')
    
    uvTextureViews = cmds.getPanel(scriptType='polyTexturePlacementPanel')
    
    