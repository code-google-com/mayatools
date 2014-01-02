import os, re, random, subprocess, inspect
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]

description = 'Set up Assembly scene.'
name = 'setupAssembly'
#mayaPath = '\"'+os.environ.get("PROGRAMFILES").replace('\\', '/')+'/Autodesk/Maya'+os.environ.get('MAYAVERSION')+'/bin/mayabatch.exe"'
mayaPath = '\"'+os.environ.get("PROGRAMFILES").replace('\\', '/')+'/Autodesk/Maya2012/bin/mayabatch.exe"'
output = fileDirCommmon + 'log.txt'

def execute():
    print 'EXECUTING: SETUP ASSEMBLY SCENE ----------------------------------'
    try:
        createBBoxmesh()
    except:
        pass
    try:
        createCacheMesh()
    except:
        pass
    #namefile = cmds.file(q= True, sn = True)
    #commScript = '"python(\\\"import sys; sys.path.append(\'' + fileDirCommmon + '\'); import _01_setupAssembly as sa; sa.createAssembleDef(pathModel = \'' + namefile + '\')\\\")"'
#mayaPython = '"python(\\\"import sys;sys.path.append(\'' + fileDirCommmon + '\'); import transferFunction; transferFunction.getAssetBatchMode(execFile = \'' + mayafile + '\')\\\")"'
#
    #p = subprocess.Popen('"' + mayaPath + " -log " + output + " -c " + commScript + '"', shell = True)
    createAssembleDef(cmds.file(q= True, sn = True))

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
    
def createAssembleDef(pathModel): # using file model as input
    if not checkNaming():
        return False
    
    cmds.file(s = True)
    cmds.file(new = True, f = True)
    nameAssemblyDefinition = os.path.split(pathModel)[1].split('.')[0]
    cmds.assembly(name = nameAssemblyDefinition)
    
    cmds.assembly(nameAssemblyDefinition, edit = True, cr = 'Locator', repName = 'locator', input = nameAssemblyDefinition)
    cmds.assembly(nameAssemblyDefinition, edit = True, rl = 'locator', nrl = 'locator')
    
    cmds.assembly(nameAssemblyDefinition, edit = True, cr = 'Scene', repName = 'model', input = pathModel)
    cmds.assembly(nameAssemblyDefinition, edit = True, rl = 'model', nrl = 'model')
    
    cmds.assembly(nameAssemblyDefinition, edit = True, cr = 'Scene', repName = 'bbox', input = pathModel.replace('.mb', '_bbox.mb'))
    cmds.assembly(nameAssemblyDefinition, edit = True, rl = 'bbox', nrl = 'bbox')
    
    cmds.assembly(nameAssemblyDefinition, edit = True, cr = 'Cache', repName = 'cache', input = pathModel.replace('.mb', '.abc'))
    cmds.assembly(nameAssemblyDefinition, edit = True, rl = 'cache', nrl = 'cache')
    
    cmds.file(rn = pathModel.replace('.mb','') + '_AD.mb')
    cmds.file(s = True)
   
def createAssembleReferences():
    pass
