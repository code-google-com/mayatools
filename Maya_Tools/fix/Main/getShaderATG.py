import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os.path

shaderPath = 'M:/assets/noodle/Materials/Library/Vehicles_DC/'

def findXMLFileInDir(XMLFile):
    for (root, dirs, files) in os.walk(shaderPath):
        if XMLFile in files:
            return (root + '/' + XMLFile)
    return (root + '/' + XMLFile)

def convertXMLFileToIconFile(xmlFile, res):
    if os.path.isfile(xmlFile):
        return xmlFile.replace('.xml','_swatch_' + str(res) + '.bmp')
    else:
        return 'G:/MayaToolSystem/Developer/Main/Source/maya_swatch.bmp'
    
def getATGMaterialXMLFileByNode(node):
    ATGMaterial = []
    cmds.hyperShade(node, smn = True)
    shaderGroup = cmds.ls(sl = True)
    for shader in shaderGroup:
        if cmds.nodeType(shader) == 'ATGMaterial':
            path = cmds.getAttr(shader + '.RawPath')
        else:
            path = 'Undefined'    
        ATGMaterial.append(path)
    #for shader in shaderGroup:
        #xmlFile = findXMLFileInDir(shader + '.xml')
        #ATGMaterial.append(xmlFile)
    return ATGMaterial
    
def dataShaderFromNode(node):
    XMLFileList = getATGMaterialXMLFileByNode(node)
    iconList = []
    nameList = []
    for xml in XMLFileList:
        iconFile = convertXMLFileToIconFile(xml, 128)
        iconList.append(iconFile)
        shaderName = os.path.split(os.path.splitext(xml)[0])[1]
        nameList.append(shaderName)
    return (iconList, nameList)
        
     