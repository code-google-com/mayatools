import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Checking Naming Convention'
name = 'checkNaming'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def loadXML(xmlFile, content, proper):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        kitNodes = root.getElementsByTagName(content)
        kit = [x.getAttribute(proper) for x in kitNodes]
        #kit.append([x.getAttribute('shortname') for x in kitNodes])
        return kit

def execute():
    xmlDir = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/IronMonkey_CustomNamingTool.xml'
    print xmlDir
    parts = loadXML(xmlDir,'part','name')
    kits = loadXML(xmlDir,'kit','shortname')
    lods = loadXML(xmlDir,'lod','name')
    
    print 'EXECUTING: FINDING ERROR MESH NAME----------------------------------'
    
    meshes = cmds.ls(type = 'mesh')
    outPut = list()
    errorMesh = list()
    for mesh in meshes:
        result = False
        for p in parts:
            try:
                if re.search(r'(.*)_{part}_(\.*)'.format(part = p), mesh):
                    result = True
                    break
            except:
                pass
        if not result:
            errorMesh.append(cmds.listRelatives(mesh, p = True, type = 'transform')[0])
    outPut += list(set(errorMesh))
    for m in errorMesh:
        print m + ' not match with any preset partname. Please correct it if nothing\'s special'
    print '-----------------------------------------------------------------------------------------'
    errorMesh = [cmds.listRelatives(mesh, p = True, type = 'transform')[0] for mesh in meshes if mesh.find('wrong_shader') != -1]
    outPut += errorMesh
    for m in errorMesh:
        print m + ' has wrong shader. Please find the most correct one and assign to it.'
    print '-----------------------------------------------------------------------------------------'    
    errorMesh = [cmds.listRelatives(mesh, p = True, type = 'transform')[0] for mesh in meshes if cmds.listRelatives(mesh, p = True, type = 'transform')[0].split('_')[-2] not in kits]
    outPut += errorMesh  
    for m in errorMesh:
        print m + ' has wrong kit name. Please correct it or inform to me if you have no idea to fix.' 
    errorMesh = [cmds.listRelatives(mesh, p = True, type = 'transform')[0] for mesh in meshes if cmds.listRelatives(mesh, p = True, type = 'transform')[0].split('_')[-1] not in lods]
    outPut += errorMesh  
    for m in errorMesh:
        print m + ' has wrong lod name. Please correct it or inform to me if you have no idea to fix.' 
         