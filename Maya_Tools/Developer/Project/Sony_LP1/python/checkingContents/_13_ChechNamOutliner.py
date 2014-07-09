description = 'Check Mesh Name'
name = 'checkMeshName'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

def execute():
    print '--------------- CHECK MESH NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    groupNameSplit = MayaFile.split('_',2)
    groupName= groupNameSplit[1] 
    print groupName