description = 'Delete non deformed history.'
name = 'DeleteHistory'
import maya.cmds as cmds
import maya.mel as mel

def execute():
    print '--------------- DELETE HISTORY-------------------------'
    transformNodes = cmds.ls(type = 'transform')
    for node in transformNodes:
        cmds.select(node)
        mel.eval('DeleteHistory;')
        print '-- Deleted history on mesh: ' + node