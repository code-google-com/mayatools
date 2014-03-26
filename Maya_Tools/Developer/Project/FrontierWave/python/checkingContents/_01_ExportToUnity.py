
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as py
import maya.mel as mel
import os, sys, inspect, re, shutil
import functools
from xml.dom.minidom import *
import pymel.core as pm
import pymel.core.datatypes as dt
from math import *
import sip
import maya.cmds as cmds


import CommonFunctions as cf

import MODULE.PolyTools.ExporterandImporter
reload(MODULE.PolyTools.ExporterandImporter)

description = 'Export To Unity.'
name = 'ExportToUnity'

UnityPath ='C:/Unity/Project/Assets/Models'


def execute():
    print '--------------- EXPORT TO UNITY-------------------------'
    exp = ExporterandImporter.exporterShader()
    exp.exportMaya()
    
    '______________ COPY TO UNITY ____________'
    fileNameFBX = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.fbx'
    folderName = os.path.split(cmds.file(q= True, sn = True))[0]
    unityTexture = UnityPath + '/' + 'Textures'
    print folderName
    if os.path.isdir(UnityPath):
        if os.path.dirname(folderName):
            names = os.listdir(folderName)
            # Kiem tra thu muc texture trong Unity Prohect
            if not os.path.exists(unityTexture):
                os.makedirs(unityTexture)
            
            # LAY FILES TEXTURE
            for name in names:
                print name
                fileName = folderName +"/" + name
                print 'files mo rong: '
                if fileName != fileNameFBX:
                    extion = name.split(".")[-1]
                    if extion =='psd':
                        if os.path.isfile(fileName):
                            shutil.copy(fileName,unityTexture)
            shutil.copy(fileNameFBX,UnityPath)
                    
               
    
    else:
        QtGui.QMessageBox.critical(None,'Wrong Unity Project','Please create Unity project before import FBX files, thanks.',QtGui.QMessageBox.Ok)
        
    
    