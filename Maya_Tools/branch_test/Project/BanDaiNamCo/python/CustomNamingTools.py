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
        self.lod = list()
        self.part = list()
        #self.customtext = ''
        #self.mat = ''
        self.ldtCustom.returnPressed.connect(self.updateActivedList)
        self.cbbPart.currentIndexChanged.connect(self.updateActivedList)
        self.cbbLOD.currentIndexChanged.connect(self.updateActivedList)
        self.cbbKit.currentIndexChanged.connect(self.updateActivedList)
        self.btnHierrachy.clicked.connect(self.buildHierrachy)
        self.material = list()
        self.loadXML(inputFile)
             
    def loadXML(self, xmlFile):
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        kitNodes = root.getElementsByTagName('kit')
        self.kit.append([x.getAttribute('name') for x in kitNodes])
        self.kit.append([x.getAttribute('shortname') for x in kitNodes])
        lodNodes = root.getElementsByTagName('lod')
        self.lod = [x.getAttribute('name') for x in lodNodes]
        partNodes = root.getElementsByTagName('part')
        self.part = [x.getAttribute('name') for x in partNodes]
        materialNode = root.getElementsByTagName('material')
        self.material.append([x.getAttribute('name') for x in materialNode])
        self.material.append([x.getAttribute('shortname') for x in materialNode])
        self.cbbPart.addItems(self.part)
        self.cbbLOD.addItems(self.lod)
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
                mat = self.material[1][self.material[0].index(shaders[0])]
            else:
                mat = 'wrong_shader'
            part = str(self.cbbPart.currentText())
            kitname = self.kit[1][self.kit[0].index(str(self.cbbKit.currentText()))]
            lod = str(self.cbbLOD.currentText())
            customtext =  str(self.ldtCustom.text())
            if customtext != '':
                newname = 'mesh_' + mat + '_' + part  + '_' + customtext + '_' + kitname + '_' + lod
            else:
                newname = 'mesh_' + mat + '_' + part  + '_' + kitname + '_' + lod
            cmds.rename(node, newname)
            
    def buildHierrachy(self):
        errorMesh = []
        selObjs = cmds.ls(sl = True, l = True)
        cmds.select(cl = True)
        for node in selObjs:
            #try:
                kit = node.split('_')[-2]
                lod = node.split('_')[-1]
                parts = [x for x in self.part if re.search('(.*){p}(\.*)'.format(p = x), node.split('|')[-1])]
                if parts[0] in ['bumper_front', 'bumper_rear','side_skirts', 'wheel_arch']:
                    if kit == 'a':
                        parent = parts[0]+'|standard_type_'+kit+'|'+ lod.replace('lod','lod_')
                        if not cmds.objExists(parent):
                            nullGroup = cmds.group(em = True)
                            cmds.parent(nullGroup, parts[0]+'|standard_type_'+kit)
                            cmds.rename(nullGroup,lod.replace('lod','lod_'))
                    else:
                        parent = parts[0]+'|type_'+kit+'|'+ lod.replace('lod','lod_')
                        if not cmds.objExists(parent):
                            if not cmds.objExists(parts[0]+'|type_'+kit):
                                nullGroup = cmds.group(em = True)
                                cmds.parent(nullGroup, parts[0])
                                cmds.rename(nullGroup,'type_'+kit) 
                            nullGroup = cmds.group(em = True)
                            cmds.parent(nullGroup, parts[0]+'|type_'+kit)
                            cmds.rename(nullGroup,lod.replace('lod','lod_'))
                        
                elif parts[0] in ['rotor_rear_left','rotor_rear_right','rotor_front_left','rotor_front_right']:
                    parent = 'J_wheel_' + parts[0].replace('rotor_','') + '|rotor|type_a|' + lod.replace('lod','lod_')
                    if not cmds.objExists(parent):
                        nullGroup = cmds.group( em = True)
                        cmds.parent(nullGroup, 'J_wheel_' + parts[0].replace('rotor_','') + '|rotor|type_a|')
                        cmds.rename(nullGroup,lod.replace('lod','lod_'))
                        
                        
                elif parts[0] in ['caliper_rear_left','caliper_rear_right','caliper_front_left','caliper_front_right']:
                    parent = 'J_suspension_bottom_' + parts[0].replace('caliper_','') +'|caliper|type_'+kit+'|'+ lod.replace('lod','lod_')
                    if not cmds.objExists(parent):
                        nullGroup = cmds.group(em = True)
                        cmds.parent(nullGroup, 'J_suspension_bottom_' + parts[0].replace('caliper_','') +'|caliper|type_'+kit)
                        cmds.rename(nullGroup,lod.replace('lod','lod_'))
                else:
                    parent = parts[0]+'|type_'+kit+'|'+ lod.replace('lod','lod_')
                    if not cmds.objExists(parent):
                        if not cmds.objExists(parts[0]+'|type_'+kit):
                            nullGroup = cmds.group(em = True)
                            cmds.parent(nullGroup, parts[0])
                            cmds.rename(nullGroup,'type_'+kit) 
                        nullGroup = cmds.group(em = True)
                        cmds.parent(nullGroup, parts[0]+'|type_'+kit)
                        cmds.rename(nullGroup,lod.replace('lod','lod_'))
                cmds.parent(node, parent)
            #except:
                #errorMesh.append(node)
        #print errorMesh
                             
def main():
    xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/'+ input + '.xml'
    form = CustomNamingTool(xmlFile)
    return form 