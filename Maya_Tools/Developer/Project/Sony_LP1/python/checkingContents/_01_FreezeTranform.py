description = 'Freeze Tranformation'
name = 'Freeze Tranformation'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    cmds.select(all=True)
    cmds.makeIdentity(apply=True, t=1,r=1,s=1,n=0)
    
    
    