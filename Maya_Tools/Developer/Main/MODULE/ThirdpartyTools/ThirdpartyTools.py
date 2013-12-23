import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
# from pymel.core import *
import functools 
# import boltUvRatio
# import math
# 
# import Source.IconResource_rc
# reload(Source.IconResource_rc)
# 
# import CommonFunctions as cf
# reload(cf)
# 
# from MODULE.PolyTools import PolyTools as pt
# reload(pt)
# 
# from MODULE.ShaderTools import ShaderTools as st
# reload(st)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ThirdpartyTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

class ThirdpartyTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Third Party tools'
        self.load()
        
    def load(self):
        melScripts = [f for f in os.listdir(fileDirCommmon + '/mel/') if f.endswith('mel')]
        pythonScripts = [f for f in os.listdir(fileDirCommmon + '/python/') if f.endswith('py')]
        for script in melScripts + pythonScripts:
            if script in melScripts:
                attachFileSource = (fileDirCommmon + '/mel/' +  script).replace('\\' ,'/')
                button = QtGui.QPushButton(script.split('.')[0])
                button.clicked.connect(functools.partial(self.sourceMelScript, attachFileSource))
                self.verticalLayout.addWidget(button)
                
    def sourceMelScript(self, melScript):
        mel.eval('source \"{file}\";'.format(file = melScript))

def main(xmlFile):
    form = ThirdpartyTools(xmlFile)
    return form             