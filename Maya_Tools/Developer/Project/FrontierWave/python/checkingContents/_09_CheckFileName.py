
description = 'Check file name is wrong.'
name = 'Checkfilenameiswrong'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import sys

import AssetForm
reload(AssetForm)


def execute():
    #signal = QtCore.pyqtSignal('QString', name = 'textureChanged')
    NameHier =''
    NameTemp=''
    print '--------------- CHECK FILE NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    
    #app = QCoreApplication(sys.argv)
    #asset = AssetForm()
    #nameAsset = QOject.connect(asset,SIGNAL("asignal(PyQt_PyObject)"),asset.returnAssetValue)
    #nameAsset = QtGui.QComboBox(parent=None)#currentText()
    #print nameAsset
    formAsset = AssetForm() 
    form = formAsset.textureChanged.connect(cbbAssets.currentText())
    self.form = textureForm.main()
    tem = self.form.textureChanged.connect(returnAssetValue)
    print tem
    # check Ten texture:
    '''
    if shaderName != 'char_' + MayaFile +'_texture':
        QtGui.QMessageBox.critical(None,'Ten Materials ','Ten Material sai: '+str(shaderName) +', Vui long sua lai ten Materials: '+str('char_' + MayaFile +'_texture'),QtGui.QMessageBox.Ok)
        pass
        '''
    