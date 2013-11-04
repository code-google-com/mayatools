
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
from pymel.core import *
import functools 


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/CrydevTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

class CrydevTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'CryEngine Toolbox'
        self.btnChecks.clicked.connect(self.cryCheck)
        self.btnMaterial.clicked.connect(self.cryMaterial)
        self.btnCryTools.clicked.connect(self.cryTools)
        self.btnCryLoad.clicked.connect(self.cryLoad)
        self.btnCryUnload.clicked.connect(self.cryUnLoad)
        self.btnCryExport.clicked.connect(self.cryExport)
        self.btnCryPivot.clicked.connect(self.cryPivot)
        self.btnCryUDP.clicked.connect(self.cryUDP)
        self.btnCryFBX.clicked.connect(self.cryFBX)
        self.btnCryValidation.clicked.connect(self.cryValidate)
    def cryCheck(self):
        attachFileSource = fileDirCommmon + '/mel/degraded_faces_check.mel'
        mel.eval('source \"{f}\";\nrcryCheckFaces;'.format(f = attachFileSource))
        
    def cryMaterial(self):
        attachFileSource = fileDirCommmon + '/mel/cryMaterial.mel'
        mel.eval('source \"{f}\";\r\ncryMaterialWin;'.format(f = attachFileSource))
        
    def cryTools(self):
        attachFileSource = fileDirCommmon + '/mel/cryTools.mel'
        mel.eval('source \"{f}\";\r\ncryToolsWin;'.format(f = attachFileSource))
        
    def cryLoad(self):
        attachFileSource = fileDirCommmon + '/mel/cryExport.mel'
        mel.eval('source \"{f}\";\r\ncryLoadPlugin;'.format(f = attachFileSource))
        
    def cryUnLoad(self):
        attachFileSource = fileDirCommmon + '/mel/cryExport.mel'
        mel.eval('source \"{f}\";\r\ncryUnloadPlugin;'.format(f = attachFileSource))
        
    def cryExport(self):
        attachFileSource = fileDirCommmon + '/mel/cryExport.mel'
        mel.eval('source \"{f}\";\r\ncryExportWin;'.format(f = attachFileSource))
        
    def cryPivot(self):
        attachFileSource = fileDirCommmon + '/mel/cryPivot.mel'
        mel.eval('source \"{f}\";\r\ncryPivot;'.format(f = attachFileSource))   
    
    def cryUDP(self):
        attachFileSource = fileDirCommmon + '/mel/cryUDP.mel'
        mel.eval('source \"{f}\";\r\ncryUDPWindow;'.format(f = attachFileSource))
        
    def cryFBX(self):
        attachFileSource = fileDirCommmon + '/mel/cryUDP.mel'
        mel.eval('source \"{f}\";\r\ncryFBX;'.format(f = attachFileSource))
        
    def cryValidate(self):
        attachFileSource = fileDirCommmon + '/mel/cryExport.mel'
        mel.eval('source \"{f}\";\r\ncryExportValidateAndExport;'.format(f = attachFileSource))             


def main(xmlnput):
    form = CrydevTools(xmlnput)
    return form 

