description = 'Delete Layer in scene.'
name = 'deleteLayer'
import maya.cmds as cmds
import maya.mel as mel

def execute():
        layers = cmds.ls(type = 'displayLayer')
        cmds.delete(layers)
    