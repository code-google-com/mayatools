description = 'Delete Empty Meshes.'
name = 'DeleteEmptyMeshes'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

import geNFS14_CleanUpFunctions
reload(geNFS14_CleanUpFunctions)

def execute():
    objects = cmds.ls(type='mesh')
    #geNFS14_CleanUpFunctions.DeleteEmptyMeshes()
    geNFS14_CleanUpFunctions.DeleteIsolatedMeshes()
    #QtGui.QMessageBox.critical(None,'Maximum Joint','Bones number used for thi character is: '+str(renamedNodes),QtGui.QMessageBox.Ok)
    
  
    
    