
description = 'Material type & Texture name wrong.'
name = 'Checknamematerialwrong.'
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
    groupNameSplit = MayaFile.split('_',2)
    groupName= groupNameSplit[1] 
    print groupName
     
    # check Ten texture:
    
    textures = py.ls(tex = True)
    for t in textures:
        nameTexture = t.getAttr('fileTextureName').split('/')[-1]
    if nameTexture != MayaFile +'_col.dds'and nameTexture != MayaFile +'_norm.dds' and nameTexture != MayaFile +'_spec.dds' and nameTexture != MayaFile +'_occ.dds':
        QtGui.QMessageBox.critical(None,'Ten Texture: ','Ten Texture bi sai:' +str(nameTexture) ,QtGui.QMessageBox.Ok)
        pass
     
    # check name Material:
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    shaders = [s for s in cmds.ls(materials = True) if s not in ['particleCloud1', 'lambert1']]
    
    # CHECK TYPE MATERIAL
    type =''
    for sh in shaders:
        if cmds.nodeType(sh) =='ATGMaterial':
            type= cmds.nodeType(sh)
        else:
            type= cmds.nodeType(sh)
    if type !='ATGMaterial':
        QtGui.QMessageBox.critical(None,'Loai Materials ','Loai Material sai: '+str(type)+'\n' +'Vui long sua lai loai Materials: ATGMaterial',QtGui.QMessageBox.Ok)
        pass
    
    # CHECKED TEN MARTERIA
    
    shaderName =''
    for s in shaders:
        if s == MayaFile +'_mat':
            shaderName = s
        else:
            shaderName = s
    if shaderName != MayaFile +'_mat':
        QtGui.QMessageBox.critical(None,'Ten Materials ','Ten Material sai: '+str(shaderName),QtGui.QMessageBox.Ok)
        pass
        