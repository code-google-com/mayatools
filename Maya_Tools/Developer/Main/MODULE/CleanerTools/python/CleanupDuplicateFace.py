description = 'Select duplicated faces.'
name = 'CleanupDuplicateFace'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- Remove duplicate faces -------------------------'
    attachFileSource = os.path.split(fileDirCommmon)[0] + '/mel/selectDuplicateFaces.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    
  
    
    