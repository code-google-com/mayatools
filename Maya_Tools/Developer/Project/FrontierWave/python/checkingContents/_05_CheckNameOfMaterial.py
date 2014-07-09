
description = 'Check Material name is wrong.'
name = 'Checkmaterialnamewrong.'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


stdUVSet = ['map1']

def execute():
    NameHier =''
    NameTemp=''
    print '--------------- CHECK MATERIAL NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    
             
    # check name Material:
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    shaders = [s for s in cmds.ls(materials = True) if s not in ['particleCloud1', 'lambert1']]
    
   
    
    # CHECKED TEN MARTERIA
    shaderName =''
    for s in shaders:
        if s == 'tex_' + MayaFile +'_d01':
            shaderName = s
        else:
            shaderName = s
    if shaderName =='':
        QtGui.QMessageBox.critical(None,'Ten Materials: ','Character nay chua co Materials' ,QtGui.QMessageBox.Ok)
        pass
    else:
        if shaderName != 'tex_' + MayaFile +'_d01' and shaderName != 'tex_' + MayaFile +'_d01_b':
            
            QtGui.QMessageBox.critical(None,'Ten Materials ','Ten Material sai: '+str(shaderName) ,QtGui.QMessageBox.Ok)
            pass
    