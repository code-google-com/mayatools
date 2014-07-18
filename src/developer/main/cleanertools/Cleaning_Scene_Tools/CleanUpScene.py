description = 'Optimize Scene (Maya default).'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


def execute():
    print '--------------- CLEAN UP SCENE-------------------------'
    
    print '--------------- Optimize scene ------------------------'
    mel.eval('OptimizeScene;')
        
    print '--------------- Delete MaxHandle node --------------------------'
    transformNode = cmds.ls(transforms = True)
    for node in transformNode:
        try:
            cmds.deleteAttr(node + '.MaxHandle')
        except:
            pass

    
    