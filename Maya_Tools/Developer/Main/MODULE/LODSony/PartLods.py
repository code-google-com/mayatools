import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import re

from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import functools 

LODsChain = ['partAero_00_layer','partAero_01_layer','partAero_02_layer','partAero_03_layer']
#Lods:
Sony_mapping_LODs = ['_PART0_','_PART1_','_PART2_','_PART3_']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/PartLods.ui'

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
        cmds.createDisplayLayer(n = 'partWings_00')
        cmds.createDisplayLayer(n = 'partWings_01')
        cmds.createDisplayLayer(n = 'partWings_02')
        cmds.createDisplayLayer(n = 'partWings_03')
        cmds.createDisplayLayer(n = 'partAero_00')
        cmds.createDisplayLayer(n = 'partAero_01')
        cmds.createDisplayLayer(n = 'partAero_02')
        cmds.createDisplayLayer(n = 'partAero_03')
        cmds.createDisplayLayer(n = 'Light_on')
        cmds.createDisplayLayer(n = 'NormalBody')
        
        
       
        # adding wheelarch standard to type a
        #cmds.editDisplayLayerMembers('type_a_layer', cmds.ls('wheel_arch|standard'), noRecurse = True)
        # select partWings_00 and put them in 
        try:
            #cmds.editDisplayLayerMembers('partWings_00_layer', cmds.ls(type = 'PartsWing_00'), noRecurse = True)
            cmds.editDisplayLayerMembers('partWings_00', cmds.ls('PartsWing_00'), noRecurse = True)
        except:
            pass
        # select partWings_01 and put them in
        try:
            cmds.editDisplayLayerMembers('partWings_01', cmds.ls('ParstWing_01'), noRecurse = True)
        except:
            pass
       
        # select partWings_02 and put them in
        try:
            cmds.editDisplayLayerMembers('partWings_02', cmds.ls('PartsWing_02'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.editDisplayLayerMembers('partWings_03', cmds.ls('PartsWing_03'), noRecurse = True)
        except:
            pass
        
        # Select PartBody and put them in
        try:
            cmds.editDisplayLayerMembers('NormalBody', cmds.ls('PartsBody'), noRecurse = True)
        except:
            pass
        
        # select Part Aero add them to layer
        # Aero_00
        try:
            cmds.editDisplayLayerMembers('partAero_00', cmds.ls('PartsAero_00'), noRecurse = True)
        except:
            pass
        # Aero_01
        try:
            cmds.editDisplayLayerMembers('partAero_01', cmds.ls('PartsAero_01'), noRecurse = True)
        except:
            pass
        # Aero_02
        try:
            cmds.editDisplayLayerMembers('partAero_02', cmds.ls('PartsAero_02'), noRecurse = True)
        except:
            pass   
        # Aero_03
        try:
            cmds.editDisplayLayerMembers('partAero_03', cmds.ls('PartsAero_03'), noRecurse = True)
        except:
            pass
       
class PartLods(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Part LOD'
        print self.__name__
        #self._projectName = 
        self._projectName = inputFile.split('.')[0]
        self._nohide = list()
        self._currentPart = ''
        # Disable botton
        self.btnSpreadHonrizonal.setEnabled(False)
        self.btnSpreadVertical.setEnabled(False)
        self.btnPreviousLOD.setEnabled(False)
        self.btnNextLOD.setEnabled(False)
        self.spnValue.setEnabled(False)
        
        # Setup Part
        self.btnSetupLOD.clicked.connect(self.check)
        # Switch LOD
        self.btnSwitchLOD.clicked.connect(self.SwapLOD)
        
        self.btnCleanUp.clicked.connect(self.CleanUp)
        self.btnSpreadHonrizonal.clicked.connect(self.setPosition)
        self.btnSpreadVertical.clicked.connect(self.setPosition)
        
        self.btnPreviousLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'previous'))
        self.btnNextLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'next'))
        self.spnValue.valueChanged.connect(self.setPosition)
       
        self.cbbSpoilers.currentIndexChanged.connect(self.showSpoilers)
       


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
        #self.btnSpreadHonrizonal.setEnabled(False)
        #self.btnSpreadVertical.setEnabled(False)
        #self.btnPreviousLOD.setEnabled(False)
        #self.btnNextLOD.setEnabled(False)
        
        try:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)  
                #cmds.delete(LODsChain[index].lstrip('_').rstrip('_'))
        except:
            pass
        #self.UnParent()
        
    def check(self):
        
        print "Project Name ###: "
        print self._projectName
        print "############"
        if self._projectName == 'BanDaiNamCo':
            setupLOD()
            childrenOfSpoilers = cmds.listRelatives('PartsWings', c = True)
            childrenOfSpoilers.append('---Nothing---')
            
            self.cbbSpoilers.clear()
            for i in range(0, len(childrenOfSpoilers)):
                if childrenOfSpoilers[i]=='PartsWing_00':
                    self.cbbSpoilers.addItems(['partWings_00'])
                if childrenOfSpoilers[i]=='PartsWing_01':
                    self.cbbSpoilers.addItems(['partWings_01'])
                if childrenOfSpoilers[i]=='PartsWing_02':
                    self.cbbSpoilers.addItems(['partWings_02'])
                if childrenOfSpoilers[i]=='PartsWing_03':
                    self.cbbSpoilers.addItems(['partWings_03'])
            
            
        #else:
            #if not cmds.objExists('LayerSetup'):
                #self.createLOD()
          
        
    def SwapLOD(self):
        if self._projectName == 'BanDaiNamCo':
            self.SwapLODBanDaiNamCo()
        if self._projectName == 'Sony':
            self.SwapLODSony()
        
    def SwapLODBanDaiNamCo(self):
        if self._projectName == 'BanDaiNamCo':
            mel.eval('showHidden -all;')        
        self._nohide = ['partBody_layer']
        
        if self.rdbSourceLOD0.isChecked():
            #LODa = mappingLODs(self._projectName,'partAero_00_layer')
            #self._nohide.append('LODa')
            LODa = 'partAero_00'
        elif self.rdbSourceLOD1.isChecked():
            #LODa = mappingLODs(self._projectName,'partAero_01_layer')
            #self._nohide.append('partAero_01_layer')
            LODa = 'partAero_01'
        elif self.rdbSourceLOD2.isChecked():
            #LODa = mappingLODs(self._projectName,'partAero_02_layer')
            #self._nohide.append('partAero_02_layer')
            LODa = 'partAero_02'
        elif self.rdbSourceLOD3.isChecked():
            #LODa = mappingLODs(self._projectName,'partAero_03_layer')
            #self._nohide.append('partAero_03_layer')
            LODa = 'partAero_03'
            
        if self.rdbTargetLOD0.isChecked():
            #LODb = mappingLODs(self._projectName,'partAero_00_layer')
            #self._nohide.append('partAero_00_layer')
            LODb ="partAero_00"
        elif self.rdbTargetLOD1.isChecked():
            #LODb = mappingLODs(self._projectName,'partAero_01_layer')
            #self._nohide.append('partAero_01_layer')
            LODb ="partAero_01"
        elif self.rdbTargetLOD2.isChecked():
            #LODb = mappingLODs(self._projectName,'partAero_02_layer')
            #self._nohide.append('partAero_02_layer')
            LODb ="partAero_02"
        elif self.rdbTargetLOD3.isChecked():
            #LODb = mappingLODs(self._projectName,'partAero_03_layer')
            #self._nohide.append('partAero_03_layer')
            LODb ="partAero_03"
        
        # ------------------------------------------------
        
        # ------------------------------------------------
        self._nohide.append(LODa)
        self._nohide.append(LODb)
        self._nohide.append('defaultLayer')
        #self._nohide.append(self._currentPart)
        print "Danh sach No Hiden: "
        print self._nohide      
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in self._nohide]
        print "displayLayer Not Work: "
        print displayLayerNotWork
        for l in displayLayerNotWork:
            cmds.setAttr(l + '.visibility', 0)
            
        flag = cmds.getAttr(LODa + '.visibility')
        cmds.setAttr(LODa + '.visibility', not flag)
        cmds.setAttr(LODb + '.visibility', flag)
        cmds.setAttr('NormalBody.visibility',True)
        #self.showSpoilers()
        #self.showExhausted()
          
    def showSpoilers(self):
        spoiler = str(self.cbbSpoilers.currentText())
        list =['partWings_00','partWings_01','partWings_02','partWings_03']
        listInKit  = [layer for layer in cmds.ls(type='displayLayer') if layer not in ['defaultLayer']]
        listWing = [node for node in listInKit if re.search('partWings_', node)]
        print listWing
        if spoiler == '---Nothing---':
            for i in listWing:
                cmds.setAttr(i + '.visibility', 0)
        else:
            for s in listWing:
                #print spoiler
                if str(spoiler) == s:
                    cmds.setAttr(s + '.visibility', 1)
                    print spoiler
                else:
                    cmds.setAttr(s + '.visibility', 0)
        '''    
        for s in cmds.listRelatives(spoiler, c = True, f= True):
            if spoiler == '---Nothing---':
                cmds.setAttr(s + '.visibility', 0)
            else:
                if str(spoiler) in s:
                    cmds.setAttr(s + '.visibility', 1)
                else:
                    cmds.setAttr(s + '.visibility', 0)
        '''
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
        if lod == 'x':
            try:
                cmds.select('*LOD4')
            except:
                pass
            self._currentPart = 'kit_x_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == 'y':
            try:
                cmds.select('*LOD5')
            except:
                pass
            self._currentPart = 'kit_y_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == 'z':
            try:
                cmds.select('*LOD6')
            except:
                pass
            self._currentPart = 'kit_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            
        if lod == 'pulled':
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 1)
            cmds.setAttr('large_overfenders_layer.visibility', 0)
            cmds.setAttr('small_overfenders_layer.visibility', 0)
            if self.btnLOD0.isChecked():
                cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD1.isChecked():
                if cmds.objExists('pulled_type_b_layer'):
                    cmds.setAttr('pulled_type_b_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD2.isChecked():
                if cmds.objExists('pulled_type_c_layer'):
                    cmds.setAttr('pulled_type_c_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD3.isChecked():
                if cmds.objExists('pulled_type_d_layer'):
                    cmds.setAttr('pulled_type_d_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
        
        if lod == 'small':
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
            cmds.setAttr('large_overfenders_layer.visibility', 0)
            cmds.setAttr('small_overfenders_layer.visibility', 1)
            
        
        if lod == 'large':
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
            cmds.setAttr('large_overfenders_layer.visibility', 1)
            cmds.setAttr('small_overfenders_layer.visibility', 0)
            if self.btnLOD0.isChecked():
                cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD1.isChecked():
                if cmds.objExists('large_type_b_layer'):
                    cmds.setAttr('large_type_b_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD2.isChecked():
                if cmds.objExists('large_type_c_layer'):
                    cmds.setAttr('large_type_c_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD3.isChecked():
                if cmds.objExists('large_type_d_layer'):
                    cmds.setAttr('large_type_d_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            
    def loadSpoilerTypeA(self):
        if self.chkSpoiler.isChecked():
            cmds.setAttr('spoiler|type_a.visibility', 1)
        else:
            cmds.setAttr('spoiler|type_a.visibility', 0)
            
def main(xmlFile):
    form = PartLods(xmlFile)
    return form 
    
