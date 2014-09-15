description = 'Clean up shaders and textures.'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


def execute():
    print '--------------- Clean up redundant shaders and textures-----------------'
    print '-- remove redundant textures--'
    textures = py.ls(textures = True)