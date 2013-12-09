description = 'Paint pure white for AO windows.'
name = 'setAOForWindows'
import maya.cmds as cmds
import maya.mel as mel


def execute():
    print '--------------- PAINT PURE WHITE FOR AO WINDOWs-------------------------'
    windowMesh = [cmds.listRelatives(mesh, c = True)[0] for mesh in cmds.ls('*WINDOW*', type = 'transform')]
    for mesh in windowMesh:
        if cmds.polyColorSet(mesh, q= True, acs = True):
            if 'colorSet1' not in cmds.polyColorSet(mesh, q= True, acs = True):
                cmds.polyColorSet(mesh, nc = 'colorSet1')
            else:
                cmds.polyColorSet(mesh, ccs = True, cs = 'colorSet1')
        else:
            cmds.polyColorSet(mesh, nc = 'colorSet1')
        cmds.polyColorPerVertex(mesh, a = 1)
    