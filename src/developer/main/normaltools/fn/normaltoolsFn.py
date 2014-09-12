'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMaya as om
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as py
import maya.mel as mel
import os, sys, inspect, re
import pymel.core as pm
import pymel.core.datatypes as dt
from math import *

try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf


#fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
def lockNormalToLargeFace():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/boltNormalToolbox.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('$s=`ls -sl`; boltNorms.EdgeToVF(1); boltNorms.LockSelectedVFs(0); select $s')
    # set locked norml edges to softedge
    cmds.polySoftEdge( a= 180, ch = False)

def lockNormalToSmallFace():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/boltNormalToolbox.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('$s=`ls -sl`; boltNorms.EdgeToVF(0); boltNorms.LockSelectedVFs(0); select $s')
    cmds.polySoftEdge( a= 180, ch = False)

def copyNormal():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geNFS14_NFS13NormalTools_UI.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('CG_copyVertexNormal()')

def copyAverageNormal():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geNFS14_NFS13NormalTools_UI.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('CG_copyAverageVertexNormal()')

def pasteNormal():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geNFS14_NFS13NormalTools_UI.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('CG_pasteVertexNormals(\"x\")')

def smoothBevelNormal():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/boltNormalToolbox.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('boltNorms.SmoothBevel(0)')

def matchseamNormal():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/boltNormalToolbox.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('boltNorms.MatchSeamNormals()') 

def lockUnLocked():
    #mel.eval('polyNormalPerVertex -ufn true;')
    selObject = cmds.ls(sl = True)[0]
    vertNum = cmds.polyEvaluate(v=True)
    for i in range(vertNum):
        if not cmds.polyNormalPerVertex(selObject + '.vtx[' + str(i) + ']', q= True, ufn = True):
            cmds.polyNormalPerVertex(selObject + '.vtx[' + str(i) + ']', fn = True)

def smoothBorderEdges(tolerance):
    #tolerance = str(self.spnSmoothEdges.value())
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geSetNormalVertexTool.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    selObjs = list(set([x.split('.')[0] for x in cmds.ls(sl = True)]))
    if len(selObjs) == 1:
        mel.eval('geSnapToObjectItself(\"\{eps}\");'.format(eps = tolerance))
    elif len(selObjs) == 2:
        mel.eval('geSnapToTheOtherObject(\"\{eps}\",\"\{para}\");'.format(eps = tolerance,para = 3))

def transferNormalWithoutDetachMesh():
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
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/geSetNormalVertexTool.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('geSnapToTheOtherObject(\"\{eps}\", \"\{para}\");'.format(eps = 0.01, para = 1))
    cmds.delete(midMesh)

def mirrorNormalTool():
    attachFileSource = cf.getPath(__file__, 2).replace('\\','/') + '/mel/boltNormalToolbox.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('boltNorms.MirrorGUI(0.0005)')