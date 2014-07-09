description = 'Remove NameSpace.'
name = 'RemoveNameSpace'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

import geNFS14_CleanUpFunctions
reload(geNFS14_CleanUpFunctions)

def execute():
    geNFS14_CleanUpFunctions.RemoveNamespaces()
    #QtGui.QMessageBox.critical(None,'Maximum Joint','Bones number used for thi character is: '+str(renamedNodes),QtGui.QMessageBox.Ok)
    
  
    
    