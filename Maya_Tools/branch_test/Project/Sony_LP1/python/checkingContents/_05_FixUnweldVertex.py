description = 'Weld Vertex d=0,01 (all mesh)'
name = 'FixUnweldVertex'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    objects = cmds.ls(type='mesh')
    print('Danh sach Object: ',objects)
    for obj in objects:
        print obj
        poly = cmds.polyListComponentConversion(cmds.select(obj),tv=True)
        cmds.polyMergeVertex( d=0.01 )
    
    
    