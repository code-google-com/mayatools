description = 'Merge UV (d=0,001)'
name = 'MergeUVs'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- Merge UVs to d =0,01-------------------------'
    attachFileSource = os.path.split(fileDirCommmon)[0] + '/MergeUVset.mel'
    print 'attachFileSource'
    print attachFileSource
    print 'fileDirCommmon'
    print fileDirCommmon
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    
  
    
    