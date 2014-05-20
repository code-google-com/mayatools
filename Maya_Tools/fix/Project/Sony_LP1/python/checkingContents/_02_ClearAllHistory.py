description = 'Delete All History.'
name = 'DeleteAllHistory'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect



def execute():
    import maya.mel as mel
    #mel.eval('BakeAllNonDefHistory;')
    mel.eval('DeleteAllHistory;')
    #QtGui.QMessageBox.critical(None,'Maximum Joint','Bones number used for thi character is: '+str(renamedNodes),QtGui.QMessageBox.Ok)
    
  
    
    