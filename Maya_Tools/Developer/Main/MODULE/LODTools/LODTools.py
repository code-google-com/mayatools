import maya.cmds as cmds
import maya.mel as mel
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
IronMonkey_nohide = ['base_car_layer']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/LODTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def mappingLODs(projectName, lod):
    try:
        return globals()[projectName + '_mapping_LODs'][LODsChain.index(lod)]
    except:
        return False # cannot find matched imte with lod

class LODTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'LOD Tools'
        self._projectName = 'IronMonkey'
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
        self.btnLOD7.clicked.connect(functools.partial(self.selectLOD,'7'))
        self.btnLOD8.clicked.connect(functools.partial(self.selectLOD,'8'))
        if not cmds.objExists('LayerSetup'):
            self.btnCleanUp.setEnabled(False)
            self.btnSpreadHonrizonal.setEnabled(False)
            self.btnSpreadVertical.setEnabled(False)
            self.btnPreviousLOD.setEnabled(False)
            self.btnNextLOD.setEnabled(False)
        else:
            self.btnCleanUp.setEnabled(True)
            self.btnSpreadHonrizonal.setEnabled(True)
            self.btnSpreadVertical.setEnabled(True)
            self.btnNextLOD.setEnabled(True)
            self.btnPreviousLOD.setEnabled(True)
            
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
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in ['defaultLayer']]
        try:
            cmds.delete(displayLayerNotWork)
            cmds.delete('LayerSetup')
        except:
            pass
        self.btnCleanUp.setEnabled(False)
        self.btnSpreadHonrizonal.setEnabled(False)
        self.btnSpreadVertical.setEnabled(False)
        self.btnPreviousLOD.setEnabled(False)
        self.btnNextLOD.setEnabled(False)
        
        try:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)  
                #cmds.delete(LODsChain[index].lstrip('_').rstrip('_'))
        except:
            pass
        self.UnParent()
        
    def check(self):
        if not cmds.objExists('LayerSetup'):
            self.createLOD()
        
    def createLOD(self):
        # --
        cmds.createNode('test')
        cmds.rename('unknown1', 'LayerSetup')
        self.btnCleanUp.setEnabled(True)
        self.btnSpreadHonrizonal.setEnabled(True)
        self.btnSpreadVertical.setEnabled(True)
        self.btnNextLOD.setEnabled(True)
        self.btnPreviousLOD.setEnabled(True)
        
        #-- create LOD1 Layer
        try:
            cmds.select('*LOD1*')
            cmds.group(n = 'LOD1')
            cmds.createDisplayLayer(n = '_LOD1_')
            cmds.editDisplayLayerMembers('_LOD1_', cmds.ls(type = 'LOD1'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD2*')
            cmds.group(n = 'LOD2')
            cmds.createDisplayLayer(n = '_LOD2_')
            cmds.editDisplayLayerMembers('_LOD2_', cmds.ls(type = 'LOD2'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD3*')
            cmds.group(n = 'LOD3')
            cmds.createDisplayLayer(n = '_LOD3_')
            cmds.editDisplayLayerMembers('_LOD3_', cmds.ls(type = 'LOD3'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD4*')
            cmds.group(n = 'LOD4')
            cmds.createDisplayLayer(n = '_LOD4_')
            cmds.editDisplayLayerMembers('_LOD4_', cmds.ls(type = 'LOD4'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD5')
            cmds.group(n = 'LOD5')
            cmds.createDisplayLayer(n = '_LOD5_')
            cmds.editDisplayLayerMembers('_LOD5_', cmds.ls(type = 'LOD5'), noRecurse = True)
        except: 
            pass
        
        try:
            cmds.select('*LOD6')
            cmds.group(n = 'LOD6')
            cmds.createDisplayLayer(n = '_LOD6_')
            cmds.editDisplayLayerMembers('_LOD6_', cmds.ls(type = 'LOD6'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*SHADOW')
            cmds.group(n = 'SHADOW')
            cmds.createDisplayLayer(n = '_SHADOW_')
            cmds.editDisplayLayerMembers('_SHADOW_', cmds.ls(type = 'SHADOW'), noRecurse = True)
        except:
            pass
        
        try:
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [x for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            cmds.group(n = 'LOD0')
            cmds.createDisplayLayer(n = '_LOD0_', nr = False)
            cmds.editDisplayLayerMembers('_LOD0_', cmds.ls(type = 'LOD0'), noRecurse = True)
        except:
            pass
        
        cmds.showHidden(all = True)
        
    def SwapLOD(self):
        mel.eval('showHidden -all;')        
        self._nohide = ['base_car_layer']
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
        # ------------------------------------------------
        self._nohide.append(LODa)
        self._nohide.append(LODb)
        self._nohide.append('defaultLayer')
        self._nohide.append(self._currentPart)
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in self._nohide]
        for l in displayLayerNotWork:
            cmds.setAttr(l + '.visibility', 0)
            
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
            self._currentPart = 'type_y_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '5':
            try:
                cmds.select('*LOD5')
            except:
                pass
            self._currentPart = 'type_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '6':
            try:
                cmds.select('*LOD6')
            except:
                pass
            self._currentPart = 'pulled_wheel_arch_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '7':
            try:
                cmds.select('*LOD7')
            except:
                pass 
            self._currentPart = 'small_overfenders_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            #self._nohide.remove('base_car_layer')
        if lod == '8':
            try:
                cmds.select('*LOD7')
            except:
                pass 
            self._currentPart = 'large_overfenders_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
       
def main(xmlFile):
    form = LODTools(xmlFile)
    return form 
    
