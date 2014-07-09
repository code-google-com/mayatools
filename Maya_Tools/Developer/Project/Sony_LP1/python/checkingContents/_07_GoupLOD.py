
description = 'Group LODs.'
name = 'groupLod.'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py

import geNFS14_CleanUpFunctions
reload(geNFS14_CleanUpFunctions)

def execute():
    listTris =list()
    ListObject = list()
    listMesh = list()
    nameGroup= ''
    print '--------------- CHECK MATERIAL NAME WRONG-------------------------'
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    MayaFile = fileName.split('/')[-1]
    groupNameSplit = MayaFile.split('_',2)
    Name= groupNameSplit[1] 
    print Name
    print('Maya Name: ',MayaFile)
    
    print '____Clean truoc khi  group____'    
    geNFS14_CleanUpFunctions.DeleteIsolatedMeshes()
    geNFS14_CleanUpFunctions.DeleteIsolatedIntermediateNodes()
    geNFS14_CleanUpFunctions.DeleteReferenceNodes()
    
    #objects = cmds.ls(geometry= True)
    objects = cmds.ls(type = 'transform')
    listTemp = [me for me in objects if me not in ['front','persp','side','top']]
    print('Object: ',objects)
    print('List Temp: ',listTemp)
    '''
    for ob in objects:
        #print('Danh sach Object: ',ob)
        #print('Relative: ',cmds.listRelatives(ob,p=True))
        print('Ob: ',ob)
        ListObject.append(cmds.listRelatives(ob,p=True))
        #ListObject.append(ob)
    '''
    if listTemp !='':
        #cmds.select(cl = True)
        for li in listTemp:
            listTris.append(cmds.polyEvaluate(li,t=True))
            #print('Trig:',cmds.polyEvaluate(li,t=True))
            #cmds.select(li,add =True)
            #print cmds.ls(li,type = 'transform')
        maxTris = max(listTris)
        minTris = min(listTris)
        listMin = [mid for mid in listTris if mid not in [minTris,maxTris]]
        #print('ListObject:',ListObject)
        for i in range(0,len(listTemp)):
            print('gia tri 1',i)
            if cmds.polyEvaluate(listTemp[i],t=True) == maxTris:
                listMesh.append(cmds.rename(listTemp[i],MayaFile + '_LOD0'))
                
            elif cmds.polyEvaluate(listTemp[i],t=True) == minTris:
                #cmds.rename(obj,MayaFile + '_LOD3')
                listMesh.append(cmds.rename(listTemp[i],MayaFile + '_LOD2'))
                
                #print("obj", ListObject[i])
            else:
                #cmds.rename(obj,MayaFile + '_LOD2') 
                listMesh.append(cmds.rename(listTemp[i],MayaFile + '_LOD1'))               
                #print maxTris
    if listMesh !='':
        for mesh in listMesh:
            cmds.select(mesh,add =True)
        mel.eval('LevelOfDetailGroup;')
        lod = cmds.ls(type = 'lodGroup')
        nameGroup = cmds.rename(lod,'lod_'+Name)
    
    cmds.setAttr(nameGroup + '.threshold[0]',10)
    cmds.setAttr(nameGroup+'.threshold[1]',20)
    
        
    #print ('Lod:',lod)
    