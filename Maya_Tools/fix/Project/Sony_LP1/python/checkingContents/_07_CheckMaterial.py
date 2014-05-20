
description = 'Check Material type is wrong.'
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
    
     
    # check Ten texture:
    '''
    textures = py.ls(tex = True)
    for t in textures:
        nameTexture = t.getAttr('fileTextureName').split('/')[-1]
    if nameTexture != 'char_'+MayaFile +'_texture.psd':
        QtGui.QMessageBox.critical(None,'Ten Texture: ','Ten Texture bi sai:' +str(nameTexture)+'\n'+'Ten dung la : '+str('char_'+MayaFile +'_texture.psd') ,QtGui.QMessageBox.Ok)
        pass
    ''' 
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
    '''
    shaderName =''
    for s in shaders:
        if s == 'char_' + MayaFile +'_texture':
            shaderName = s
        else:
            shaderName = s
    if shaderName != 'char_' + MayaFile +'_texture':
        QtGui.QMessageBox.critical(None,'Ten Materials ','Ten Material sai: '+str(shaderName) +'\n'+'Vui long sua lai ten Materials: '+str('char_' + MayaFile +'_texture'),QtGui.QMessageBox.Ok)
        pass
    '''
    