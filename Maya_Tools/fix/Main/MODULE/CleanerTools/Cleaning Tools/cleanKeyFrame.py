description = 'Clean keyframes not needed.'
name = 'cleanKeyFrame'

import maya.cmds as cmds
import maya.mel as mel
def execute():
    print '--------------- REMOVE KEYFRAME-------------------------'
    transformNodes = cmds.ls(type = 'transform')
    for node in transformNodes:
        cmds.cutKey(node, cl = True)
        print '-- Deleted keyframe on mesh: ' + node 