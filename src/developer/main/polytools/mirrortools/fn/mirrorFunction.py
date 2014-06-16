'''
Created on May 31, 2014

@author: quoctrung
'''

#-- import dependencies

import re

import maya.cmds as cmds
import maya.mel as mel


#import pymel.core as py
#import pymel.core.datatypes as dt
#--
presetNameforLeft = ['_L_','L_','left','LEFT','_FL_','_BL_','_RL_']
presetNameforRight = ['_R_','R_','right','RIGHT','_FR_','_BR_','_RR_']

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
                dupMesh = [obj]
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
