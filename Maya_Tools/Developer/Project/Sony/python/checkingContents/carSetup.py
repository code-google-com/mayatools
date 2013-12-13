description = 'Car setup.'
name = 'carSetup'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import pymel.core.datatypes as dt
from PyQt4 import QtGui

import setAOForWindows as ao
reload(ao)

def execute():
    print '--------------- SETUP CAR s\' POSITION, SCALE, ROTATE -------------------------'
    # check WHEELs present in scene
    wheelNodes = py.ls('WHEEL*', type = 'transform')
    match = [wheel for wheel in ['WHEEL_FL', 'WHEEL_FR', 'WHEEL_BR', 'WHEEL_BL'] if wheel not in wheelNodes]
    if len(match):
        QtGui.QMessageBox.critical(None, 'Missing wheel nodes', 'Please make sure that all wheels are imported! Thanks', QtGui.QMessageBox.Ok)
    else:
        # zero pivot offset
        
        wheel = py.ls('WHEEL_FL')[0]
        a = wheel.translateX.get()
        wheel = py.ls('WHEEL_BL')[0]
        b = wheel.translateX.get()
        bb= py.xform(wheel, q= True, bb = True)
        c= ( a + b)/2
        # group all selected mesh in scene
        mel.eval('SelectAll;')
        py.group(n = 'setup')
        g = py.ls('setup')[0]
        # move to center
        g.translateX.set(-c)
        g.translateZ.set(-bb[2])
        #g.xform(cp = True)
        
        g.setScalePivot(dt.Vector(0,0,0))
        g.setRotatePivot(dt.Vector(0,0,0))
        
        g.scale.set(dt.Vector(0.01, 0.01, 0.01))
        
        g.rotateX.set(-90)
        g.rotateY.set(90)
        
        # clean up
        try:
            cmds.makeIdentity(str(g), a = True, t = 1, r = 1, s = 1, n = 0)
        except:
            pass
        
    # set AO
    ao.setupColorSetWholeScene()
        
      
        
        
    
    
    
        
        
        
    
        
   