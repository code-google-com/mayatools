import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import re

from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import functools 

LODsChain = ['_LOD0_','_LOD1_','_LOD2_','_LOD3_','_LOD4_','_LOD5_','_LOD6_']
# SONY Lods:
Sony_mapping_LODs = ['_LOD0_','_LOD1_','_LOD2_','_LOD3_','_LOD4_','_LOD5_','_LOD6_']
Sony_nohide = []
# IronMonkey Lods:
IronMonkey_mapping_LODs = ['lod_00_layer', 'lod_01_layer', 'lod_02_layer', 'lod_03_layer', 'lod_04_layer', 'lod_05_layer', 'lod_06_layer']
IronMonkey_nohide = ['base_car_layer','spoilers','exhausts']


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/SonyLODTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def mappingLODs(projectName, lod):
    try:
        return globals()[projectName + '_mapping_LODs'][LODsChain.index(lod)]
    except:
        return False # cannot find matched imte with lod
    


class CustomLODTools(form_class,base_class):
    def __init__(self):
        super(base_class,self).__init__()
        self.setupUi(self)
        self._projectName = 'Sony'
        self._nohide = list()
        self._currentPart = ''
        self.btnSetupLOD.clicked.connect(self.check)
        self.btnSwitchLOD.clicked.connect(self.SwapLOD)
        self.btnCleanUp.clicked.connect(self.CleanUp)
        self.btnSpreadHonrizonal.clicked.connect(self.setPosition)
        self.btnSpreadVertical.clicked.connect(self.setPosition)
        self.btnPreviousLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'previous'))
        self.btnNextLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'next'))
        self.spnValue.valueChanged.connect(self.setPosition)
        self.btnLOD0.clicked.connect(functools.partial(self.selectLOD,'0'))
        self.btnLOD1.clicked.connect(functools.partial(self.selectLOD,'1'))
        self.btnLOD2.clicked.connect(functools.partial(self.selectLOD,'2'))
        self.btnLOD3.clicked.connect(functools.partial(self.selectLOD,'3'))
        self.btnLOD4.clicked.connect(functools.partial(self.selectLOD,'4'))
        self.btnLOD5.clicked.connect(functools.partial(self.selectLOD,'5'))
        self.btnLOD6.clicked.connect(functools.partial(self.selectLOD,'6'))
        self.btnSHADOW.clicked.connect(functools.partial(self.selectLOD,'shadow'))
        #self.btnPulled.clicked.connect(functools.partial(self.selectLOD,'pulled'))
        #self.btnSmall.clicked.connect(functools.partial(self.selectLOD,'small'))
        #self.btnLarge.clicked.connect(functools.partial(self.selectLOD,'large'))
        #self.chkSpoiler.clicked.connect(self.loadSpoilerTypeA)
        #self.btnLOD6.clicked.connect(functools.partial(self.selectLOD,'6'))
        #self.btnLOD7.clicked.connect(functools.partial(self.selectLOD,'7'))
        #self.btnLOD8.clicked.connect(functools.partial(self.selectLOD,'8'))
        #self.btnStandard.clicked.connect(functools.partial(self.selectLOD,'6'))
  


    def UnParent(self):
        transformEvo = [x for x in cmds.ls(dag = True) if cmds.nodeType(cmds.pickWalk(x,d = 'down')) == 'evoAttributeNode']
        try:
            cmds.delete(transformEvo)
        except:
            pass
        transformMayaNode = cmds.ls(transforms = True)
        for node in transformMayaNode: 
            try:
                cmds.parent(node, world = True)
            except:
                pass
        
    def CleanUp(self):
        try:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)  
                #cmds.delete(LODsChain[index].lstrip('_').rstrip('_'))
        except:
            pass
        self.UnParent()
        
    def check(self):
        if self._projectName == 'IronMonkey':
            setupLOD()
            childrenOfSpoilers = cmds.listRelatives('spoiler', c = True)
            childrenOfSpoilers.append('---Nothing---')
            childrenOfExhaust = cmds.listRelatives('exhaust', c = True)
            childrenOfExhaust.append('---Nothing---')
            self.cbbSpoilers.addItems(childrenOfSpoilers)
            self.cbbExhausted.addItems(childrenOfExhaust)
        else:
            if not cmds.objExists('LayerSetup'):
                self.createLOD()

        
    def createLOD(self):
        # --
