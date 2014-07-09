
description = 'Select meshes with wrong UVSet.'
name = 'fixUvSet'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel

stdUVSet = ['map1']

def execute():
    print '--------------- SELECTE MESHES WRONG UVSET-------------------------'
    errorMesh = []
    uvSets =[] 
    meshes = cmds.ls(type = 'mesh')
    for mesh in meshes:
        uvSets = set(cmds.polyUVSet(mesh, q= True,  auv = True))
        if not uvSets.issubset(stdUVSet) or 'map1' not in uvSets:
            errorMesh.append(mesh)  
            print mesh + ' khong dap ung duoc so luong uvset can co, uvset hien tai: ' + str(uvSets) + '.\n'
            QtGui.QMessageBox.critical(None,'Dat sai UVset','UVSet sai: ' + str(uvSets)+'\n' +'UVSet dung: '+str(stdUVSet),QtGui.QMessageBox.Ok)
    cmds.select(cl = True)
    cmds.select(errorMesh)
    mel.eval('HideUnselectedObjects;')
    #QtGui.QMessageBox.critical(None,'Dat sai UVset','UVSet la: '+str(uvSets),QtGui.QMessageBox.Ok)
    