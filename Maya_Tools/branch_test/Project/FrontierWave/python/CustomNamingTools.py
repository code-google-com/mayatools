import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect, re
import pymel.core as py
import pymel.core.datatypes as dt
import functools 
from xml.dom.minidom import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/CustomNamingTool.ui'

form_class, base_class = uic.loadUiType(dirUI)    

class CustomNamingTool(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        
        self.btnUpdateFile.clicked.connect(self.readFileText)
        self.btnPreview.clicked.connect(self.updateText)
        self.btnNext.clicked.connect(self.loadText)
        
    def readFileText(self):
        print"Text"
    
    def updateText(self):
        print"Text"
    def loadText(self):
        print'text'
    def previewAnimation(self):
        print"text"
    def nextAnimation(self):
        print"text"
         
   
        
def main():
    xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/FrontierWave_CustomNamingTool.xml'
    form = CustomNamingTool(xmlFile)
    return form 