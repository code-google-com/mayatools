import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Checking and fix MaterialID.'
name = 'checkMaterialIDs'
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
    matNames = loadXML(xmlDir, 'material', 'name')
    matIDs = loadXML(xmlDir, 'material', 'id')
    shaders = [s for s in cmds.ls(material = 'True') if s not in ['particleCloud1', 'lambert1']]
    for s in shaders:
        if 