description = 'Clean up some bas issues.'
name = 'CleanUpScene'

import maya.cmds as cmds
import maya.mel as mel
def execute():
    print '--------------- CLEAN UP SCENE-------------------------'
    print '\n'
    print '--------------- Optimize scene ------------------------'
    print '\n'
    mel.eval('OptimizeScene;')
    print '--------------- Convert Instance mesh to object-------------------'
    
    print '\n'
    print '--------------- Clean up redundant shaders and textures-----------------'
    print '\n'