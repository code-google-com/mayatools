import os, re, random, inspect
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *
import pymel.core as py
import pymel.core.datatypes as dt

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]

description = 'Set up Shadow plane.'
name = '_02_setupShadowPlane'

def checkNaming():
    namefile = os.path.split(cmds.file(q= True, sn = True))[1].split('.')[0]
    rootNode = cmds.ls(namefile)[0]
    try:
        return rootNode
    except:
        print 'Cannot find root Node has the same name with file name to create shadow plane.'
        return False

def execute():
    if not checkNaming():
        return 
    else:
     # creating plane so its size is larger 10 percent meshes in scene
        if cmds.objExists('mesh_shadow'):
            cmds.delete('mesh_shadow')
        else:
            bbox = py.xform(checkNaming(), q= True, bb= True)
            width = bbox[3] - bbox[0]
            length = bbox[5] - bbox[2]  
            plane = py.polyPlane(n= 'mesh_shadow', w = width * 1.25, h = length * 1.1, sy = 1, sx = 1)[0]
            pos = dt.Vector((bbox[3] + bbox[0])/2, 0, (bbox[5] + bbox[2])/2)
            plane.translate.set(pos)
     # adding AO surface shader to make shadow map
        if (cmds.objExists('textureBakeSetAO')):
            cmds.delete('textureBakeSetAO')
        cmds.createNode('textureBakeSet', n = 'textureBakeSetAO')
        cmds.setAttr('textureBakeSetAO' + '.colorMode',3) # set color mode to bake Occlusion
        cmds.setAttr('textureBakeSetAO' + '.xResolution',512)
        cmds.setAttr('textureBakeSetAO' + '.yResolution',512)
        cmds.setAttr('textureBakeSetAO' + '.format',1)
        cmds.setAttr('textureBakeSetAO' + '.bits',2)
        cmds.setAttr('textureBakeSetAO' + '.mor',512)
        cmds.select('mesh_shadow')
        cmds.convertLightmapSetup('initialShadingGroup', 'mesh_shadow', camera = 'persp', sh = True, bo = 'textureBakeSetAO')