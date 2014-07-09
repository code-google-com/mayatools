description = 'Check Max Bones.'
name = 'CheckMaxBones'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect



def execute():
   jointList = cmds.ls(type ="joint")
   numberJoint = len(jointList)
   QtGui.QMessageBox.critical(None,'Maximum Joint','Bones number used for thi character is: '+str(numberJoint),QtGui.QMessageBox.Ok)
    
  
    
    