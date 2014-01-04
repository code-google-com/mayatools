description = 'Delete non deformed history.'
name = 'DeleteHistory'
import maya.cmds as cmds
import maya.mel as mel

def execute():
    print '--------------- DELETE HISTORY-------------------------'
    transformNodes = cmds.ls(type = 'transform')
    for node in transformNodes:
        cmds.select(node)
        mel.eval('BakeAllNonDefHistory;')
        print '-- Deleted non-deformable history on mesh: ' + node