import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect
from pymel.core import *
import functools 
from xml.dom.minidom import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/CustomNamingTool.ui'

form_class, base_class = uic.loadUiType(dirUI)    

class CustomNamingTool(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.kit = list()
        self.lod = ''
        self.part = ''
        self.customtext = ''
        self.mat = ''
        self.ldtCustom.returnPressed.connect(self.updateActivedList)
        self.cbbPart.currentIndexChanged.connect(self.updateActivedList)
        self.cbbLOD.currentIndexChanged.connect(self.updateActivedList)
        self.cbbKit.currentIndexChanged.connect(self.updateActivedList)
        self.material = list()
        
        self.loadXML(inputFile)
             
    def loadXML(self, xmlFile):
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        kitNodes = root.getElementsByTagName('kit')
        self.kit.append([x.getAttribute('name') for x in kitNodes])
        self.kit.append([x.getAttribute('shortname') for x in kitNodes])
        lodNodes = root.getElementsByTagName('lod')
        lod = [x.getAttribute('name') for x in lodNodes]
        partNodes = root.getElementsByTagName('part')
        part = [x.getAttribute('name') for x in partNodes]
        materialNode = root.getElementsByTagName('material')
        self.material.append([x.getAttribute('name') for x in materialNode])
        self.material.append([x.getAttribute('shortname') for x in materialNode])
        self.cbbPart.addItems(part)
        self.cbbLOD.addItems(lod)
        self.cbbKit.addItems(self.kit[0])
        
    def updateActivedList(self):
        selObjs = cmds.ls(sl = True, l = True)
        for obj in selObjs:
            self.updateNodeName(obj)
        
    def updateNodeName(self, node):
        shape = cmds.listRelatives(node, s = True)[0]
        sgs = cmds.listConnections(shape, type =  'shadingEngine')
        shaders = list(set([cmds.connectionInfo(x + '.surfaceShader', sfd = True).split('.')[0] for x in sgs]))
        if len(shaders) > 1:
            QtGui.QMessageBox.critical(self,'Error','Mesh khong the dat ten vi nhieu hon 1 shader',QtGui.QMessageBox.Ok)
        elif len(shaders) == 1:
            if shaders[0] in self.material[0]:
                self.mat = self.material[1][self.material[0].index(shaders[0])]
            else:
                self.mat = 'wrong_shader'
            self.part = str(self.cbbPart.currentText())
            self.kitname = self.kit[1][self.kit[0].index(str(self.cbbKit.currentText()))]
            self.lod = str(self.cbbLOD.currentText())
            self.customtext =  str(self.ldtCustom.text())
            if self.customtext != '':
                newname = 'mesh_' + self.mat + '_' + self.part  + '_' + self.kitname + '_' + self.customtext + '_' + self.lod
            else:
                newname = 'mesh_' + self.mat + '_' + self.part  + '_' + self.kitname + '_' + self.lod
            cmds.rename(node, newname)
        
        
def main():
    xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/IronMonkey_CustomNamingTool.xml'
    form = CustomNamingTool(xmlFile)
    return form 