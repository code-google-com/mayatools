description = 'Freeze transformatiom of node'
name = 'FreezeTransformation'

import maya.cmds as cmds
import maya.mel as mel
def execute():
    print '--------------- FREEZE TRANSFORM-------------------------'
    transformNodes = cmds.ls(type = 'transform')
    for node in transformNodes:
        cmds.select(node)
        mel.eval('FreezeTransformations;')