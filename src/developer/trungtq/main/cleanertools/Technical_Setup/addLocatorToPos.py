description = 'Add a locator to selected position.'
tooltip = ''

import maya.cmds as cmds
import pymel.core as py
import pymel.core.datatypes as dt


def execute(self):
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
        #-----------------
        locator = py.spaceLocator()
        locator.translate.set(dt.Vector(pivPos))