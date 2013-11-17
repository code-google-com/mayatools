import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools 
import boltUvRatio
import math
import Source.IconResource_rc
reload(Source.IconResource_rc)

import CommonFunctions as cf

import UvRatio
reload(UvRatio)

#import PolyTools.ExporterandImporter
#reload(PolyTools.ExporterandImporter)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/UVTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

class UVTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'UV tools' 
        self.btnUp.clicked.connect(functools.partial(self.moveUVShell,'up'))
        self.btnDown.clicked.connect(functools.partial(self.moveUVShell,'down'))
        self.btnLeft.clicked.connect(functools.partial(self.moveUVShell,'left'))
        self.btnRight.clicked.connect(functools.partial(self.moveUVShell,'right'))
        self.btnAssignRatio.clicked.connect(self.applyScale)
        self.btnSetTexel.clicked.connect(functools.partial(self.applyScale))
        self.btnUVRatio.clicked.connect(self.openUVRatioToolBox)
        self.btnMirrorU.clicked.connect(functools.partial(self.mirrorUV,'H'))
        self.btnMirrorV.clicked.connect(functools.partial(self.mirrorUV,'V'))
        self.cbbSourceMat.addItems(['Materials from source'])
        self.cbbTargetMat.addItems(['Materials from target'])
        self.ldtSource.addActions([self.actionAddSource, self.actionClearSource, self.actionCopySource, self.actionPasteSource])
        self.ldtTarget.addActions([self.actionAddTarget,self.actionClearTarget, self.actionCopyTarget, self.actionPasteTarget])
        
        self.actionAddSource.triggered.connect(functools.partial(self.getNameFromSelected, 'Source'))
        self.actionAddTarget.triggered.connect(functools.partial(self.getNameFromSelected, 'Target'))
        
        self.actionClearSource.triggered.connect(functools.partial(self.clear, 'Source'))
        self.actionClearTarget.triggered.connect(functools.partial(self.clear, 'Target'))
        
        self.actionCopySource.triggered.connect(functools.partial(self.copy, 'Source'))
        self.actionCopyTarget.triggered.connect(functools.partial(self.copy, 'Target'))
        
        self.actionPasteSource.triggered.connect(functools.partial(self.paste, 'Source'))
        self.actionPasteTarget.triggered.connect(functools.partial(self.paste, 'Target'))
        
        self.ldtSource.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ldtTarget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        #self.ldtSource.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
        #self.ldtTarget.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
        
    def filterTheFirstFaceInCluster(self, inList):
        out = list()
        #firstFilter = filterShaderNodes(inList) # filter 01
        exit = False
        while not exit:
            cmds.select(mesh[0])
            mel.eval('ConvertSelectionToUVShell')
            selFaces = set(cmds.ls(sl = True, fl = True )) 
            a = selFaces.intersection(inList)

    def moveUVShell(self, direction):
        if direction == 'down':
            cmds.polyEditUVShell( u = 0, v = -float(self.lineEdit.text()))
        if direction == 'up':
            cmds.polyEditUVShell( u = 0, v = float(self.lineEdit.text()))
        if direction == 'left':
            cmds.polyEditUVShell( u = -float(self.lineEdit.text()), v = 0)
        if direction == 'right':
            cmds.polyEditUVShell( u = float(self.lineEdit.text()), v = 0)
    
    def validateInfo(self):
        try:
            texel = float(self.ldtTexel.text())
            res = float(self.ldtRes.text())
            ratio = float(self.ldtRatio.text())
        except:
            QtGui.QMessageBox.information(self, 'Wrong data', 'Vui long xem lai cac thong so can thiet da dung chua?', buttons=QMessageBox_Ok, defaultButton=QMessageBox_NoButton)
    
    def applyScale(self):
        boltUvRatio.collect_shells_and_set_shells_UV_ratio(float(self.ldtRatio.text()))
        #selFaces = cmds.ls(sl = True, fl =True)
        #scalePara = float(self.ldtTexel.text()) /int(self.ldtRes.text())  
        #for face in selFaces:
        #    cmds.unfold(face, i = 0, ss=0.001, gb = 0, gmb = 1, pub = 0, ps = 0, oa = 0, us = True, s = scalePara)
            
    def on_ldtRes_returnPressed(self):
        #self.validateInfo()
        self.ldtTexel.setText( str(float(self.ldtRes.text())/math.sqrt(float(self.ldtRatio.text()))))
    
    def on_ldtRatio_returnPressed(self):
        #self.validateInfo()
        self.ldtTexel.setText( str ( float(self.ldtRes.text())/math.sqrt(float(self.ldtRatio.text()))))
        
    def on_ldtTexel_returnPressed(self):
        #self.validateInfo()
        self.ldtRatio.setText( str(math.pow(float(self.ldtRes.text())/float(self.ldtTexel.text()),2)) )
        
    def openUVRatioToolBox(self):
        reload(UvRatio)
        self.uvRatio = UvRatio.UVRatio()
        self.uvRatio.show()
        
    def mirrorUV(self,direction):#, pivotPoint = setPivotMirror()):
        meshes = cmds.ls(hl = True)
        UVs = cmds.ls(sl = True)
        filterMesh = []
        for i in meshes:
            temp = []
            for j in UVs:
                if j.split('.')[0] == i:
                    temp.append(j)
            filterMesh.append(temp)
        cmds.select(cl = True)
        for l in filterMesh:
            try:
                cmds.select(l)
                if direction == 'V':
                    cmds.polyMoveUV(pivot = [0,0], scaleV = -1)
                if direction == 'H':
                    cmds.polyMoveUV(pivot = [0,0], scaleU = -1)
            except:
                pass
            
    def createRightClickonMenu_on_selectedItems(self,pos):
            RightClickMenu = QtGui.QMenu(self)
            RightClickMenu.addAction(self.actionAdd)
            RightClickMenu.exec_(QtGui.QCursor.pos())
            
    def getNameFromSelected(self, widget):
        objName = cmds.ls(sl = True)[0]
        # get shader from nodes
        shapeNode = cmds.listRelatives(c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
        for sg in sgs:
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                shaders.append(shader)
        # ---------------------------
        if widget =='Source':
            self.ldtSource.setText(objName)
            self.cbbSourceMat.clear()
            self.cbbSourceMat.addItems(shaders)
            # test whether material in source and target matched together
            
        if widget =='Target':
            self.ldtTarget.setText(objName)
            self.cbbTargetMat.clear()
            self.cbbTargetMat.addItems(shaders)
            
    def clear(self, widget):
        if widget =='Source':
            self.ldtSource.setText('')
        if widget =='Target':
            self.ldtTarget.setText('')
            
    def copy(self, widget):
        if widget =='Source':
            cf.setDataToClipboard(self.ldtSource.text())
        if widget =='Target':
            cf.setDataToClipboard(self.ldtTarget.text())
            
    def paste(self, widget):
        if widget =='Source':
            self.ldtSource.setText(cf.getDataFromClipboard())
        if widget =='Target':
            self.ldtTarget.setText(cf.getDataFromClipboard())
        
        
def main(xmlFile):
    form = UVTools(xmlFile)
    return form  