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

def mirrorUV(self,direction):#, pivotPoint = setPivotMirror()):
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