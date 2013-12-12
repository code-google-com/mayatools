import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as py
import maya.mel as mel
import os, sys, inspect, re
import functools
from xml.dom.minidom import *
import pymel.core as pm
import pymel.core.datatypes as dt
from math import *
import sip

import CommonFunctions as cf

import ExporterandImporter
reload(ExporterandImporter)

import Source.IconResource_rc
reload(Source.IconResource_rc)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/PolyTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def isIdentity(transform):
    return cmds.xform(transform, query=True, matrix=True) == [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

presetNameforLeft = ['_L_','L_','left','LEFT','_FL_','_BL_','_RL_']
presetNameforRight = ['_R_','R_','right','RIGHT','_FR_','_BR_','_RR_']

def rearrangeEdgeList(edgeList, edge_01):
    orderedList = list()
    edge = edge_01
    stop = False
    while not stop:
        vertexes = cmds.polyListComponentConversion(edge, tv = True)
        connEdges_00 = cmds.polyListComponentConversion(vertex[0], te = True)
    
def attachMesh():
        # check shader assigned to faces before attaching
        attachFileSource = fileDirCommmon + '/mel/flattenCombine.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))

def detachMesh():
        attachFileSource = fileDirCommmon + '/mel/detachComponent.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        
def extractMesh():
        desMesh = cmds.ls(sl = True)[0].split('.')[0]
        midMesh = cmds.duplicate(desMesh, n = desMesh + '_duplicated' ,rr = True)[0]
        selectFaces = [x.replace(desMesh,midMesh) for x in cmds.ls(sl = True)]
        cmds.select(cl = True)
        cmds.select(selectFaces)
        mel.eval('InvertSelection')
        cmds.delete()
        cmds.select(midMesh)
        
def mirrorTool(axis, isKeepHistory, isClone, method):
        selObjs = cmds.ls(sl = True)
        for obj in selObjs:
            if axis == 'x':
                matchName = [x for x in presetNameforLeft if re.search(r'(.*)\{pattern}(\.*)'.format(pattern = x), obj)]
                if len(matchName):
                    index = presetNameforLeft.index(matchName[0])
                    newname = obj.replace(matchName[0], presetNameforRight[index])
                else:
                    matchName = [x for x in presetNameforRight if re.search(r'(.*)\{pattern}(\*.)'.format(pattern = x), obj)]
                    if len(matchName):
                        index = presetNameforRight.index(matchName[0])
                        newname = obj.replace(matchName[0], presetNameforLeft[index])
                    
            if isClone == 'Clone':
                if isKeepHistory:
                    try: 
                        dupMesh = cmds.duplicate(n = newname, ic = True)
                    except NameError:
                        dupMesh = cmds.duplicate(n = obj + '_mirrored', ic = True)
                else:
                    try:
                        dupMesh = cmds.duplicate(n = newname, ic = True)
                    except NameError:
                        dupMesh = cmds.duplicate(n = obj + '_mirrored', ic = False)
            elif isClone == 'Instance':
                try:
                    dupMesh = cmds.duplicate(n = newname, ilf = True)
                except NameError:
                    dupMesh = cmds.duplicate(n = obj + '_mirrored', ilf = True)
            else:
                dupMesh = obj
            if method == 'By axis':
                locator = cmds.spaceLocator()
                cmds.parent(dupMesh, locator)
                if axis == 'x':   
                    cmds.setAttr(locator[0] + '.scaleX', -1)
                if axis == 'y':   
                    cmds.setAttr(locator[0] + '.scaleY', -1)
                if axis == 'z':   
                    cmds.setAttr(locator[0] + '.scaleZ', -1)
                cmds.parent(dupMesh,world = True)
                cmds.delete(locator[0])
            elif method == 'By pivot':
                if axis == 'x':   
                    cmds.setAttr(dupMesh[0] + '.scaleX', -1)
                if axis == 'y':   
                    cmds.setAttr(dupMesh[0] + '.scaleY', -1)
                if axis == 'z':   
                    cmds.setAttr(dupMesh[0] + '.scaleZ', -1)
            #mel.eval('FreezeTransformations')
            cmds.makeIdentity(a = True, t = 1, r = 0, s = 1, n = 0)
            mel.eval('DeleteHistory')
            
            cmds.polyNormal(dupMesh, nm = 0, userNormalMode = 0)
            dupMeshShape = cmds.listRelatives(dupMesh, type = 'mesh', fullPath = True)
            cmds.setAttr(dupMeshShape[0] + '.opposite', False)
            cmds.select(cl = True)
            cmds.select(dupMesh)
            
def exportMesh():
        exp = ExporterandImporter.exporterShader()
        exp.exportMaya()
        
def importMesh():
        imp = ExporterandImporter.importerShader()
        imp.importMaya()

def editFlowEdges(edgeList):
    vertexes = cmds.polyListComponentConversion(edgeList, tv = True)
    #conjugateEdges = cmds.polyListComponentConversion(vertexes, te = True)
    #vertexesExpanding = cmds.polyListComponentConversion(conjugateEdges, tv = True)
    # filter 
    for v in vertexes:
        conjugateEdges = cmds.polyListComponentConversion(v, te = True)
        conjugateVertexes = cmds.polyListComponentConversion(conjugateEdges, te = True)
        filteredVertexes = [v for v in conjugateVertexes if v not in vertexes]
        interpolatePosition(v, filteredVertexes)
            
class PolyTools(form_class,base_class):
    closeTransferTool = QtCore.pyqtSignal('QString', name = 'closeTransferTool')
    def __init__(self, inputFile, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.__name__ = 'Poly tools'
        self._ring = 0
        self._loop = 0
        
        self.btnExport.clicked.connect(exportMesh)
        self.btnImport.clicked.connect(importMesh)
        self.btnSetupAxis.clicked.connect(self.changeAxis)
        self.btnSetNormalSize.clicked.connect(self.changeNormalSize)
        self.btnSetupBackground.clicked.connect(self.changColorBackGround)
        
        # -- POLY MODELING TOOL
        self.btnAttach.clicked.connect(attachMesh)
        self.btnDetach.clicked.connect(detachMesh)
        self.btnDuplicate.clicked.connect(extractMesh)
        self.btnLoopEdges.clicked.connect(self.LoopEdges)
        self.btnRingEdges.clicked.connect(self.RingEdges)
        self.btnSmartCollapse.clicked.connect(self.smartCollapsing)
        self.btnSnapVertexTool.clicked.connect(self.snapTool)
        # -- LOCK NORMAL TOOLBOX
        self.btnLockToLargeFace.clicked.connect(self.lockNormalToLargeFace)
        self.btnLockToSmallFace.clicked.connect(self.lockNormalToSmallFace)
        self.btnCopyNormal.clicked.connect(self.copyNormal)
        self.btnCopyAverageNormal.clicked.connect(self.copyAverageNormal)
        self.btnPasteNormal.clicked.connect(self.pasteNormal)
        self.btnSmoothBevel.clicked.connect(self.smoothBevelNormal)
        self.btnmatchSeamNormal.clicked.connect(self.matchseamNormal)
        self.btnUnlock.clicked.connect(self.lockUnLocked)
        self.btnSmoothAdjacentEdges.clicked.connect(self.smoothBorderEdges)
        self.btnTransferNormalWithoutDetachMesh.clicked.connect(self.transferNormalWithoutDetachMesh)
        self.btnMirrorTools.clicked.connect(self.mirrorNormalTool)
        # -- MIRROR TOOL
                              
        self.btnAxisX.clicked.connect(functools.partial(self.mirror,'x', 'By axis'))
        self.btnAxisY.clicked.connect(functools.partial(self.mirror,'y', 'By axis'))
        self.btnAxisZ.clicked.connect(functools.partial(self.mirror,'z', 'By axis'))
                                                                                                               
        self.btnPivotX.clicked.connect(functools.partial(self.mirror,'x', 'By pivot'))
        self.btnPivotY.clicked.connect(functools.partial(self.mirror,'y', 'By pivot'))
        self.btnPivotZ.clicked.connect(functools.partial(self.mirror,'z', 'By pivot'))  
        
        self.btnMirrorU.clicked.connect(self.updateTextMirrorTool)
        self.btnMirrorV.clicked.connect(self.updateTextMirrorTool)
                                                                                               
        self.startUp()
        
    def startUp(self):
        up = cmds.upAxis(q = True, ax = True)
        if up == 'y':
            self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Y_up.png'))
        else:
            self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Z_up.png'))
            
        self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_off.png'))
            
    def returnAngleBetweenVectors(vector1, vector2):
        cos0 = vector1.dot(vector2)/(vector1.length()*vector2.length())
        angle = dt.degrees(dt.acos(cos0))
        print angle
        return angle
    
    def RingEdges(self):
        #print N
        mel.eval('polySelectEdgesEveryN "edgeRing" \"{num}\";'.format(num = str(self.spnRing.value() + 1)))
        
    def LoopEdges(self):
        #print N
        mel.eval('polySelectEdgesEveryN "edgeLoop" \"{num}\";'.format(num = str(self.spnLoop.value() + 1)))
    
    def rotateVectorToZAxis(self, vector):
        vectorLength = sqrt(pow(vector.x,2) + pow(vector.z,2))
        y_Rot = degrees(acos(vector.z/vectorLength))
        x_Rot = degrees(acos(vectorLength/vector.length()))
        return (x_Rot, -y_Rot)
            
    def changColorBackGround(self):
        if cmds.displayPref(q=True, displayGradient=True) == False: 
            cmds.displayRGBColor( 'background', 0.5, 0.5, 0.5 )
            cmds.displayPref(displayGradient=True)
        else:
            cmds.displayRGBColor( 'background', 1, 0, 1 )
            cmds.displayPref(displayGradient=False)
    
    def changeAxis(self):
        up = cmds.upAxis(q = True, ax = True)
        if up == 'y':
            cmds.upAxis(ax = 'z')
            self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Z_up.png'))
        else:
            cmds.upAxis(ax = 'y')
            self.btnSetupAxis.setIcon(QtGui.QIcon(':/Project/Y_up.png'))
            
    def changeNormalSize(self):
        # get normal size of selected meshes
        selObjs = cmds.ls(sl = True)
        if len(selObjs) == 0:
            cmds.error('Please select one mesh')
        normalDisplay = cmds.polyOptions(selObjs[0], q = True, dn = True)
        if not normalDisplay[0]:
            self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_small.png'))
            cmds.polyOptions(gl = True, dn = True, pt = True, sn = 0.1 )
        else:
            sizeNormal = cmds.polyOptions(selObjs[0], q = True, sn = True)
            if sizeNormal[0] == 0.1:
                self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_large.png'))
                cmds.polyOptions(gl = True, dn = True, pt = True, sn = 1)
            elif sizeNormal[0] == 1:
                self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_off.png'))
                cmds.polyOptions(gl = True, dn = False)
            elif sizeNormal[0] not in [0.1,1]:
                self.btnSetNormalSize.setIcon(QtGui.QIcon(':/Project/normal_small.png'))
                cmds.polyOptions(gl = True, dn = True, pt = True, sn = 0.1)
    
    def lineIntersect(self,A, B, C, D):
        a = B - A
        b = D - C
        c = C - A
        cross1 = a.cross(b)
        cross2 = c.cross(b)
        intersectPoint = A + a* cross2.dot(cross1)/math.pow(cross1.length(),2)
        return intersectPoint
        
    def getConnectedEdges(self):
        #if not cmds.selectType(q = True, e = True):   
        selectedEdges = cmds.ls(sl = True, fl = True)
        unconnectedSelectedEdges = list()
        #currentEdge = selectedEdges[0]
        while len(selectedEdges) > 0:
            unconnectedSelectedEdges.append(list())
            unconnectedSelectedEdges[len(unconnectedSelectedEdges) - 1].append(selectedEdges[0])
            selectedEdges.remove(selectedEdges[0])
            i = 0
            while i < len(unconnectedSelectedEdges[len(unconnectedSelectedEdges) - 1]):
                i += 1
                verts = cmds.polyListComponentConversion(unconnectedSelectedEdges[len(unconnectedSelectedEdges) - 1], tv = True)
                neigborEdges = cmds.polyListComponentConversion(verts, te = True)
                cmds.select(neigborEdges)
                neigborEdges = cmds.ls(sl= True, fl = True)
                for e in neigborEdges:
                    if e in selectedEdges:
                        selectedEdges.remove(e)
                        unconnectedSelectedEdges[len(unconnectedSelectedEdges) - 1].append(e)
        return unconnectedSelectedEdges    
        
    def smartCollapsing(self):
        print str(self.spnRing.value())
        print str(self.spnLoop.value())
        
        print '--execute ---'
        edgeSets = self.getConnectedEdges()
        for set in edgeSets:
            try:
                verts = list()
                endVerts = list()
                midleVerts = list()
                for e in set:
                    for vertStr in cmds.polyListComponentConversion(e, tv = True):
                        cmds.select(vertStr)
                        for v in cmds.ls(sl = True, fl = True):
                            verts.append(v)
                            # filter verts to separate endverts and midle
            
                for v in verts:
                    if verts.count(v) > 1:
                        midleVerts.append(v)
                    else:
                        endVerts.append(v)
                            
                # get end edges
                edges = cmds.polyListComponentConversion(endVerts, te = True)
                execEdges = list()
                cmds.select(edges)
                for e in cmds.ls(sl = True, fl = True):
                    if e in set:
                        execEdges.append(e)
                cmds.select(execEdges)
                # there are only two edges at the end
                # get two point on the first edges
                vertSet = cmds.polyListComponentConversion(execEdges[0], tv = True)
                cmds.select(vertSet)
                vertSet = cmds.ls(sl = True, fl = True)
                pointA = pm.pointPosition(vertSet[0])
                pointB = pm.pointPosition(vertSet[1])
                # get two point on the second edges
                vertSet = cmds.polyListComponentConversion(execEdges[1], tv = True)
                cmds.select(vertSet)
                vertSet = cmds.ls(sl = True, fl = True)
                pointC = pm.pointPosition(vertSet[0])
                pointD = pm.pointPosition(vertSet[1])
                # get the intersect Point base on 4 point
                intersectPoint = self.lineIntersect(pointA, pointB, pointC, pointD)
                for v in midleVerts:
                    pm.move(v, intersectPoint)
            except:
                continue 
        polybase = cmds.ls(hl = True)
        cmds.select(polybase) 
        cmds.polyMergeVertex( d = 0.001)  
        
    def rotateObject(self):
        cmds.selectType(fc = True)
        if cmds.selectType(q = True, fc = True):
            meshBase = cmds.ls(hl = True)[0]
            if isIdentity(meshBase):
                transformNode = py.PyNode(meshBase)
                shapeNode = transformNode.getShape()
                selFaces = cmds.ls(sl = True, fl = True)
                vectorN = dt.Vector(0,0,0)
                for face in selFaces:
                    id = int(face.split('.')[1].replace('f[','').replace(']',''))
                    vectorI = shapeNode.getPolygonNormal(id)
                    vectorN += vectorI
                vectorN = vectorN/(len(selFaces))
                #print vectorN 
                (rotX, rotY) = self.rotateVectorToZAxis(vectorN)
                # select mesh base object
                cmds.select(meshBase)
                mel.eval('FreezeTransformations')
                cmds.rotate(0, rotY, 0, meshBase, ws = True)
                mel.eval('FreezeTransformations')
                cmds.rotate(rotX , 0, 0, meshBase, a = True)
                mel.eval('FreezeTransformations')
                mel.eval('DeleteHistory')
            else:
                print 'chua Freeze Transform'
        
    def lockNormalToLargeFace(self):
        attachFileSource = fileDirCommmon + '/mel/boltNormalToolbox.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('$s=`ls -sl`; boltNorms.EdgeToVF(1); boltNorms.LockSelectedVFs(0); select $s')
        # set locked norml edges to softedge
        cmds.polySoftEdge( a= 180, ch = False)
        
    def lockNormalToSmallFace(self):
        attachFileSource = fileDirCommmon + '/mel/boltNormalToolbox.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('$s=`ls -sl`; boltNorms.EdgeToVF(0); boltNorms.LockSelectedVFs(0); select $s')
        cmds.polySoftEdge( a= 180, ch = False)
        
    def copyNormal(self):
        attachFileSource = fileDirCommmon + '/mel/geNFS14_NFS13NormalTools_UI.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('CG_copyVertexNormal()')
        
    def copyAverageNormal(self):
        attachFileSource = fileDirCommmon + '/mel/geNFS14_NFS13NormalTools_UI.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('CG_copyAverageVertexNormal()')
        
    def pasteNormal(self):
        attachFileSource = fileDirCommmon + '/mel/geNFS14_NFS13NormalTools_UI.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('CG_pasteVertexNormals(\"x\")')
        
    def smoothBevelNormal(self):
        attachFileSource = fileDirCommmon + '/mel/boltNormalToolbox.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('boltNorms.SmoothBevel(0)') 
        
    def lockUnLocked(self):
        #mel.eval('polyNormalPerVertex -ufn true;')
        selObject = cmds.ls(sl = True)[0]
        vertNum = cmds.polyEvaluate(v=True)
        for i in range(vertNum):
            if not cmds.polyNormalPerVertex(selObject + '.vtx[' + str(i) + ']', q= True, ufn = True):
                 cmds.polyNormalPerVertex(selObject + '.vtx[' + str(i) + ']', fn = True)
    
    def matchseamNormal(self):
        attachFileSource = fileDirCommmon + '/mel/boltNormalToolbox.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('boltNorms.MatchSeamNormals()') 
        
    def smoothBorderEdges(self):
        tolerance = str(self.spnSmoothEdges.value())
        attachFileSource = fileDirCommmon + '/mel/geSetNormalVertexTool.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        selObjs = list(set([x.split('.')[0] for x in cmds.ls(sl = True)]))
        if len(selObjs) == 1:
            mel.eval('geSnapToObjectItself(\"\{eps}\");'.format(eps = tolerance))
        elif len(selObjs) == 2:
            mel.eval('geSnapToTheOtherObject(\"\{eps}\",\"\{para}\");'.format(eps = tolerance,para = 3))
            
    def snapTool(self):
        tolerance = str(self.spnTolerance.value())
        attachFileSource = fileDirCommmon + '/mel/geSnapVetexTools_M10.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        selObjs = list(set([x.split('.')[0] for x in cmds.ls(sl = True)]))
        if len(selObjs) == 1:
            mel.eval('geSnapToObjectItself(\"\{eps}\");'.format(eps = tolerance))
        elif len(selObjs) == 2:
            mel.eval('geSnapToTheOtherObject(\"\{eps}\");'.format(eps = tolerance))
            
    def mirrorNormalTool(self):
        attachFileSource = fileDirCommmon + '/mel/boltNormalToolbox.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('boltNorms.MirrorGUI(0.0005)')
                    
    def mirror(self, axis, method):
        isKeepHistory = True
        isClone = ''
        if self.rdbKeepHistory.isChecked():
            isKeepHistory = True
        else: 
            isKeepHistory = False
        if self.rdbNoClone.isChecked():
            isClone = 'No Clone'
        elif self.rdbClone.isChecked():
            isClone = 'Clone'
        elif self.rdbInstance.isChecked():
            isClone = 'Instance'
        mirrorTool(axis, isKeepHistory, isClone, method)
        
    def transferNormalWithoutDetachMesh(self):
        selObjs = cmds.ls(sl = True)
        transferedFaces = [x for x in selObjs if re.search(r'(.*).f\[(\.*)',x,re.I)]
        
        srcMesh = [x for x in selObjs if not re.search(r'(.*).f\[(\.*)',x,re.I)][0]
        desMesh = list(set([x.split('.')[0] for x in transferedFaces ]))[0]
        
        #-- Duplicate mesh
        midMesh = cmds.duplicate(desMesh, n = desMesh + '_proxy' ,rr = True)
        selectFaces = [midMesh[0] + '.' + x.split('.')[1] for x in transferedFaces]
        cmds.select(cl = True)
        cmds.select(selectFaces)
        mel.eval('InvertSelection')
        cmds.delete()
        
        #-- Transfer Normal Tool
        cmds.transferAttributes(srcMesh, midMesh, nml = True)
        cmds.select(midMesh)
        mel.eval('DeleteHistory')
        
        #-- Copy normal from proxy to des
        vertexnums = cmds.polyEvaluate(v = True) - 1
        cmds.select(midMesh[0] + '.vtx[0:' + str(vertexnums) + ']')
        cmds.select(desMesh, add = True)
        attachFileSource = fileDirCommmon + '/mel/geSetNormalVertexTool.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        mel.eval('geSnapToTheOtherObject(\"\{eps}\", \"\{para}\");'.format(eps = 0.01, para = 1))
        cmds.delete(midMesh)
        
    def updateTextMirrorTool(self):
        if self.btnMirrorU.isChecked():
            self.btnMirrorU.setText('Mirror U')
        else:
            self.btnMirrorU.setText('X')
        if self.btnMirrorV.isChecked():
            self.btnMirrorV.setText('Mirror V')
        else:
            self.btnMirrorV.setText('Z')
    
                  
def main(xmlnput):
    form = PolyTools(xmlnput)
    return form 



    
