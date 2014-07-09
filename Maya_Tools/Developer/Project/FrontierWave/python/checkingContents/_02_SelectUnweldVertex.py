description = 'Show Border edgs'
name = 'SelectUnweldVertext'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    objects = cmds.ls(type='mesh')
    cmds.select(objects)
    cmds.polyOptions(gl=True, softEdge=True, sizeBorder=5, displayBorder=True, displayMapBorder=False, displayCreaseEdge=False, displayVertex=False, displayNormal=False, facet=True, displayCenter=False, displayTriangle=False, displayWarp=False, displayItemNumbers=[False,False,False,False], sizeNormal=0.4, backCulling=True, displayUVs=False, displayUVTopology=False, colorShadedDisplay=False, colorMaterialChannel='diffuse', materialBlend='overwrite', backCullVertex=True)
    
    