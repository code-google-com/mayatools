import inspect, os, re
import maya.mel as mel
import pymel.core as py
import pymel.core.datatypes as dt

description = 'Test and fix tech specs for wheel'
name = 'fixWheel'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def checkWheelFileCorrect():
    fileName = cmds.file(q = True, sn = True)
    if re.search(r'(.*)wheel(\.*)', fileName):
        return True
    else:
        return False

def checkDimensionConstraint():
    try:
        cmds.select('*wheel_tire*')
        bbox = cmds.xform(cmds.ls(ls = True)[0], q= True, bb = True)
        dimension = dt.Vector(bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2])
        if dimension.x != 0.25 or dimension.y != dimension.z != 0.72:
            return (False, dimension)
        else:
            return (True, dimension) 
    except:
        print 'No tire object was found.'

def checkPivotPosition():
    lowerLods = ['lod00','lod01','lod02','lod03','lod04','lod05','lod06']
    try:
        selMeshes = cmds.select('*lod00*')
        for i in selMeshes:
            pivotPos = cmsd.xform(i, q = True, sp = True )
    except:
        pass
            
def checkALL(axis):
    result = checkWheelFileCorrect()
    if result:
        pass
    if axis == 'Y':
        pass
    elif axis == 'X':
        pass
    elif axis == 'Z':
        pass
        
def assignPivot(radius, thickness):
    pass
    
def execute():
     pass