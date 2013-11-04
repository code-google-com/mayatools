description = 'Correct shape node name'
name = 'CorrectShapeNode'

import maya.cmds as cmds
def execute():
    print '--------------- RENAME SHAPENODE-------------------------'
    meshes = cmds.ls(type= 'mesh')
    for mesh in meshes:
        transformNode = cmds.listRelatives(mesh, parent = True, type = 'transform')[0]
        if mesh != transformNode + 'Shape':
            cmds.rename(mesh, transformNode + 'Shape')
            print '-- Renamed shape node on mesh:' + mesh