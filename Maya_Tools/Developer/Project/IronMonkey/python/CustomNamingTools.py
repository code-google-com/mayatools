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
locators = ['pivot_bumper_front_left','pivot_bumper_front_right','pivot_bumper_rear_left','pivot_bumper_rear_right','locator_headlights_00','locator_brakelights_00','locator_wheel_smoke_00 ','locator_nitro_00','wheel_arch_loc']
lods = ['lod_00','lod_01','lod_02','lod_03','lod_04','lod_05','lod_06']
parts = ['type_a','type_b','type_c','type_d','type_y','type_z', 'pulled_type_a','pulled_type_b', 'pulled_type_c', 'pulled_type_d',
         'large_type_a', 'large_type_b', 'large_type_c', 'large_type_d',
         'small_type_a','small_type_b', 'small_type_c', 'small_type_d']#,'pull_wheelarch','large_overfender','small_overfender']
form_class, base_class = uic.loadUiType(dirUI)    

class CustomNamingTool(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.kit = list()
        self.lod = list()
        self.part = list()
        self.ldtCustom.returnPressed.connect(self.updateActivedList)
        self.cbbPart.currentIndexChanged.connect(self.updateActivedList)
        self.cbbLOD.currentIndexChanged.connect(self.updateActivedList)
        self.cbbKit.currentIndexChanged.connect(self.updateActivedList)
        self.btnHierrachy.clicked.connect(self.buildHierrachy)
        self.btnPlace.clicked.connect(self.placeLocators)
        self.btnSetupLOD.clicked.connect(self.setupLOD)
        self.material = list()
        self.loadXML(inputFile)
        self.cbbLocatorList.addItems(locators)
         
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
        
    def setupLOD(self):
        #----- remove current layers. An setup correct structures
        layers = cmds.ls(type = 'displayLayer')
        cmds.delete(layers)
        
        #----- create structure layers. --------------------------------------------------
        cmds.createDisplayLayer(n = 'decal_placement_layer')
        cmds.createDisplayLayer(n = 'locator_layer')
        cmds.createDisplayLayer(n = 'collision_layer')
        cmds.createDisplayLayer(n = 'wheel_placeholder_layer')
        cmds.createDisplayLayer(n = 'base_car_layer')
        cmds.createDisplayLayer(n = 'pulled_wheel_arch_layer')
        cmds.createDisplayLayer(n = 'small_overfenders_layer')
        cmds.createDisplayLayer(n = 'large_overfenders_layer')
        
        for part in parts:
            try:
                py.select('*' + part + '*')
                cmds.createDisplayLayer(e = False, n = part + '_layer')
            except:
                pass
        for lod in lods:
            try: 
                py.select('*' + lod + '*')
                cmds.createDisplayLayer(e = False, n = lod + '_layer')
            except:
                pass
        # select all locator and put them in 
        try:
            cmds.editDisplayLayerMembers('locator_layer', cmds.ls(type = 'locator'), noRecurse = True)
        except:
            pass
        # select wheel place holder and put them in
        try:
            cmds.editDisplayLayerMembers('wheel_placeholder_layer', cmds.ls('*placeholder*'), noRecurse = True)
        except:
            pass
        # select decal placeholder and put them in
        # cmds.editDisplayLayerMembers('decal_placement_layer', [x for x in cmds.ls('*decal_*') if x not in cmds.ls(materials = True)], noRecurse = True)
        # select decal placeholder and put them in
        try:
            cmds.editDisplayLayerMembers('collision_layer', cmds.ls('*collider*'), noRecurse = True)
        except:
            pass
        # select lod00 and add them to layer
        cmds.editDisplayLayerMembers('lod_00_layer', cmds.ls('lod_00'), noRecurse = True)
        # select lod01 and add them to layer
        cmds.editDisplayLayerMembers('lod_01_layer', cmds.ls('lod_01'), noRecurse = True)
        # select lod02 and add them to layer
        cmds.editDisplayLayerMembers('lod_02_layer', cmds.ls('lod_02'), noRecurse = True)
        # select lod03 and add them to layer
        cmds.editDisplayLayerMembers('lod_03_layer', cmds.ls('lod_03'), noRecurse = True)
        # select lod04 and add them to layer
        cmds.editDisplayLayerMembers('lod_04_layer', cmds.ls('lod_04'), noRecurse = True)
        # select lod05 and add them to layer
        cmds.editDisplayLayerMembers('lod_05_layer', cmds.ls('lod_05'), noRecurse = True)
        # select lod06 and add them to layer
        cmds.editDisplayLayerMembers('lod_06_layer', cmds.ls('lod_06'), noRecurse = True)
        # select base car and add them to layer
        cmds.editDisplayLayerMembers('base_car_layer', cmds.ls('rotor|type_a','caliper|type_a','chassis|type_a','body|type_a','interior|type_a','windows|type_a','headlights|type_a','taillights|type_a'), noRecurse = True)
        # select pull wheel arch
        try:
            cmds.editDisplayLayerMembers('pulled_wheel_arch_layer', cmds.ls('pulled'), noRecurse = True)
        except:
            pass
        # select small over fender
        try:
            cmds.editDisplayLayerMembers('small_overfenders_layer', cmds.ls('small'), noRecurse = True)
        except:
            pass
        # select large over fender
        try:
            cmds.editDisplayLayerMembers('large_overfenders_layer', cmds.ls('large'), noRecurse = True)
        except:
            pass
        
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
                #ext = node.split('_')[-3]
                parts = [x for x in self.part if re.search('(.*){p}(\.*)'.format(p = x), node.split('|')[-1])]
                if parts[0] in ['bumper_front', 'bumper_rear','side_skirts', 'wheel_arch']:
                    if kit not in  ['z','y']:
                        parent = parts[0]+'|standard_type_'+kit+'|'+ lod.replace('lod','lod_')
                        if not cmds.objExists(parent):
                            if not cmds.objExists(parts[0]+'|standard_type_'+kit):
                                nullGroup = cmds.group(em = True)
                                cmds.parent(nullGroup, parts[0])
                                cmds.rename(nullGroup,'standard_type_'+kit) 
                            nullGroup = cmds.group(em = True)
                            cmds.parent(nullGroup, parts[0]+'|standard_type_' + kit)
                            cmds.rename(nullGroup,lod.replace('lod','lod_'))
                        if re.search('(.*){p}(\.*)'.format(p = 'pulled'),node):
                            parent = parts[0]+'|pulled_type_'+kit+'|'+ lod.replace('lod','lod_')
                            if not cmds.objExists(parent):
                                if not cmds.objExists(parts[0]+'|pulled_type_'+kit):
                                    nullGroup = cmds.group(em = True)
                                    cmds.parent(nullGroup, parts[0])
                                    cmds.rename(nullGroup,'pulled_type_'+kit)
                                nullGroup = cmds.group(em = True)
                                cmds.parent(nullGroup, parts[0]+'|pulled_type_' + kit)
                                cmds.rename(nullGroup,lod.replace('lod','lod_')) 
                        if re.search('(.*){p}(\.*)'.format(p = 'large'), node):
                            parent = parts[0]+'|large_type_'+kit+'|'+ lod.replace('lod','lod_')
                            if not cmds.objExists(parent):
                                if not cmds.objExists(parts[0]+'|large_type_'+kit):
                                    nullGroup = cmds.group(em = True)
                                    cmds.parent(nullGroup, parts[0])
                                    cmds.rename(nullGroup,'large_type_'+kit)
                                nullGroup = cmds.group(em = True)
                                cmds.parent(nullGroup, parts[0]+'|large_type_' + kit)
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
        
    def placeLocators(self):
        vertexes = cmds.polyListComponentConversion(tv = True)
        cmds.select(vertexes)
        vertex = cmds.ls(sl=True,fl=True) 
        pivPos = [0,0,0]
        count = len(vertex)
        for i in vertex:
            iPos = cmds.pointPosition(i)
            pivPos[0] =  pivPos[0] + iPos[0]
            pivPos[1] =  pivPos[1] + iPos[1]
            pivPos[2] =  pivPos[2] + iPos[2]
        pivPos = [pivPos[0]/count,pivPos[1]/count,pivPos[2]/count]
        #-----------------
        locator = py.spaceLocator(n = str(self.cbbLocatorList.currentText()))
        locator.translate.set(dt.Vector(pivPos))
                             
def main():
    xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/IronMonkey_CustomNamingTool.xml'
    form = CustomNamingTool(xmlFile)
    return form 