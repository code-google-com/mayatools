description = 'Check Max Skin Influences'
name = 'CheckMaxSkinInfluences'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- Check Max Skin Influences-------------------------'
    attachFileSource = os.path.split(fileDirCommmon)[0] + '/checkMaxSkinInfluences.mel'
    print 'attachFileSource'
    print attachFileSource
    print 'fileDirCommmon'
    print fileDirCommmon
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    
  
    
    