'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as py
import maya.mel as mel
import pymel.core as pm
import pymel.core.datatypes as dt
from math import *

try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf

def attachMesh():
    # check shader assigned to faces before attaching
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/flattenCombine.mel'
    print attachFileSource
    mel.eval('source \"{f}\";'.format(f = attachFileSource))

def detachMesh():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/detachComponent.mel'
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

def lineIntersect(A, B, C, D):
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
 
def smartCollapsing():          
    print '--execute ---'
    edgeSets = getConnectedEdges()
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
            intersectPoint = lineIntersect(pointA, pointB, pointC, pointD)
            for v in midleVerts:
                pm.move(v, intersectPoint)
        except:
            continue 
        polybase = cmds.ls(hl = True)
        cmds.select(polybase) 
        cmds.polyMergeVertex( d = 0.001)  
        
def snapTool(tolerance):
        #tolerance = str(self.spnTolerance.value())
        attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geSnapVetexTools_M10.mel'
        mel.eval('source \"{f}\";'.format(f = attachFileSource))
        selObjs = list(set([x.split('.')[0] for x in cmds.ls(sl = True)]))
        if len(selObjs) == 1:
            mel.eval('geSnapToObjectItself(\"\{eps}\");'.format(eps = tolerance))
        elif len(selObjs) == 2:
            mel.eval('geSnapToTheOtherObject(\"\{eps}\");'.format(eps = tolerance))
            
def detachByMaterial(node):
    pass

def CleanupMesh():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geNFS14_SpecialFCCOnSelectedMeshes.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    