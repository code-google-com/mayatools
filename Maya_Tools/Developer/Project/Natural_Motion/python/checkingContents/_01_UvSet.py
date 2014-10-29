
description = 'Create UV and Color.'
name = 'CreateUVandColor'
import maya.cmds as cmds
import maya.mel as mel

import Natural_MotionUV
reload(Natural_MotionUV)
def execute():
    print '--------------- CREATE UV WITH COLOR-------------------------'
    exp = Natural_MotionUV.createGUI()
    exp.exportMaya()
   
    