#         cmds.createNode('test')
#         cmds.rename('unknown1', 'LayerSetup')
#         self.btnCleanUp.setEnabled(True)
#         self.btnSpreadHonrizonal.setEnabled(True)
#         self.btnSpreadVertical.setEnabled(True)
#         self.btnNextLOD.setEnabled(True)
#         self.btnPreviousLOD.setEnabled(True)
        lodList = ['LOD1','LOD2','LOD3','LOD4','LOD5','LOD6','SHADOW']
        #-- create LOD1 Layer
        for i in lodList:
            try:
                cmds.select('*' + i + '*')
                #cmds.group(n = 'LOD1')
                cmds.createDisplayLayer(n = '_'+ i +'_')
                cmds.editDisplayLayerMembers('_' + i + '_', cmds.ls(sl = True), noRecurse = True)
            except:
                pass
        
        try:
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [cmds.listRelatives(x, c = True)[0] for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            #cmds.group(n = 'LOD0')
            cmds.createDisplayLayer(n = '_LOD0_', nr = False)
            cmds.editDisplayLayerMembers('_LOD0_', cmds.ls(type = 'LOD0'), noRecurse = True)
        except:
            pass
        
        cmds.showHidden(all = True)
        
    def SwapLOD(self):
        if self._projectName == 'IronMonkey':
            self.SwapLODIronMonkey()
        if self._projectName == 'Sony':
            self.SwapLODSony()
        
    def SwapLODIronMonkey(self):
        if self._projectName == 'IronMonkey':
            mel.eval('showHidden -all;')        
        self._nohide = ['base_car_layer', 'spoilers','exhausts']
        
        if self.rdbSourceLOD0.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbSourceLOD1.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbSourceLOD2.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbSourceLOD3.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbSourceLOD4.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbSourceLOD5.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbSourceLOD6.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbSourceSHADOW.isChecked():
            LODa = mappingLODs(self._projectName,'_SHADOW_')
            
        if self.rdbTargetLOD0.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbTargetLOD1.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbTargetLOD2.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbTargetLOD3.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbTargetLOD4.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbTargetLOD5.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbTargetLOD6.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbTargetSHADOW.isChecked():
            LODb = mappingLODs(self._projectName,'_SHADOW_')
        # ------------------------------------------------
        type_a = list()
        if not self.btnLOD0.isChecked():
            cmds.setAttr('type_a_layer.visibility', 1)
            if self.chkBumper_front.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                type_a.append('bumper_front|standard_type_a')
            if self.chkBumper_rear.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                type_a.append('bumper_rear|standard_type_a')
            if self.chkSide_skirt.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                type_a.append('side_skirts|standard_type_a')
            if self.chkHood.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                type_a.append('hood|type_a')
                
            groups = [group.split('.')[0] for group in cmds.connectionInfo('type_a_layer.drawInfo', dfs = True)]
            for g in groups:
                if g not in type_a:
                    try:
                        cmds.setAttr(g + '.visibility', 0)
                    except:
                        pass 
        else:
            type_a = cmds.ls('standard_type_a')
            for g in type_a:
                cmds.setAttr(g + '.visibility', 1)
                    
        if self.btnTypeX.isChecked() or self.btnTypeY.isChecked() or self.btnTypeZ.isChecked(): # kit Y and kit Z
            cmds.setAttr('wheel_arch.visibility', 1)
            try:
                cmds.setAttr('wheel_arch|standard.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|pulled.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|small.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|large.visibility', 0)
            except:
                pass
        
        # ------------------------------------------------
        self._nohide.append(LODa)
        self._nohide.append(LODb)
        self._nohide.append('defaultLayer')
        self._nohide.append(self._currentPart)
        if self.btnPulled.isChecked():
            print 'pulled'
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            self._nohide.append('pulled_wheel_arch_layer') 
            if self.btnLOD0.isChecked():
                self._nohide.append('pulled_type_a_layer')
            if self.btnLOD1.isChecked():
                self._nohide.append('pulled_type_b_layer')
            if self.btnLOD2.isChecked():
                self._nohide.append('pulled_type_c_layer')
            if self.btnLOD3.isChecked():
                self._nohide.append('pulled_type_d_layer')
                
        if self.btnSmall.isChecked():
            print 'pulled'
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            self._nohide.append('small_overfenders_layer') 
                 
        if self.btnLarge.isChecked():
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            print 'large'
            self._nohide.append('large_overfenders_layer')
            if self.btnLOD0.isChecked():
                self._nohide.append('large_type_a_layer')
            if self.btnLOD1.isChecked():
                self._nohide.append('large_type_b_layer')
            if self.btnLOD2.isChecked():
                self._nohide.append('large_type_c_layer')
            if self.btnLOD3.isChecked():
                self._nohide.append('large_type_d_layer')
                
    
        print self._nohide      
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in self._nohide]

        for l in displayLayerNotWork:
            cmds.setAttr(l + '.visibility', 0)
            
        flag = cmds.getAttr(LODa + '.visibility')
        cmds.setAttr(LODa + '.visibility', not flag)
        cmds.setAttr(LODb + '.visibility', flag)
        self.showSpoilers()
        self.showExhausted()
        
    def SwapLODSony(self):
        if self._projectName == 'IronMonkey':
            mel.eval('showHidden -all;')        
        self._nohide = ['base_car_layer', 'spoilers']
        
        if self.rdbSourceLOD0.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbSourceLOD1.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbSourceLOD2.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbSourceLOD3.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbSourceLOD4.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbSourceLOD5.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbSourceLOD6.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbSourceSHADOW.isChecked():
            LODa = mappingLODs(self._projectName,'_SHADOW_')
            
        if self.rdbTargetLOD0.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbTargetLOD1.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbTargetLOD2.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbTargetLOD3.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbTargetLOD4.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbTargetLOD5.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbTargetLOD6.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbTargetSHADOW.isChecked():
            LODb = mappingLODs(self._projectName,'_SHADOW_')
        # ------------------------------------------------
        
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in [LODa, LODb]]
        for l in displayLayerNotWork:
            try:
                cmds.setAttr(l + '.visibility', 0)
            except:
                pass
        flag = cmds.getAttr(LODa + '.visibility')
        cmds.setAttr(LODa + '.visibility', not flag)
        cmds.setAttr(LODb + '.visibility', flag)

    
    def setPosition(self):
        if not self.btnSpreadHonrizonal.isChecked():
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
        else:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', int(self.spnValue.value()) * index)
        if not self.btnSpreadVertical.isChecked():
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)
        else:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', int(self.spnValue.value()) * index)
    
    def moveToNeighborLOD(self, direction):
        indexofCurrentLOD, indexofNeighborLOD = 0,0
        currentLODs = [lod for lod in cmds.ls(type = 'displayLayer') if cmds.getAttr(lod + '.visibility') == True and lod != 'defaultLayer']
        if len(currentLODs) > 1:
            for i in range(1, len(currentLODs)):
                cmds.setAttr(currentLODs[i] + '.visibility', False)
        elif len(currentLODs) == 0:
            currentLODs = ['LOD0']
        indexofCurrentLOD = LODsChain.index(currentLODs[0])
        
        if direction == 'next':
            if indexofCurrentLOD == len(LODsChain) - 1:
                indexofNeighborLOD = 0
            else:
                indexofNeighborLOD = indexofCurrentLOD + 1
            
        if direction == 'previous':
            if indexofCurrentLOD == 0:
                indexofNeighborLOD = len(LODsChain) - 1
            else:
                indexofNeighborLOD = indexofCurrentLOD - 1
                
        cmds.setAttr(LODsChain[indexofNeighborLOD] + '.visibility', True)
        cmds.setAttr(LODsChain[indexofCurrentLOD] + '.visibility', False)
        
    def selectLOD(self, lod):
        type_layer = cmds.ls('type_*_layer')
        if lod == '0':
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [x for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            self._currentPart = 'type_a_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '1':
            try:
                cmds.select('*LOD1')
            except:
                pass
            self._currentPart = 'type_b_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            
        if lod == '2':
            try:
                cmds.select('*LOD2')
            except:
                pass
            self._currentPart = 'type_c_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '3':
            try:
                cmds.select('*LOD3')
            except:
                pass
            self._currentPart = 'type_d_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '4':
            try:
                cmds.select('*LOD4')
            except:
                pass
            self._currentPart = 'kit_x_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == '5':
            try:
                cmds.select('*LOD5')
            except:
                pass
            self._currentPart = 'kit_y_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == '6':
            try:
                cmds.select('*LOD6')
            except:
                pass
            self._currentPart = 'kit_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == 'shadow':
            try:
                cmds.select('*_SHADOW')
            except:
                pass
            self._currentPart = 'kit_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            
        
            
    def loadSpoilerTypeA(self):
        if self.chkSpoiler.isChecked():
            cmds.setAttr('spoiler|type_a.visibility', 1)
        else:
            cmds.setAttr('spoiler|type_a.visibility', 0)
            
def main():
    form = CustomLODTools()
    return form 
    
