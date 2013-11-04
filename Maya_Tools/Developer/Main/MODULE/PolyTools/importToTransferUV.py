
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *
import os, sys

def loadFBXParas():
    mel.eval('FBXImportUnlockNormals -v true')
    mel.eval('FBXImportUpAxis y')
    
def transferFromRefPath(path):
    loadFBXParas()
    cmds.file(path, r = True, namespace = 'unwrapped')
    refNode = cmds.referenceQuery(path , referenceNode = True)
    nodes = cmds.referenceQuery(refNode , nodes = True)
    #mel.eval('FBXImport -f \"{f}\"'.format(f = path))
    #nodes = cmds.ls('*_unwrapped')
    for sourceNode in nodes:
        try:
            targetNode = sourceNode.replace('unwrapped:','')
            cmds.transferAttributes(sourceNode, targetNode, uvs = True)
            cmds.select(targetNode)
            mel.eval('DeleteHistory')
            cmds.delete(sourceNode)
        except:
            pass
    cmds.file(path, rr = True)