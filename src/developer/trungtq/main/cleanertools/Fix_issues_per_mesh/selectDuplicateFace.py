description = 'Select duplicated faces.'
tooltip = ''

import os, inspect

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- Remove duplicate faces -------------------------'
    attachFileSource = os.path.split(fileDirCommmon)[0] + '/Fix issues per mesh/selectDuplicateFaces.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    
  
    
    