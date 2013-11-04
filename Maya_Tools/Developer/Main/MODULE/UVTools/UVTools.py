import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools 
import boltUvRatio
import math
import Source.IconResource_rc
reload(Source.IconResource_rc)

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
        
def main(xmlFile):
    form = UVTools(xmlFile)
    return form  