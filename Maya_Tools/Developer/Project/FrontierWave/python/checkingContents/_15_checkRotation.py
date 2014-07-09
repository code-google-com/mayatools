
description = 'Check rotation UVSet.'
name = 'checkRotationUVset'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

stdUVSet = ['map1','map2']

def getShellFaces(poly, asString=False):
    shells = set()
    faces = set()
    total = cmds.polyEvaluate(poly, s=True)
    
    for f in xrange(cmds.polyEvaluate(poly, f=True)):
 
        if len(shells) >= total:
            break
        if f in faces:
            continue
 
        shell = cmds.polySelect(poly, extendToShell=f)
        faces.update(shell)
        
        if asString:
            val = "%s.f[%d:%d]" % (poly, min(shell), max(shell))
        else:
            val = min(shell)
        
        shells.add(val)
 
    return list(shells) 
def findUvShells(uvSet='map1'):
    data = [] # this is the array that will store, per object in the selection list, a dagPath and the number of shells in the given UV set.
  
    selList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selList)
    selListIter = om.MItSelectionList(selList, om.MFn.kMesh)
  
    uvShellArray = om.MIntArray() 
    # step through the objects on our selection list
    while not selListIter.isDone():
        pathToShape = om.MDagPath()
        selListIter.getDagPath(pathToShape)
        meshNode = pathToShape.fullPathName()
        
        # continue only if the given UV set exists on the shape
        uvSets = cmds.polyUVSet(meshNode, query=True, allUVSets =True)
        
        if (uvSet in uvSets):
     
          shapeFn = om.MFnMesh(pathToShape)
      
          shells = om.MScriptUtil()
          shells.createFromInt(0)
          shellsPtr = shells.asUintPtr()
      
          shapeFn.getUvShellsIds(uvShellArray, shellsPtr, uvSet)
      
          data.append( meshNode )
          data.append( str(shells.getUint(shellsPtr)) ) # I've chosen to return a string variable, but the class method returns an int
      
          # optional : print the shell index of each UV
          print('UV Shell Array: ',uvShellArray.length())
          for i in range(uvShellArray.length()):
              print('Tung UV Set: ',uvShellArray[i])
              
        uvShellArray.clear()      
        selListIter.next()
      
    return data

def execute():
    print '--------------- CHECK ROTATION UVSET-------------------------'
    #errorMesh = []
    uvSets =[] 
    #meshes = cmds.ls(type = 'mesh')
    temp = findUvShells('map1')
    print('UVSet:', temp)
    meshes = cmds.ls(sl=True)
    for mesh in meshes:
        shells = getShellFaces(mesh)
        print('***********************************************')
        for f in shells:
            cmds.polySelect(mesh, extendToShell=f)
        print('----------------------------------------------')
        shells = getShellFaces(mesh, True)
        for f in shells:
            cmds.select(f)
        #uvSets = set(cmds.polyUVSet(mesh, q= True,  auv = True))
    
        
    '''
        if not uvSets.issubset(stdUVSet) or 'map1' not in uvSets:
            errorMesh.append(mesh)  
            print mesh + ' khong dap ung duoc so luong uvset can co, uvset hien tai: ' + str(uvSets) + '.\n'
            QtGui.QMessageBox.critical(None,'Dat sai UVset','UVSet sai: ' + str(uvSets)+'\n' +'UVSet dung: '+str(stdUVSet),QtGui.QMessageBox.Ok)
    cmds.select(cl = True)
    cmds.select(errorMesh)
    mel.eval('HideUnselectedObjects;')
    #QtGui.QMessageBox.critical(None,'Dat sai UVset','UVSet la: '+str(uvSets),QtGui.QMessageBox.Ok)
    '''
    