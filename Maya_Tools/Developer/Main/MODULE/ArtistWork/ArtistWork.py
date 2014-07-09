import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect, decimal
import maya.mel as mel
import pymel.core as py
import pymel.core.datatypes as dt
import functools
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ArtistWork.ui'
form_class, base_class = uic.loadUiType(dirUI)

def setPivotLocation():
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
        # get obj's component
        mainObj = cmds.ls(hilite=True)
        cmds.select(mainObj)
        cmds.xform(rp = pivPos, ws= True)

class Pivots(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Artist Work'
        self.scriptjobPivot = cmds.scriptJob(e = ['SelectionChanged',self.clearAll] , protected = True)
        self.btnPivottoCenterElement.clicked.connect(setPivotLocation)
        self.rdbXmin.clicked.connect(self.updatePivotPosition)
        self.rdbXmid.clicked.connect(self.updatePivotPosition)
        self.rdbXmax.clicked.connect(self.updatePivotPosition)
        self.rdbYmin.clicked.connect(self.updatePivotPosition)
        self.rdbYmid.clicked.connect(self.updatePivotPosition)
        self.rdbYmax.clicked.connect(self.updatePivotPosition)
        self.rdbZmin.clicked.connect(self.updatePivotPosition)
        self.rdbZmid.clicked.connect(self.updatePivotPosition)
        self.rdbZmax.clicked.connect(self.updatePivotPosition)
        self.rdbX.clicked.connect(functools.partial(self.pivotOnAxis,'x'))
        self.rdbY.clicked.connect(functools.partial(self.pivotOnAxis,'y'))
        self.rdbZ.clicked.connect(functools.partial(self.pivotOnAxis,'z'))
        self.chkStatus.clicked.connect(self.checkStatus)
        self.edtX.textChanged.connect(self.updateLineEdit)
        self.btnPivottoCenterElement.clicked.connect(setPivotLocation)
        self.btnCenterPivot.clicked.connect(self.qtCenterPivotForSelectedMeshes)
        self.btnPivottoOrigin.clicked.connect(self.qtPivotToOriginForSelectedMeshes)
        self.btnPivottoanotherObj.clicked.connect(self.qtPivotToAnotherObject)
        
    def clearAll(self):
        try:
            selObj = cmds.ls(sl=True,transforms = True)[0]
            bb = cmds.xform(q=True,bb = True)
        
            width = bb[3] - bb[0]
            self.X.setText(str(round(width,2)))
        
            length = bb[4] - bb[1]
            self.Y.setText(str(round(length,2)))
        
            height = bb[5] - bb[2]
            self.Z.setText(str(round(height,2)))
        except IndexError:
            print 'No Problem'
        except RuntimeError:
            pass
        
    def pivots_to_pos(self,obj, Xpos, Ypos, Zpos):
        cmds.xform(cp=True)
        #selObjs = cmds.ls(sl=True)
        bbox = cmds.xform(obj, q=True,bb=True)
        pivot = cmds.xform(obj, q=True,sp=True,ws=True)
        vector  = [0,0,0] 
        vectorX = [0,0,0]
        vectorY = [0,0,0]
        vectorZ = [0,0,0]
        ##
        if Xpos == 'Xmax':
            vectorX = [(bbox[3]-bbox[0])/2,0,0]
        if Xpos == 'Xmin':
            vectorX = [-(bbox[3]-bbox[0])/2,0,0]
        if Xpos == 'Xmid':
            vectorX = [0,0,0]
        ##   
        if Ypos == 'Ymax':
            vectorY = [0,(bbox[4]-bbox[1])/2,0]
        if Ypos == 'Ymin':
            vectorY = [0,-(bbox[4]-bbox[1])/2,0]
        if Ypos == 'Ymid':
            vectorY = [0,0,0]
        ##
        if Zpos == 'Zmax':
            vectorZ = [0,0,(bbox[5]-bbox[2])/2]
        if Zpos == 'Zmin':
            vectorZ = [0,0,-(bbox[5]-bbox[2])/2]
        if Zpos == 'Zmid':
            vectorZ = [0,0,0]
            
        vector[0] = pivot[0] + vectorX[0] + vectorY[0] + vectorZ[0]
        vector[1] = pivot[1] + vectorX[1] + vectorY[1] + vectorZ[1]
        vector[2] = pivot[2] + vectorX[2] + vectorY[2] + vectorZ[2]
        
        cmds.xform(obj, piv = vector,ws=True, a=True)
    
    def updatePivotPosition(self):
        if self.rdbXmin.isChecked():
            Xpos = 'Xmin'
        elif self.rdbXmid.isChecked():
            Xpos = 'Xmid'
        elif self.rdbXmax.isChecked():
            Xpos = 'Xmax'
        else:
            Xpos = ''
            
        if self.rdbYmin.isChecked():
            Ypos = 'Ymin'
        elif self.rdbYmid.isChecked():
            Ypos = 'Ymid'
        elif self.rdbYmax.isChecked():
            Ypos = 'Ymax'
        else:
            Ypos = ''
            
        if self.rdbZmin.isChecked():
            Zpos = 'Zmin'
        elif self.rdbZmid.isChecked():
            Zpos = 'Zmid'
        elif self.rdbZmax.isChecked():
            Zpos = 'Zmax'
        else:
            Zpos = ''
        selObjs = cmds.ls(sl=True)    
        self.pivots_to_pos(selObjs[0], Xpos,Ypos,Zpos)
        
    def alignPivottoFace(self, mesh, face):
        if len(face) > 0:
            return False
        elif len(face) == 0:
            return False
        else:
            vertexes = cmds.polyListComponentConversion(face , ff = True, tv = True)
            pointA = vertexes[0]
            pointB = vertexes[1]
            pointC = vertexes[2]
            vectorAB = dt.Vector(pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2])
            vectorAC = dt.Vector(pointC[0] - pointA[0], pointC[1] - pointA[1], pointC[2] - pointA[2])
            normal = vectorAB.cross(vectorAC)
            x0 = normal.dot([1,0,0])*180/dt.pi
            y0 = normal.dot([0,1,0])*180/dt.pi
            z0 = normal.dot([0,0,1])*180/dt.pi
            
        cmds.xfom(mesh, roo = 'yzx', rp = [x0, y0,z0], ws = True)
   
    def qtCenterPivotForSelectedMeshes(self):
            selObj = cmds.ls(sl=True)
            for obj in selObj:
                cmds.select(obj)
                cmds.xform(cp=True)
            
    def qtPivotToOriginForSelectedMeshes(self):
            selObj = cmds.ls(sl=True)
            for obj in selObj:
                cmds.move(0,0,0,obj+'.scalePivot',obj+'.rotatePivot',a=True)
                
    def qtPivotToAnotherObject(self):
        selObj = cmds.ls(sl=True)
        target = cmds.xform(selObj[1],q=True,sp=True,ws=True)
        cmds.xform(selObj[0],piv=target, ws=True)
        
    def pivotOnAxis(self, axis):
        selObj = cmds.ls(sl=True)[0]
        oldPivot = cmds.xform(q=True,sp=True,ws=True)
        if axis == 'x':
            cmds.xform(piv=[0,oldPivot[1],oldPivot[2]],ws=True)
        if axis == 'y':
            cmds.xform(piv=[oldPivot[0],0,oldPivot[2]],ws=True)
        if axis == 'z':
            cmds.xform(piv=[oldPivot[0],oldPivot[1],0],ws=True)
    
    def checkStatus(self):
        if self.chkStatus.isChecked():
            self.edtY.setText(self.edtX.text())
            self.edtZ.setText(self.edtX.text())
            self.lbY.setEnabled(False)
            self.lbZ.setEnabled(False)
            self.edtY.setEnabled(False)
            self.edtZ.setEnabled(False)
        else:
            self.lbY.setEnabled(True)
            self.lbZ.setEnabled(True)
            self.edtY.setEnabled(True)
            self.edtZ.setEnabled(True)
            
    def updateLineEdit(self):
        if self.chkStatus.isChecked():
            self.edtY.setText(self.edtX.text())
            self.edtZ.setText(self.edtX.text())
            
    def scaleMeshes(self):
        mesh = py.ls(sl = True)[0]
        currentScale = mesh.scaleX.get()
        
def main(xmlFile):
    form = Pivots(xmlFile)
    return form 
    
