'''
Created on Sep 10, 2014

@author: Trung
'''
import maya.mel as mel
import maya.cmds as cmds
from PyQt4 import QtGui

def LoopEdges(spnLoop):
    #print N
    mel.eval('polySelectEdgesEveryN "edgeLoop" \"{num}\";'.format(num = str(spnLoop + 1)))

def RingEdges(spnRing):
    #print N
    mel.eval('polySelectEdgesEveryN "edgeRing" \"{num}\";'.format(num = str(spnRing + 1))) #self.spnRing.value()
    
def selectEdgesOption(input):
    edgeList = list()
    mesh = cmds.ls(sl = True)[0]
    edges = cmds.polyEvaluate(mesh, e = True)
    if input == 1:
        for e in range(edges):
            edgeInfo = cmds.polyInfo(mesh + '.e[' + str(e) + ']', ev = True)
            if 'Hard' in edgeInfo[0]:
                edgeList.append(mesh + '.e[' + str(e) + ']')
    else:
        for e in range(edges):
            edgeInfo = cmds.polyInfo(mesh + '.e[' + str(e) + ']', ev = True)
            if 'Hard' not in edgeInfo[0]:
                edgeList.append(mesh + '.e[' + str(e) + ']')
        
    if len(edgeList) == 0:
        if input == 1:
            QtGui.QMessageBox.information(None, 'Messages', 'Khong tim thay HardEdges', QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.information(None, 'Messages', 'Khong tim thay SoftEdges', QtGui.QMessageBox.Ok)
        return
    cmds.select(edgeList)
    
