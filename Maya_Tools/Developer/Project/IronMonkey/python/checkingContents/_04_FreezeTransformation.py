description = 'Freeze transformatiom of mesh.'
name = 'FreezeTransformation'

import maya.cmds as cmds
import maya.mel as mel
def execute():
    print '--------------- FREEZE TRANSFORM-------------------------'
    transformNodes = [node for node in cmds.ls(type = 'transform') if cmds.nodeType(node.listRelatives(c=True)) not in ['locator']]
    for node in transformNodes:
        cmds.select(node)
        mel.eval('FreezeTransformations;')
        
    # lock transformation of joint if found
    
    jointNodes = [j for j in cmds.ls(type = 'joint')]
    for joint in joinNodes:
        cmds.setAttr(joint + '.tx', l = True)
        cmds.setAttr(joint + '.ty', l = True)
        cmds.setAttr(joint + '.tz', l = True)
        cmds.setAttr(joint + '.rx', l = True)
        cmds.setAttr(joint + '.ry', l = True)
        cmds.setAttr(joint + '.rz', l = True)
        cmds.setAttr(joint + '.sx', l = True)
        cmds.setAttr(joint + '.sy', l = True)
        cmds.setAttr(joint + '.sz', l = True)