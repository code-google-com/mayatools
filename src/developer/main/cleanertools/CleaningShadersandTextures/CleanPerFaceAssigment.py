description = 'Fix double shader  on single face'
name = 'CleanPerFaceAssigment'
import maya.cmds as cmds
import maya.mel as mel


cmds.loadPlugin('cleanPerFaceAssignment')

def execute():
    mel.eval('cleanPerFaceAssignment;')