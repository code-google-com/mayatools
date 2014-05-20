import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Reset Joint to Zero.'
name = 'resetJoint'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')


def execute():
    print 'EXECUTING: RESET JOINT----------------------------------'
    selJointList = cmds.ls(sl=True,dag=True,type='joint')
    for j in selJointList:
        nameList=[]
        nameTemp = []
        childList = cmds.listRelatives(j, children=True,f=True)
        print 'danh sach con'
        #add name before rename
        for chil in childList:
            nameList.append(chil.split('|')[-1])
        # rename before unparent
        for tm in childList:
            tp = cmds.rename(tm,tm+'temp')
            nameTemp.append(tp)
        # Unparent and reset to zero
        childList1 = cmds.listRelatives(j, children=True)
        print childList1
        cmds.parent(childList1,w=True)
        for attr in [".jointOrientX", ".jointOrientY", ".jointOrientZ"]:
            cmds.setAttr(j+attr, 0)
        # Parent Againt
        cmds.parent(childList1,j)
        # Restore name before
        childList3 = cmds.listRelatives(j, children=True)
        print childList3
        for n in range(0,len(childList3)):
            name = nameList[n]
            cmds.rename(childList3[n],name)