
description = 'Check name is wrong.'
name = 'Checknameiswrong.'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py

stdUVSet = ['map1']

def execute():
    NameHier =''
    NameTemp=''
    print '--------------- CHECK NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    
    # Check Name name Hierarchy
    Hierarchy = cmds.ls(l=0, fl=1, type='transform')
    #listName = [s for s in Hierarchy if MayaFile in s]
    print Hierarchy
    # CHECK NAME OUTLINER:
   
    outlinerName=''
    for n in Hierarchy:
        if n not in ['front','persp','side','top']:
            if n == MayaFile:
                NameHier = n
            else:
                NameHier = n
        
    if NameHier != MayaFile:
        QtGui.QMessageBox.critical(None,'Ten Outliner ','Ten Outliner sai: '+str(NameHier) +', Ten dung la : '+str(MayaFile) ,QtGui.QMessageBox.Ok)
        pass
    
    
    # check Ten texture:
    textures = py.ls(tex = True)
    for t in textures:
        nameTexture = t.getAttr('fileTextureName').split('/')[-1]
    if nameTexture != MayaFile +'_D.tga':
        QtGui.QMessageBox.critical(None,'Ten Texture: ','Ban phai sua ten Texture.' +', Ten dung la : '+str(nameTexture) ,QtGui.QMessageBox.Ok)
        pass
        
    # check name Material:
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    shaders = [s for s in cmds.ls(materials = True) if s not in ['particleCloud1', 'lambert1']]
    # CHECK KIEU METERIAL
    type =''
    for sh in shaders:
        if cmds.nodeType(sh) =='phong':
            type= cmds.nodeType(sh)
        else:
            type= cmds.nodeType(sh)
    if type !='phong':
        QtGui.QMessageBox.critical(None,'Loai Materials ','Loai Material sai: '+str(type) +', Vui long sua lai loai Materials: phong',QtGui.QMessageBox.Ok)
        pass
      
    # CHECK TEN MATERIAL
    shaderName =''
    for s in shaders:
        if s == MayaFile +'_mat':
            shaderName = s
        else:
            shaderName = s
    
    if shaderName != MayaFile +'_mat':
        QtGui.QMessageBox.critical(None,'Ten Materials ','Ten Material sai: '+str(shaderName) +', Vui long sua lai ten Materials: '+str(MayaFile +'_mat'),QtGui.QMessageBox.Ok)
        pass
    