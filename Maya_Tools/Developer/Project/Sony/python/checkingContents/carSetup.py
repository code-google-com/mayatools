description = 'Car setup.'
name = 'carSetup'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui

def execute():
    print '--------------- SETUP CAR s\' POSITION, SCALE, ROTATE -------------------------'
    # check WHEELs present in scene
    wheelNodes = py.ls('WHEEL*', type = 'transform')
    if not set(wheelNodes) & set(['WHEEL_FL', 'WHEEL_FR', 'WHEEL_BR', 'WHEEL_BL']):
        QtGui.QMessageBox.error(self, 'Missing wheel nodes', 'Please make sure that all wheels are imported! Thanks', QtGui.QMessageBox.Ok)
    else:
        pass
        # set pivot for wheel
    for w in wheelNodes:
        pass
        
        
    
        
   