##------------------ Export Material ------------------------###-- Author: Tran Quoc Trung #-- Company: GlassEgg Digital Media#-- Date: 8-10-2012#-- Description:#    Export FBX and Material XML to store assigned shaders to each object then importing 3dsMax will read this file to recover # material by assign approriate ID and apply multi-sub Material.#    Also, Export FBX from 3dsMax will create XML file to store material info to recover when import to Mayaimport maya.cmds as cmdsimport maya.mel as melfrom xml.dom.minidom import *import os, sysfrom PyQt4 import QtGui, QtCoreimport CommonFunctions as cf#sys.path.append('M:/tools/maya/Python/Maya2010/Python26/Lib/site-packages/win32/lib')#sys.path.append('M:/tools/maya/Python/Maya2010/Python26/Lib/site-packages/win32/')import ctypes# not working in maya 2013.5 because maya 2013.5 was re compiled under VS 2010#import win32clipboard as wc#import win32condef filterShaderNodes(inList):    out = list()    currentNode = ''    for item in inList:        try: # each object assigned more than 1 shader            node = item.split('.')[0]            value = int(item.split('.')[1].rstrip(']').lstrip('f['))            if node == currentNode:                out[len(out)-1].append(value)            else:                lst = list()                node = item.split('.')[0]                value = int(item.split('.')[1].rstrip(']').lstrip('f['))                lst.append(node)                lst.append(value)                out.append(lst)                currentNode = node        except IndexError: # object just assigned one shader            print (item + " need assign one more shader to proceed")            numFace = cmds.polyEvaluate(item, f= True)            lst = list()            lst.append(node)            for i in range(numFace):                lst.append(i)            out.append(lst)    return outdef selectFromString(inList):    out = []    faces = inList[1].split(',')    for i in faces:        out.append(inList[0] + '.f[' + i + ']')    return out            class exporterShader():    def __init__(self):        self._shaderDAGNodes = list()    def writeXML(self):        fbxFile = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.fbx'        #backupShaderFile = os.path.splitext(cmds.file(q= True, sn = True))[0] + '_backup_Shader.mb'        print '-------PRINT XML --------------'        xmlDoc = xml.dom.minidom.Document()        rootNode = xmlDoc.createElement('file')        fileName = os.path.split(cmds.file(q= True, sn = True))[1]        rootNode.setAttribute('name', fileName)        xmlDoc.appendChild(rootNode)        fbxDirNode = xmlDoc.createElement('fbxfile')        fbxDirNode.setAttribute('name', fbxFile)        rootNode.appendChild(fbxDirNode)        for shader in self._shaderDAGNodes:            shaderNode = xmlDoc.createElement('shader')            shaderNode.setAttribute('name', shader[0])            rootNode.appendChild(shaderNode)            for node in shader:                if node == shader[0]:                     continue                dagNode = xmlDoc.createElement('node')                dagNode.setAttribute('name', node[0].replace('Shape',''))                shaderNode.appendChild(dagNode)                faceNode = xmlDoc.createElement('face')                data = ''                for i in node:                    if i == node[0]:#.rstrip('Shape'):                        continue                    data += str(i) + ','                textNode = xmlDoc.createTextNode(data.rstrip(','))                faceNode.appendChild(textNode)                dagNode.appendChild(faceNode)         # -------------- write XML to file        text = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.xml'        #copyToClipboard(text)        cf.setDataToClipboard(text)        openStream = open(os.path.splitext(cmds.file(q= True, sn = True))[0] + '.xml', 'w')        openStream.write(xmlDoc.toprettyxml())        openStream.close()           def exportMaya(self):        #print 'Exporting file FBX .......'        selectedNode = cmds.ls(sl = True)        if len(cmds.ls(sl = True)) != 0:            filename = ''            # -- collect Shader info to save XML file            shaderNodes = cmds.ls(mat = True)            for shader in shaderNodes:                if shader in ['lambert1','particleCloud1']:                    continue                shaderDAGNodes = list()                shaderDAGNodes.append(shader)                cmds.hyperShade(objects = shader)                selObjs = cmds.ls(sl = True, fl = True)                    #print selObjs                        out = filterShaderNodes(selObjs)                for i in out:                    shaderDAGNodes.append(i)                self._shaderDAGNodes.append(shaderDAGNodes)            # ------- Export to FBX whole Scene            cmds.select(selectedNode)            fileName = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.fbx'            mel.eval('FBXExportSmoothingGroups -v true')            mel.eval('FBXExportUpAxis z')            mel.eval('FBXExportScaleFactor 1.0')            mel.eval('FBXExport -f \"{f}\" -s'.format(f = fileName))            #cmds.file(es = True)            self.writeXML()        else:            MessageBox = ctypes.windll.user32.MessageBoxA            MessageBox(None,'Vui long chon mot object truoc khi export' , 'Notice', 0)            # ------- Export Shader info to XML file        #self.writeXML()#        try:#            #mel.eval('FBXExportFileVersion "FBX201200"')#            pass#         #        except:#            MessageBox = ctypes.windll.user32.MessageBoxA#            MessageBox(None,'Please enable FBX plugins,thanks.' , 'Notice', 0)         class importerShader():    def __init__(self):        self.shaderDAGNodes = list()            def readXML(self):        xmlDir = cf.getDataFromClipboard()        print xmlDir        #if not os.path.isfile(xmlDir):        #    return False        xmldoc = xml.dom.minidom.parse(xmlDir)        fbxFile = xmldoc.getElementsByTagName('fbxfile')[0].getAttribute('name')        shaderNodes = xmldoc.getElementsByTagName('shader')        for shader in shaderNodes:            tmpList = list()            tmpList.append(shader.getAttribute('name'))            nodes = shader.getElementsByTagName('node')            for node in nodes:                    tmpNode = list()                tmpNode.append(node.getAttribute('name'))                faceNode = node.getElementsByTagName('face')[0]                texData = faceNode.childNodes[0].data                tmpNode.append(texData.strip('\t\n\r'))                tmpList.append(tmpNode)            self.shaderDAGNodes.append(tmpList)        return fbxFile            def importMaya(self):        fbxFile = self.readXML()        mel.eval('FBXImportUnlockNormals -v true')        mel.eval('FBXImportSmoothingGroups -v true')        mel.eval('FBXImportUpAxis y')        mel.eval('FBXImport -f \"{f}\"'.format(f = fbxFile))        newname = os.path.splitext(os.path.split(fbxFile)[1])[0]        cmds.file(rn = newname)        cmds.file(save = True, typ = 'mayaBinary')        for shader in self.shaderDAGNodes:            for node in shader:                if node == shader[0]:                     continue                else:                    out = selectFromString(node)                    cmds.select(out)                    cmds.hyperShade(assign = shader[0])