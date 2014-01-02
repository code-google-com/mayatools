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
IronMonkey_nohide = ['base_car_layer','spoilers']

lods = ['lod_00','lod_01','lod_02','lod_03','lod_04','lod_05','lod_06']
parts = ['type_a','type_b','type_c','type_d','type_y','type_z', 'pulled_type_a','pulled_type_b', 'pulled_type_c', 'pulled_type_d',
         'large_type_a', 'large_type_b', 'large_type_c', 'large_type_d',
         'small_type_a','small_type_b', 'small_type_c', 'small_type_d']#,'pull_wheelarch','large_overfender','small_overfender']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/LODTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def mappingLODs(projectName, lod):
    try:
        return globals()[projectName + '_mapping_LODs'][LODsChain.index(lod)]
    except:
        return False # cannot find matched imte with lod
    
def setupLOD():
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
        cmds.createDisplayLayer(n = 'base_unwrap')
        cmds.createDisplayLayer(n = 'spoilers')
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
        # adding wheelarch standard to type a
        #cmds.editDisplayLayerMembers('type_a_layer', cmds.ls('wheel_arch|standard'), noRecurse = True)
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
        cmds.editDisplayLayerMembers('base_car_layer', cmds.ls('rotor|type_a','caliper|type_a','chassis|type_a','body|type_a','interior|type_a','windows|type_a','headlights|type_a','taillights|type_a','wheel_arch|standard'), noRecurse = True)
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
        # select misc meshes
        try:
            cmds.editDisplayLayerMembers('base_unwrap', cmds.ls('base_unwrap'), noRecurse = True)
        except:
            pass
        # add spoilers to layers
        try:
            cmds.editDisplayLayerMembers('spoilers', cmds.ls('spoiler|*'), noRecurse = True)
        except:
            pass

class LODTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'LOD Tools'
        self._projectName = inputFile.split('.')[0]
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
        #self.btnLOD6.clicked.connect(functools.partial(self.selectLOD,'6'))
        #self.btnLOD7.clicked.connect(functools.partial(self.selectLOD,'7'))
        #self.btnLOD8.clicked.connect(functools.partial(self.selectLOD,'8'))
        self.cbbSpoilers.currentIndexChanged.connect(self.showSpoilers)
        ############################ BUTTON LOAD LAYER
        self.btnStandard.clicked.connect(functools.partial(self.loadStandard_Clicked))
        self.btnPulled.clicked.connect(functools.partial(self.loadPulled_Clicked))
        self.btnSmall.clicked.connect(functools.partial(self.loadSmall_Clicked))
        self.btnLarge.clicked.connect(functools.partial(self.loadLarge_Clicked))
        
        
        self.btnLOD0.setChecked(True)
        self.btnStandard.setChecked(True)


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
        if self._projectName == 'IronMonkey':
            setupLOD()
            childrenOfSpoilers = cmds.listRelatives('spoiler', c = True)
            self.cbbSpoilers.addItems(childrenOfSpoilers)
        else:
            if not cmds.objExists('LayerSetup'):
                self.createLOD()
                
    def showSpoilers(self):
        spoiler = self.cbbSpoilers.currentText()
        for s in cmds.listRelatives('spoiler', c = True, f= True):
            if str(spoiler) in s:
                cmds.setAttr(s + '.visibility', 1)
            else:
                cmds.setAttr(s + '.visibility', 0)
        
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
    '''    
    def SwapLOD(self):
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
                    
        if self.btnLOD5.isChecked() or self.btnLOD4.isChecked(): # kit Y and kit Z
            cmds.setAttr('wheel_arch.visibility', 0)
            
        
        # ------------------------------------------------
        self._nohide.append(LODa)
        self._nohide.append(LODb)
        self._nohide.append('defaultLayer')
        self._nohide.append(self._currentPart)
        if self.btnLOD6.isChecked():
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            print 'pulled'
            self._nohide.append('pulled_wheel_arch_layer') 
            if self.btnLOD0.isChecked():
                self._nohide.append('pulled_type_a_layer')
            if self.btnLOD1.isChecked():
                self._nohide.append('pulled_type_b_layer')
            if self.btnLOD2.isChecked():
                self._nohide.append('pulled_type_c_layer')
            if self.btnLOD3.isChecked():
                self._nohide.append('pulled_type_d_layer')
                 
        if self.btnLOD8.isChecked():
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
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in self._nohide]
        for l in displayLayerNotWork:
            cmds.setAttr(l + '.visibility', 0)
            
        flag = cmds.getAttr(LODa + '.visibility')
        cmds.setAttr(LODa + '.visibility', not flag)
        cmds.setAttr(LODb + '.visibility', flag)
        self.showSpoilers()
    '''
    ###################### SWITCH LOAD NEW ############################
    def SwapLOD(self):
        layerSource =[]
        layerTarget=[]
        sourceLOD=''
        TargetLOD=''
        if self._projectName == 'IronMonkey':
            mel.eval('showHidden -all;')        
        self._nohide = ['base_car_layer', 'spoilers']
        
        if self.rdbSourceLOD0.isChecked():
            sourceLOD='LOD0'
        elif self.rdbSourceLOD1.isChecked():
            sourceLOD ='LOD1'
        elif self.rdbSourceLOD2.isChecked():
            sourceLOD ='LOD2'
        elif self.rdbSourceLOD3.isChecked():
            sourceLOD ='LOD3'
        elif self.rdbSourceLOD4.isChecked():
            sourceLOD ='LOD4'
        elif self.rdbSourceLOD5.isChecked():
            sourceLOD ='LOD5'
        elif self.rdbSourceLOD6.isChecked():
            sourceLOD ='LOD6'
        elif self.rdbSourceSHADOW.isChecked():
            LODa = mappingLODs(self._projectName,'_SHADOW_')
            
        if self.rdbTargetLOD0.isChecked():
            TargetLOD = 'LOD0'
        elif self.rdbTargetLOD1.isChecked():
            TargetLOD = 'LOD1'
        elif self.rdbTargetLOD2.isChecked():
            TargetLOD = 'LOD2'
        elif self.rdbTargetLOD3.isChecked():
            TargetLOD = 'LOD3'
        elif self.rdbTargetLOD4.isChecked():
            TargetLOD = 'LOD4'
        elif self.rdbTargetLOD5.isChecked():
            TargetLOD = 'LOD5'
        elif self.rdbTargetLOD6.isChecked():
            TargetLOD = 'LOD6'
        elif self.rdbTargetSHADOW.isChecked():
            LODb = mappingLODs(self._projectName,'_SHADOW_')
        # ------------------------------------------------
        ###########################################################################
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
        ###########################################################################
        listLayer = [layer for layer in cmds.ls(type='displayLayer') if layer not in ['defaultLayer']]
        #print listLayer
        #for n in listLayer:
         #    cmds.setAttr(n+'.visibility',0)
        print'##################################################'
        flagSource = self.checkLoadActiveSource(sourceLOD)
        print 'flag source'
        print flagSource
        print '_____________End LOD SOURCE________'
        flagTarget =self.checkLoadActiveTarget(TargetLOD)
        print 'flag Target'
        print flagTarget
        print '_____________END LOD TARGET_________'
        ########################################
        
        if flagSource ==1:
            if flagTarget ==0:
                print 'Chuyen ve lod Target'            
                for j in range(0,7):
                    if TargetLOD == 'LOD'+str(j):
                        #print TargetLOD
                        layerTarget = self.loadLODTarget(j)
                        #print layerTarget
                        for layer in layerTarget:
                            cmds.setAttr(layer+'.visibility',1)
                listLayerHide = [x for x in listLayer if (x not in layerTarget)]         
                for hide in listLayerHide:
                    cmds.setAttr(hide+'.visibility',0)
            elif flagTarget ==1:
                print 'chuyen ve lod Source neu flagtarget=1 va flagSource =1' 
                for j in range(0,7):
                    if 'LOD'+str(j) == sourceLOD:
                        #print sourceLOD
                        layerSource = self.loadLODSource(j)
                        #print layerSource
                        for layer in layerSource:
                            cmds.setAttr(layer+'.visibility',1)
                listLayerHide = [x for x in listLayer if (x not in layerSource)]
                #print listLayerHide         
                for hide in listLayerHide:
                    cmds.setAttr(hide+'.visibility',0)
        elif flagSource==0:
            if flagTarget == 1:
                print 'chuyen ve lod Source neu flagtarget=1' 
                for j in range(0,7):
                    if 'LOD'+str(j) == sourceLOD:
                        #print sourceLOD
                        layerSource = self.loadLODSource(j)
                        #print layerSource
                        for layer in layerSource:
                            cmds.setAttr(layer+'.visibility',1)
                listLayerHide = [x for x in listLayer if (x not in layerSource)]
                #print listLayerHide         
                for hide in listLayerHide:
                    cmds.setAttr(hide+'.visibility',0)
            elif flagTarget ==0:
                print 'Chuyen ve lod Source neu flagtarget =0' 
                for j in range(0,7):
                    if 'LOD'+str(j) == sourceLOD:
                        #print sourceLOD
                        layerSource = self.loadLODSource(j)
                        #print layerSource
                        for layer in layerSource:
                            cmds.setAttr(layer+'.visibility',1)
                listLayerHide = [x for x in listLayer if (x not in layerSource)]
                #print listLayerHide         
                for hide in listLayerHide:
                    cmds.setAttr(hide+'.visibility',0)
        self.showSpoilers()
                                           
    ########### LOAD LAYER THEO LOAD
    def checkLoadActiveSource(self,lodSource):
        print 'source Lod'
        print lodSource
        
        flagSource = ''
        for i in range(0,7):
            
            if 'LOD'+str(i)==lodSource:
                
                visible = cmds.getAttr('lod_0'+str(i)+'_layer.visibility')
                print'Lod thu: '
                print 'LOD'+str(i)
               # print i
                if visible ==True:
                    flagSource =1
                else:
                    flagSource =0
        
        return flagSource
        
    def checkLoadActiveTarget(self,lodTarget):
        flagTarget = ''
        print 'check Lod Target'
        print lodTarget
        for j in range(0,7):
            
            #print 'LOD'+str(j)
            
            if 'LOD'+str(j)==lodTarget:
                print 'LOD'+str(j)
                print 'lay du lieu'
            
                visible = cmds.getAttr('lod_0'+str(j)+'_layer.visibility')
                print visible
                if visible ==True:
                    #print 'test thu'
                    flagTarget = 1
                else:
                    flagTarget = 0
        
        return flagTarget
            
            
    def loadLODSource(self,lodNum):
        layerLod = ['lod_0'+str(lodNum)+'_layer','spoilers','base_car_layer','locator_layer']
        if self.btnLOD0.isChecked():
            layerLod.append('type_a_layer')
                    
        elif self.btnLOD1.isChecked():
            layerLod.append('type_b_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_a_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
           
        elif self.btnLOD2.isChecked():
            layerLod.append('type_c_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_c_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():#large_overfenders_layer
                layerLod.append('large_type_c_layer')
                layerLod.append('large_overfenders_layer')
                
        elif self.btnLOD3.isChecked():
            layerLod.append('type_d_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_d_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_type_d_layer')
                layerLod.append('large_overfenders_layer')
        
        elif self.btnLOD4.isChecked():
            layerLod.append('type_y_layer')
            if self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_overfenders_layer')
        
        elif self.btnLOD5.isChecked():
            layerLod.append('type_z_layer')
            if self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_overfenders_layer')
            
        
        return layerLod
    def loadLODTarget(self,lodNum):
        layerLod = ['lod_0'+str(lodNum)+'_layer','spoilers','base_car_layer','locator_layer']
        if self.btnLOD0.isChecked():
            layerLod.append('type_a_layer')
            
        elif self.btnLOD1.isChecked():
            layerLod.append('type_b_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_a_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
        elif self.btnLOD2.isChecked():
            layerLod.append('type_c_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_c_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():#large_overfenders_layer
                layerLod.append('large_type_c_layer')
                layerLod.append('large_overfenders_layer')
        elif self.btnLOD3.isChecked():
            layerLod.append('type_d_layer')
            if self.btnPulled.isChecked():
                layerLod.append('pulled_type_d_layer')
                layerLod.append('pulled_wheel_arch_layer')
            elif self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_type_d_layer')
                layerLod.append('large_overfenders_layer')
        elif self.btnLOD4.isChecked():
            layerLod.append('type_y_layer')
            if self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_overfenders_layer')
        elif self.btnLOD5.isChecked():
            layerLod.append('type_z_layer')
            if self.btnSmall.isChecked():
                layerLod.append('small_overfenders_layer')
            elif self.btnLarge.isChecked():
                layerLod.append('large_overfenders_layer')
        return layerLod
    ####################### END SWITCH LOAD ############################
    
    
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
                
    ########################## LOAD LAYER
    '''
    def nextLayerSwap_Clicked(self):
        nextLayer = self.getNextLayer()
        cmds.setAttr(nextLayer + '.visibility', 1)
        preLayer = self.getPreLayer()
        cmds.setAttr(preLayer + '.visibility', 0)
    '''
    ######################### GETLIST LAYER
    '''
    def getPreLayer(self,wheelArch):
        listLayer = [layer for layer in cmds.ls(type='displayLayer') if layer not in ['defaultLayer']]
        if wheelArch == 'Standard':
            listType = [type for type in listLayer if re.search('(.*)type(\.*)', type)]
            
        if wheelArch == 'PULLED':
            listType = [type for type in listLayer if re.search('(.*)type(\.*)', type)]
        if wheelArch =='SMALL':
            listType = [type for type in listLayer if re.search('(.*)type(\.*)', type)]
        if wheelArch =='LARGE':
            listType = [type for type in listLayer if re.search('(.*)type(\.*)', type)]
        
        preIndex=''
        for index, obj in enumerate(listLayer):
           preIndex = listLayer[index]
           break
        return preIndex
        '''
    ########################## FUNCTION GET VALUE
    
    def loadStandard_Clicked(self):
        cmds.setAttr('pulled_type_a_layer.visibility', 0)
        cmds.setAttr('pulled_type_d_layer.visibility', 0)
        cmds.setAttr('pulled_type_c_layer.visibility', 0)
        cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
        cmds.setAttr('large_type_d_layer.visibility', 0)
        cmds.setAttr('large_type_c_layer.visibility', 0)
        cmds.setAttr('large_overfenders_layer.visibility', 0)
        cmds.setAttr('small_overfenders_layer.visibility', 0)
         
    def loadPulled_Clicked(self):
        listLayer = [layer for layer in cmds.ls(type='displayLayer') if layer not in ['defaultLayer']]
        listType = [type for type in listLayer if re.search('type', type)]
        cmds.setAttr('large_type_d_layer.visibility', 0)
        cmds.setAttr('large_type_c_layer.visibility', 0)
        cmds.setAttr('large_overfenders_layer.visibility', 0)
        cmds.setAttr('small_overfenders_layer.visibility', 0)
        for type in listType:
            if type == 'type_a_layer':
                visible = cmds.getAttr(type+'.visibility')
                if visible ==1:
                    cmds.setAttr('pulled_type_a_layer.visibility', 1)
                    cmds.setAttr('pulled_type_d_layer.visibility', 0)
                    cmds.setAttr('pulled_type_c_layer.visibility', 0)
                    cmds.setAttr('pulled_wheel_arch_layer.visibility', 1)
        
            if type == 'type_c_layer':
                visible = cmds.getAttr(type+'.visibility')
                if visible==1:
                    cmds.setAttr('pulled_type_a_layer.visibility', 0)
                    cmds.setAttr('pulled_type_d_layer.visibility', 0)
                    cmds.setAttr('pulled_type_c_layer.visibility', 1)
                    cmds.setAttr('pulled_wheel_arch_layer.visibility', 1)
            if type== 'type_d_layer':
                visible = cmds.getAttr(type+'.visibility')
                if visible==1:
                    cmds.setAttr('pulled_type_a_layer.visibility', 0)
                    cmds.setAttr('pulled_type_d_layer.visibility', 1)
                    cmds.setAttr('pulled_type_c_layer.visibility', 0)
                    cmds.setAttr('pulled_wheel_arch_layer.visibility', 1)
           
    def loadSmall_Clicked(self):
        cmds.setAttr('pulled_type_a_layer.visibility', 0)
        cmds.setAttr('pulled_type_d_layer.visibility', 0)
        cmds.setAttr('pulled_type_c_layer.visibility', 0)
        cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
        cmds.setAttr('large_type_d_layer.visibility', 0)
        cmds.setAttr('large_type_c_layer.visibility', 0)
        cmds.setAttr('large_overfenders_layer.visibility', 0)
        cmds.setAttr('small_overfenders_layer.visibility', 1)
        
    def loadLarge_Clicked(self):
        listLayer = [layer for layer in cmds.ls(type='displayLayer') if layer not in ['defaultLayer']]
        listType = [type for type in listLayer if re.search('type', type)]
        cmds.setAttr('pulled_type_a_layer.visibility', 0)
        cmds.setAttr('pulled_type_d_layer.visibility', 0)
        cmds.setAttr('pulled_type_c_layer.visibility', 0)
        cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
        cmds.setAttr('small_overfenders_layer.visibility', 0)
        for type in listType:
            if type=='type_c_layer':
                visible = cmds.getAttr(type+'.visibility')
                if visible==1:
                    cmds.setAttr('large_type_d_layer.visibility', 0)
                    cmds.setAttr('large_type_c_layer.visibility', 1)
                    cmds.setAttr('large_overfenders_layer.visibility', 1)
            if type =='type_d_layer':
                visible = cmds.getAttr(type+'.visibility')
                if visible==1:
                    cmds.setAttr('large_type_d_layer.visibility', 1)
                    cmds.setAttr('large_type_c_layer.visibility', 0)
                    cmds.setAttr('large_overfenders_layer.visibility', 1)
    
    ######################################## END LOAD LAYER ###################################################    
    
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
            self._currentPart = 'type_y_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '5':
            try:
                cmds.select('*LOD5')
            except:
                pass
            self._currentPart = 'type_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
#         if lod == '6':
#             try:
#                 cmds.select('*LOD6')
#             except:
#                 pass
#             self._currentPart = 'pulled_wheel_arch_layer'
#             cmds.setAttr(self._currentPart + '.visibility', 1)
#         if lod == '7':
#             try:
#                 cmds.select('*LOD7')
#             except:
#                 pass 
#             self._currentPart = 'small_overfenders_layer'
#             cmds.setAttr(self._currentPart + '.visibility', 1)
#             #self._nohide.remove('base_car_layer')
#         if lod == '8':
#             try:
#                 cmds.select('*LOD7')
#             except:
#                 pass 
#             self._currentPart = 'large_overfenders_layer'
#             cmds.setAttr(self._currentPart + '.visibility', 1)
#             
        for l in type_layer:
             if l != self._currentPart:
                 cmds.setAttr(l + '.visibility', 0)
def main(xmlFile):
    
    form = LODTools(xmlFile)
    return form 
    
