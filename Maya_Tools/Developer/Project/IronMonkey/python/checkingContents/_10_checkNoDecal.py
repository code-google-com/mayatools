import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Checking No Decal.'
name = 'checkNoDecal'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')


def execute():
    print 'EXECUTING: CHECKING NO DECAL----------------------------------'
    import re
    objectOrror = list()
    #meshes = cmds.ls(type = 'mesh')#.split('|')[0]
    all_transform = [f for f in cmds.listRelatives(cmds.ls('mesh')[0], ad = True,f=True) if cmds.nodeType(f) != 'mesh'] 
    allMesh = [tran for tran in all_transform if re.search('mesh_',tran)]#.split('|')[-1]
    mirror = [tran for tran in allMesh if re.search('_mirrors_',tran)]
    spoiler = [spoil for spoil in allMesh if re.search('_spoiler_',spoil)]
    mir_spoil = list(set(mirror + spoiler))
    listNo_mir_spoil = [tran for tran in allMesh if tran not in mir_spoil]
    print'################# CORRECT MATERIAL MIRRORS AND SPOILER ################################'
    for mes in mir_spoil:
        #print mes
        object=mes
        shapeNode = cmds.listRelatives(mes, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
        #print sgs
        for sg in sgs:
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                if shader == 'paint_shader_nodecal_opaque':
                    print(shader,'Shaders corect assign')
                else:
                    objectOrror.append(object)
                    #print(object,shader,'Error, shaders incorect assign')
    print'################# INCORRECT MATERIAL ################################'    
    for mes in listNo_mir_spoil:
        object=mes.split('|')[-1]
        shapeNode = cmds.listRelatives(mes, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
        #print sgs
        for sg in sgs:
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                if shader == 'paint_shader_nodecal_opaque':
                    objectOrror.append(object)
                    #print(object,'Incorrect material',shader)
                    
    print objectOrror
    objectHide = [obj for obj in allMesh if obj not in objectOrror]
    if len(objectOrror)>0:
        for ob in objectOrror:
            cmds.select(ob)
    if len(objectHide)>0:
        for obj in objectHide:
            cmds.setAttr(obj + '.visibility', 0)
            