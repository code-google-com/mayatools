import maya.cmds as cmds

__name__ = 'Poly Count'

def run(mesh):
    numFaces = cmds.polyEvaluate(mesh, face = True)
    message = 'There is ' + str(numFaces) + ' faces on ' + mesh + '.'
    return(numFaces, message, '')

def fix(mesh):
    pass