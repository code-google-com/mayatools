import time
from maya import cmds as cmds
import maya.mel as mel

__name__ = 'Freeze Transformations'

def isIdentity(transform):
    return cmds.xform(transform, query=True, matrix=True) == [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

def run(mesh):
    result = isIdentity(mesh)
    message = ''
    if result:
        message = mesh + ' has transformation value: [X-Y-Z] = 0, rotation value: [X-Y-Z] = 0 and scale: [X-Y-Z] = 1.'
    else:
        message = mesh + ' should have transformation value: [X-Y-Z] = 0, rotation value: [X-Y-Z] = 0 and scale: [X-Y-Z] = 1. Please refer to \'How to fix\' section. Thanks!'
    return (result,message, '')  

def fix(mesh):
    mel.eval('FreezeTransformations')