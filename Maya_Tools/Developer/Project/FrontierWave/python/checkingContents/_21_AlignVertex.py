
description = 'Align Vertex.'
name = 'AlignVertex'
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as mc
import maya.mel as mel
import math as mh


def execute():
    sel = mc.ls(fl=1,os=1)
    if len(sel) > 2:
        B = mc.pointPosition(sel[0])
        A = mc.pointPosition(sel[-1])
        otherPoint = list(sel)
        otherPoint.remove(sel[0])
        otherPoint.remove(sel[-1])
        #for i in range(1,(len(sel)-1)):
        for point in otherPoint:
            C = mc.pointPosition(point)
            Mab = mh.sqrt(mh.pow(B[0]-A[0],2) + mh.pow(B[1]-A[1],2) + mh.pow(B[2]-A[2],2))
            Mac = mh.sqrt(mh.pow(C[0]-A[0],2) + mh.pow(C[1]-A[1],2) + mh.pow(C[2]-A[2],2))
            Vab = [(B[0]-A[0])/Mab,(B[1]-A[1])/Mab,(B[2]-A[2])/Mab]
            Vac = [(C[0]-A[0])/Mac,(C[1]-A[1])/Mac,(C[2]-A[2])/Mac]
            cosA = Vab[0]*Vac[0]+Vab[1]*Vac[1]+Vab[2]*Vac[2]
            e = Mac*cosA
            E = [A[0]+Vab[0]*e,A[1]+Vab[1]*e,A[2]+Vab[2]*e]
            mc.move(E[0],E[1],E[2],point,ws=1,wd=1)