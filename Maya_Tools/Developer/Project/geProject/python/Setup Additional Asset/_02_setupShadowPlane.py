import os, re, random, inspect
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]

description = 'Setup a shadow plane.'
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
        bbox = py.xform(q= True, bb= True)
        plane = py.Plane()
     # adding AO surface shader to make shadow map