import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import xml.dom.minidom as xml
import os,inspect

root = 'M:\\'
xmlDir = root + 'xmlMeshInfo.xml'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
storedDataFile = root + 'storedMaya.mb' # temp file contains imported mesh
xmlPairFile = root + 'xmlPairFile.xml'

def exportToFBX(fileDir):  
    #mel.eval('FBXExportSmoothingGroups -v true')
    #mel.eval('FBXExportUpAxis z')
    #mel.eval('FBXExportScaleFactor 1.0')
    #mel.eval('FBXExport -f \"{f}\" -s'.format(f = fileDir))
    py.exportSelected(fileDir, shader = False, type= 'mayaBinary')

def writeXML(xmlDoc, location):
    #print xmlDoc.toprettyxml()
    openStream = open(location, 'w')
    openStream.write(xmlDoc.toprettyxml())
    openStream.close()
    
def cleanPerFaceAssigment():
    cmds.loadPlugin('cleanPerFaceAssignment', qt = 1)
    mel.eval('cleanPerFaceAssignment;')
    #transfromNode = cmds.ls()
    
def getShaderFromNodes(node):
    try:
        shape = cmds.listRelatives(node, shapes = True)[0]
        #print 'listRelatives'
    except:
        shape = cmds.pickWalk(node, d = 'down')[0]
        #print 'pickWwalk'
    shadingGroups = list(set(py.listConnections(shape, type = 'shadingEngine')))
    if len(shadingGroups) == 0: # neu object khong co shader duoc gan thi khong can luu thong tin
        return False
    else:
        shadersList = []
        for shading in shadingGroups:
            if cmds.connectionInfo(shading + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(shading + '.surfaceShader', sfd = True).split('.')[0]
                shadersList.append(shader)
        return shadersList

def getUVFromNode(node):
    UVSets = py.polyUVSet(node, q= True, auv = True)
    return UVSets

def getAssetFromList(nodes):
        masterList = []
        #nodes = cmds.ls(g = True)
        shapes = []
        for node in nodes:
            #print node
            element = list()
            shaders = getShaderFromNodes(node)
            #print shaders
            if shaders:
                element.append(node)
                element.append(shaders)
                element.append(getUVFromNode(node))
                masterList.append(element)
        return masterList
        
def makingXMLFromMasterList(masterList):
        filename = cmds.file(q= True, sn = True)
        xmlDoc = xml.Document()
        rootNode = xmlDoc.createElement('root')
        rootNode.setAttribute('file',filename)
        xmlDoc.appendChild(rootNode)
        for index in range(len(masterList)):
            shapeNode = xmlDoc.createElement('mesh')
            shapeNode.setAttribute('name', masterList[index][0])
            rootNode.appendChild(shapeNode)
            shaderNode = xmlDoc.createElement('shader')
            shapeNode.appendChild(shaderNode)
            UVNode = xmlDoc.createElement('UV')
            shapeNode.appendChild(UVNode)
            # get shader from shape
            for shader in masterList[index][1]:
                shaderItemNode = xmlDoc.createElement('shaderItem')
                shaderItemNode.setAttribute('name',shader)
                shaderNode.appendChild(shaderItemNode)
            # get UvSet from shape
            #uvSets = py.polyUVSet(masterList[index][0], q= True, auv = True)
            for uv in masterList[index][2]:
                uvSetItemNode = xmlDoc.createElement('uvSetItem')
                uvSetItemNode.setAttribute('name', uv)
                UVNode.appendChild(uvSetItemNode)
        writeXML(xmlDoc,xmlDir)
        
def loadXMLDataInfoMesh(XMLfile):
    masterList = []
    xmlDoc = xml.parse(XMLfile)
    shapeNodes = xmlDoc.getElementsByTagName('mesh')
    for node in shapeNodes:
        element = []
        nameNode = node.getAttribute('name')
        element.append(nameNode)
        shaderNodes = node.getElementsByTagName('shaderItem')
        shaderList = []
        for shader in shaderNodes:
            nameShader = shader.getAttribute('name')
            shaderList.append(nameShader)
        element.append(shaderList)
        uvNodes = node.getElementsByTagName('uvSetItem')
        UVList = []
        for uv in uvNodes:
            nameUVSet = uv.getAttribute('name')
            UVList.append(nameUVSet) 
        element.append(UVList)
        masterList.append(element)
    return masterList

def getFaceFromSelectedShaderAndSelectedMesh(shader, mesh):
    # get shading group from shader
    try:
        shape = cmds.listRelatives(mesh, shapes = True)[0]
    except ValueError:
        return
    shadingGroups = py.listConnections(shader, type = 'shadingEngine')
    #print shadingGroups
    faceList = py.sets(shadingGroups, q = True)
    #print faceList
    selectedFaces = []
    for f in faceList:
        shapefromFace = f.split('.')[0]
        if shapefromFace == shape:
            selectedFaces.append(f)
    #print selectedFaces
    if shape not in selectedFaces:
        cmds.select(selectedFaces)
        if len(cmds.ls(sl = True, fl = True)) == cmds.polyEvaluate(mesh, f = True):# in case selected faces is equal to the number of  faces
            cmds.select(mesh)
        else:
            attachFileSource = fileDirCommmon + '/detachComponent.mel'
            mel.eval('source \"{f}\";'.format(f = attachFileSource))
    else: # object has only one material
        #print 'select: ' + mesh
        cmds.select(mesh)
        
def loadXMLExtractMeshData():
    xmlDoc = xml.parse(xmlPairFile)
    mayaFile = xmlDoc.getElementsByTagName('root')[0].getAttribute('name')
    if os.path.exists(mayaFile):
        cmds.file(new = 1, f = 1)
        cmds.file(mayaFile, f = 1, o = 1 )
        # if file open succeed
        # get pair of tranfer Meshes
        pairNodes = xmlDoc.getElementsByTagName('pair')
        for pair in pairNodes:
            mesh = pair.getElementsByTagName('meshFile')[0].getAttribute('name')
            print mesh
            shader = pair.getElementsByTagName('meshFile')[0].getAttribute('shader')
            print shader
            getFaceFromSelectedShaderAndSelectedMesh(shader, mesh)
            newname = mesh + '__' + shader + '_source_unwrapped'
            cmds.rename(newname)
        filterMesh = cmds.ls('*source_unwrapped*')
        cmds.select(filterMesh)
        exportToFBX(storedDataFile)

def getAssetBatchMode(execFile):
    if os.path.exists(execFile):
        cmds.file(new = 1, f = 1)
        cmds.file(execFile, f= 1, o =1)
        nodes = cmds.ls(transforms = True)
        masterList = getAssetFromList(nodes)
        makingXMLFromMasterList(masterList)