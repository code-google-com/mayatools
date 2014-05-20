
description = 'Delete Color Set.'
name = 'ColorSet'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel


def execute():
    
    print '--------------- DELETE COLOR SET-------------------------'
    objects = cmds.ls(type='mesh')
    print('objects',objects)
    for ob in objects:
        ploys = cmds.polyColorSet(ob,query=True,allColorSets=True)
        if ploys !=None:
            for p in ploys:
                cmds.polyColorSet(ob,delete=True,colorSet=p)
    