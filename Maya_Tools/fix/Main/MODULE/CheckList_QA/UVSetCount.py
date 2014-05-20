import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

__name__ = 'UVSet Count'

def run(mesh):
    try:
        message = ''
        result = True
        UVSetCount = cmds.polyUVSet(mesh, q = True, auv = True)
        if len(UVSetCount) > 1:
            result = False
            message = 'There are so many UVSet on ' + mesh + '.Please click \'HOW TO FIX\' to fix this error.'
        elif len(UVSetCount) == 1:
            message = mesh + ' has enough UVSet.'
        return (result, message,'')
    except:
        print mesh  + ' cannot exam uvSet'
        return (False,'UVSet not avaiable','')

def fix(mesh):
    pass
        