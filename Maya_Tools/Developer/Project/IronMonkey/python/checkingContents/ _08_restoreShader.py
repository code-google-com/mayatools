description = 'Select meshes with wrong UVSet.'
name = 'fixUvSet'
import maya.cmds as cmds
import maya.mel as mel

stdUVSet = set(['map1', '2_scratch'])
def execute():
    print '--------------- SELECTE MESHES WRONG UVSET-------------------------'
    materials = cmds.ls(materials = True)
    for m in materials:
        cmds.connectAttr(m + '.outColor', m +'SG.surfaceShader', f = True)
    #meshes = cmds.ls(type = 'mesh')
    #for mesh in meshes:
    