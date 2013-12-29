import inspect, os, re, ramdom
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Set up Assembly scene.'
name = '_01_setupAssembly'



def execute():
    print 'EXECUTING: SETUP ASSEMBLY SCENE----------------------------------'


def checkNaming():
    namefile = os.path.split(cmds.file(q= True, sn = True))[1].split('.')[0]
    rootNode = cmds.ls(namefile)[0]
    try:
        return rootNode
    except:
        print 'Cannot find root Node to export meshes.'
        return False
        
def createBBoxmesh():
    colors  = [random.randint(1,255)/255.0, random.randint(1,255)/255.0, random.randint(1,255)/255.0]
    if checkNaming():
        cmds.select(checkNaming())
        rootNode = cmds.ls(sl = True)[0]
        cmds.geomToBBox(n = rootNode + '_bbox', ko = True, s = True, sc = colors)
        cmds.file(os.path.split(cmds.file(q= True, sn = True))[0] + '/' + rootNode + '_bbox.mb', es = True, type = 'mayaBinary')
        cmds.delete(rootNode + '_bbox')
    else:
        print 'cannot create bbox'
        return
    
def createCacheMesh():
    if checkNaming():
        cmds.select(checkNaming())
        rootNode = cmds.ls(sl = True)[0]
        mel.eval('AbcExport -j "-frameRange 1 1 -root |' + rootNode +' -file ' +  os.path.split(cmds.file(q= True, sn = True))[0] + '/' + rootNode + '.abc";')
    else:
        print 'cannot create cache mesh'
        return
    
def createAssembleDef(name):
    cmds.createNode('assemblyDefinition')
    
def createAssembleReferences():
    pass
