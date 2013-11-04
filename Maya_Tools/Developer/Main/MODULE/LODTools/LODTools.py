import maya.cmds as cmds
import re

from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import functools 

LODsChain = ['_LOD0_','_LOD1_','_LOD2_','_LOD3_','_LOD4_','_LOD5_','_LOD6_']
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/LODTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

class LODTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'LOD Tools'
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
            cmds.createDisplayLayer(e = False, n = '_LOD1_')
        except:
            pass
        
        try:
            cmds.select('*LOD2*')
            cmds.group(n = 'LOD2')
            cmds.createDisplayLayer(e = False, n = '_LOD2_')
        except:
            pass
        
        try:
            cmds.select('*LOD3*')
            cmds.group(n = 'LOD3')
            cmds.createDisplayLayer(e = False, n = '_LOD3_')
        except:
            pass
        
        try:
            cmds.select('*LOD4*')
            cmds.group(n = 'LOD4')
            cmds.createDisplayLayer(e = False, n = '_LOD4_')
        except:
            pass
        
        try:
            cmds.select('*LOD5')
            cmds.group(n = 'LOD5')
            cmds.createDisplayLayer(e = False, n = '_LOD5_')
        except: 
            pass
        
        try:
            cmds.select('*LOD6')
            cmds.group(n = 'LOD6')
            cmds.createDisplayLayer(e = False, n = '_LOD6_')
        except:
            pass
        
        try:
            cmds.select('*SHADOW')
            cmds.group(n = 'SHADOW')
            cmds.createDisplayLayer(e = False, n = '_SHADOW_')
        except:
            pass
        
        try:
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [x for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            cmds.group(n = 'LOD0')
            cmds.createDisplayLayer(e = False, n = '_LOD0_', nr = False)
        except:
            pass
        
        cmds.showHidden(all = True)
        
    def SwapLOD(self):
        LODa, LODb = '_LOD0_','_LOD1_'
        if self.rdbSourceLOD0.isChecked():
            LODa = '_LOD0_'
        elif self.rdbSourceLOD1.isChecked():
            LODa = '_LOD1_'
        elif self.rdbSourceLOD2.isChecked():
            LODa = '_LOD2_'
        elif self.rdbSourceLOD3.isChecked():
            LODa = '_LOD3_'
        elif self.rdbSourceLOD4.isChecked():
            LODa = '_LOD4_'
        elif self.rdbSourceLOD5.isChecked():
            LODa = '_LOD5_'
        elif self.rdbSourceLOD6.isChecked():
            LODa = '_LOD6_'
        elif self.rdbSourceSHADOW.isChecked():
            LODa = '_SHADOW_'
            
        if self.rdbTargetLOD0.isChecked():
            LODb = '_LOD0_'
        elif self.rdbTargetLOD1.isChecked():
            LODb = '_LOD1_'
        elif self.rdbTargetLOD2.isChecked():
            LODb = '_LOD2_'
        elif self.rdbTargetLOD3.isChecked():
            LODb = '_LOD3_'
        elif self.rdbTargetLOD4.isChecked():
            LODb = '_LOD4_'
        elif self.rdbTargetLOD5.isChecked():
            LODb = '_LOD5_'
        elif self.rdbTargetLOD6.isChecked():
            LODb = '_LOD6_'
        elif self.rdbTargetSHADOW.isChecked():
            LODb = '_SHADOW_'
        
        # --
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in [LODa, LODb, 'defaultLayer']]
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
        if lod == '1':
            cmds.select('*LOD1')
        if lod == '2':
            cmds.select('*LOD2')
        if lod == '3':
            cmds.select('*LOD3')
        if lod == '4':
            cmds.select('*LOD4')
        if lod == '5':
            cmds.select('*LOD5')
        if lod == '6':
            cmds.select('*LOD6')
        if lod == 'shadow':
            cmds.select('*SHADOW') 
        
                    
def main(xmlFile):
    form = LODTools(xmlFile)
    return form 
    
