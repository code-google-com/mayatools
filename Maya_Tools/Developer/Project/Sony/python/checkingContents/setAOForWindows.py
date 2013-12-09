description = 'Paint pure white for AO windows.'
name = 'setAOForWindows'
import maya.cmds as cmds
import maya.mel as mel


def execute():
    print '--------------- PAINT PURE WHITE FOR AO WINDOWs-------------------------'
    windowMesh = py.ls('*WINDOW*')
    