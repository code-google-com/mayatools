
description = 'Check Material type is wrong.'
name = 'CheckMaterialTypewrong.'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


stdUVSet = ['map1']

def execute():
    NameHier =''
    NameTemp=''
    print '--------------- CHECK MATERIAL TYPE WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    
     
    
        
    # check name Material:
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    shaders = [s for s in cmds.ls(materials = True) if s not in ['particleCloud1', 'lambert1']]
    
    # CHECK TYPE MATERIAL
    type =''
    for sh in shaders:
        if cmds.nodeType(sh) =='lambert':
            type= cmds.nodeType(sh)
        else:
            type= cmds.nodeType(sh)
    if type !='lambert':
        QtGui.QMessageBox.critical(None,'Loai Materials ','Loai Material sai: '+str(type)+'\n' +'Vui long sua lai loai Materials: lambert',QtGui.QMessageBox.Ok)
        pass
    
    