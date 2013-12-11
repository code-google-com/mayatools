description = 'Paint pure white for AO windows.'
name = 'setAOForWindows'
import maya.cmds as cmds
import maya.mel as mel


def execute():
    setupAOToWhite()
    
def setupAOToWhiteForWindow():
    print '--------------- PAINT PURE WHITE FOR AO WINDOWs-------------------------'
    windowMesh = [cmds.listRelatives(mesh, c = True)[0] for mesh in cmds.ls('*WINDOW*', type = 'transform')]
    for mesh in windowMesh:
        setupColorSetForMesh(mesh)
        cmds.polyColorPerVertex(mesh, a = 1)
        
def setupColorSetWholeScene():
  # set colorset for mesh
        print '-- Create colorSet1 for all mesh if not available.'
        meshNode = [cmds.listRelatives(mesh, c = True)[0] for mesh in cmds.ls(type = 'transform') if cmds.nodeType(cmds.listRelatives(mesh, c = True)[0]) == 'mesh']
        for mesh in meshNode:
            setupColorSetForMesh(mesh)
    
def setupColorSetForMesh(meshShape):
    currColorSet =  cmds.polyColorSet(meshShape, q= True, acs = True)
    if currColorSet:
        if 'colorSet1' not in currColorSet:
            cmds.polyColorSet(meshShape, cr = True, cs = 'colorSet1')
        else:
            cmds.polyColorSet(meshShape, ccs = True, cs = 'colorSet1')
    else:
        cmds.polyColorSet(meshShape, cr = True, cs = 'colorSet1')
    cmds.polyColorPerVertex(meshShape, a = 1)