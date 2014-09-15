description = 'Clean up instance meshes.'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


def execute():
    print '--------------- Convert Instance mesh to object-------------------'
    shapeNodes = cmds.ls(type = 'mesh')
    for shape in shapeNodes:
        parents = cmds.listRelatives(shape, allParents = True)
        if len(parents) > 1:
            print shape + ' is instances of mesh'
            py.select(parents)
            mel.eval('ConvertInstanceToObject;')

    
    