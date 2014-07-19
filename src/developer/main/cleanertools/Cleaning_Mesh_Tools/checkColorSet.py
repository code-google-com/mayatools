description = 'Select meshes with wrong ColorSet.'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel

stdColorSet = set(['colorSet1','damageLookup_colorSet','damageVector_colorSet'])
def execute():
    print '--------------- SELECTE MESHES WRONG UVSET-------------------------'
    errorMesh = []
    meshes = cmds.ls(type = 'mesh')
    for mesh in meshes:
        try:
            colorSets = set(cmds.polyColorSet(mesh, q= True, acs = True))
        except:
            colorSets = set([])
        if not colorSets.issubset(stdColorSet):
            errorMesh.append(mesh)  
            print mesh + ' khong dap ung duoc so luong colorSet can co, uvset hien tai: ' + str(colorSets) + '.\n'
    cmds.select(cl = True)
    cmds.select(errorMesh)
    mel.eval('HideUnselectedObjects;')
    