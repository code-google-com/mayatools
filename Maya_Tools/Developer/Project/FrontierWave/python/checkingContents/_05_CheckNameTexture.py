
description = 'Check Texture name is wrong.'
name = 'CheckTextureNamewrong.'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


stdUVSet = ['map1']

def execute():
    NameHier =''
    NameTemp=''
    textures =''
    nameTexture =''
    print '--------------- CHECK TEXTURE NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    
     
    # check Ten texture:
    textures = py.ls(tex = True)
    
    for t in textures:
        nameTexture = t.getAttr('fileTextureName').split('/')[-1]
    
    if nameTexture =='':
        QtGui.QMessageBox.critical(None,'Ten Texture: ','Character nay chua co texture' ,QtGui.QMessageBox.Ok)
        pass
    else:        
        if nameTexture != 'tex_'+MayaFile +'_d01.png' and nameTexture != 'tex_' + MayaFile +'_d01_b.png':
            QtGui.QMessageBox.critical(None,'Ten Texture: ','Ten Texture bi sai:' +str(nameTexture),QtGui.QMessageBox.Ok)
            pass
    