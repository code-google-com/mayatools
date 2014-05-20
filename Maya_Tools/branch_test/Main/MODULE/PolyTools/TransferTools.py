import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mel
import os, sys, inspect
import subprocess
import pymel.core as py
import random
import sip
import xml.dom.minidom as xml
import time, re

#try:
#    reload(PolyTools)
#except:
#    import PolyTools

try:
    reload(transferFunction)
except:
    import transferFunction
    
    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/TransferTools_v3.ui'
try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')

# set up some global variables

version = 'Maya2013.5' # version maya
mayaPath = '\"'+os.environ.get("PROGRAMFILES").replace('\\', '/')+'/Autodesk/'+version+'/bin/mayabatch.exe"'
#mayaPath = '\"E:/Program Files/Autodesk/'+version+'/bin/mayabatch.exe\"'

## Files needed to clean up whenever everything is done
xmlFile = transferFunction.xmlDir
xmlPairFile = transferFunction.root + 'xmlPairFile.xml'
storedDataFile = transferFunction.root + 'storedMaya.mb'

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def browser():
    mayaFilter = 'Maya Files (*.ma *.mb);;Maya ASCII (*.ma);; Maya Binary (*.mb);;Object (*.obj);;FBX Files (*.fbx);; All Files (*.*)'
    mayafile = cmds.fileDialog2(cap = 'Browser File', dir = 'D:/', ff = mayaFilter, fileMode = 1, okc = 'Open')    
    return mayafile[0]

class DropDownListDelegate(QtGui.QItemDelegate):
    def __init__(self, masterList):
        super(QtGui.QItemDelegate,self).__init__(parent = None)
        self._masterList = masterList
    
    def createEditor(self, parent, option, index):
        if index.column():
            self.editor = QtGui.QComboBox(parent)
            stringList = QtGui.QStringListModel()
            stringList.setStringList(self._masterList[index.row()][index.column()])
            self.editor.setModel(stringList)
            return self.editor

    def setModelData(self, editor, model, index):
        value = self.editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def setEditorData(self, editor, index):
        if index.column():
            asset = index.model().data(index, QtCore.Qt.EditRole)
            id = self.editor.findText(asset.toString())
            self.editor.setCurrentIndex(id)
            
    def removeItemData(self, index, value):
        if index.column() == 1:
            row = index.row()
            try:
                self._masterList[row][column].remove(value)
            except:
                pass
            
    def appendItemData(self, index, value):
        if index.column() == 1:
            row = index.row()
            self._masterList[row][columm].append(value)
            
            
class customModel(QtCore.QAbstractItemModel):
    def __init__(self, masterList):
        self._internalList = masterList
        self._selectedItems = list()
        
    def rowCount(self):
        return len(self._internalList)
    
    def columnCount(self):
        return 3
    
    def data(self, index, role):
        if role == QtCore.Qt.TextAlignmentRole:
            return int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():       
                return self._internalList[index.row()][index.column()]
                #if column == 2:
                 #   return self._details[row]
        if role == QtCore.Qt.ForegroundRole:
            if index.isValid():
                column = index.column()
                if column != 0:
                    data = index.data().toString()
                    brush = QtGui.QBrush()
                    if data in self._selectedItem:
                        color = QtGui.QColor(125,125,125)
                        brush.setColor(color)
                    else:
                        color = QtGui.QColor(255, 255, 255)
                        brush.setColor(color)
                    return brush
                
    def setData(self, index, data, role):
        pass
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return 'MESH'
                if section == 1:
                    return 'SHADER'
                if section == 2:
                    return 'UVSET'
                        
    def insertRow(self, data, role):
        self._internalList.append(data)
        
    def appendItemToSelected(self, value):
        self._selectedItems.append(value)
        
class TransferTools(form_class,base_class):
    def __init__(self, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
#        self._masterListSourceModel = QtGui.QStandardItemModel()
#        self._masterListTargetModel = QtGui.QStandardItemModel()
#        self._listSource = []
#        self._listTarget = []
        self._pair = [[], []]
        self.setObjectName('transferWindow')
        self.ldtMayaFile.setReadOnly(True)
        self.btnGetScene.clicked.connect(self.loadScene)
#        self.btnOpenFile.clicked.connect(self.batchExecute)
        self.actionMark.triggered.connect(self.markShader)
        self.actionUnMark.triggered.connect(self.UnMarkShader)
#        self.actionUn_Pair.triggered.connect(self.unPairFiles)
#        self.btnPair.clicked.connect(self.pairFiles)
        self.listIcon.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
#        self.tbvScene.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
#        self.tbvFile.viewportEntered.connect
#        self.btnClearSceneView.clicked.connect(self.clearSceneView)
#        self.btnClearFileView.clicked.connect(self.clearFileView)
#        self.btnUV.clicked.connect(self.transferUV)
#        self.initView(self._masterListSourceModel, self.tbvFile)
#        self.initView(self._masterListTargetModel, self.tbvScene)
        
#    def cleanUp(self):
#        self._pair = []
#        if os.path.exists(xmlFile):
#            os.remove(xmlFile)
#        if os.path.exists(xmlPairFile):
#            os.remove(xmlPairFile)
#        if os.path.exists(storedDataFile):
#            os.remove(xmlPairFile)
#        if os.path.exists(storedDataFile):
#            os.remove(storedDataFile)
            
#    def pickObject(self, model, tableView):
#        sel = cmds.ls(sl = True, transform = True)
#        masterList = list()
#        for node in sel:
#            element = list()
#            shader = transferFunction.getShaderFromNode(node)
#            if shader:
#                element.append(node)
#                element.append(shader)
#                element.append(transferFunction.getUVFromNode(node))
#                masterList.append(element)
#        self.loadDatatoUI()
#                 
#    def killBatch(self):
#        batchKill = 'taskkill /F /IM mayabatch.exe'
#        p = subprocess.Popen('"'+ batchKill + '"', shell=True).wait()
#        
#    def loadDatatoUI(self, masterList, model, tableView):
#        length = len(masterList)
#        model.setRowCount(length)
#        delegate = DropDownListDelegate(masterList)
#        for row in range(length):
#            for column in range(3):
#                if column == 0:
#                    index = model.index(row, column, QtCore.QModelIndex())
#                    model.setData(index, masterList[row][0], QtCore.Qt.DisplayRole)
#                else:
#                    tableView.setItemDelegateForColumn(column,delegate)
#                    index = model.index(row, column, QtCore.QModelIndex())
#                    model.setData(index, masterList[row][column][0])
#        tableView.resizeColumnsToContents()
                
#    def batchExecute(self):
#        mayafile = browser()
#        self.ldtMayaFile.setText(mayafile)
#        if not os.path.exists(mayafile):
#            return
#        self.killBatch()
#        cmds.pause(sec = 1)  
#    # load scene in background and update UI
        mayaPython = '"python(\\\"import sys;sys.path.append(\'' + fileDirCommmon + '\'); import transferFunction; transferFunction.getAssetBatchMode(execFile = \'' + mayafile + '\')\\\")"'
#        errorOutput = '"' + transferFunction.root + 'error.txt"'
#        p = subprocess.Popen('"' + mayaPath + " -log " + errorOutput + " -c " + mayaPython + '"', shell = True)
#        t0 = time.time()
#        delta = 0
#        while not os.path.exists(xmlFile) & (delta < 20):
#            delta = time.time() - t0
#            cmds.pause(sec = 1)
#        self.loadFile()
#        #self.cleanUp() 
#    
#    def unPairFiles(self):
#        Color = QtGui.QColor(42,42,42)
#        

    def redrawListIcon(self):
        pass
        
    def UnMarkShader(self):
        color = QtGui.QColor(0,0,0)
        mesh = self.listWidget.currentItem().text()
        shaders = self.listIcon.selectedItems()
        try:
            id = self._pair[0].index(mesh)
            if len(self._pair[1][id]) == 0:
                for s in shaders:
                    self._pair[1].remove(self._pair[1][id])
                    self.listWidget.currentItem().setBackgroundColor(color)
        except:
            pass

    def markShader(self):
        randomColor = QtGui.QColor(0,255,0, 125)
        self.listWidget.currentItem().setBackgroundColor(randomColor)
        item = self.listWidget.currentItem()
        mesh = item.text()
        shaders = self.listIcon.selectedItems()
        # append shader to mesh in already in pair list
        try:
            id = self._pair[0].index(mesh)
            for s in shaders:
                self._pair[1][id].append(str(s.text()))
                s.setBackgroundColor(randomColor)
        except:
            self._pair[0].append(mesh)
            shaderList = list()
            for s in shaders:
                shaderList.append(str(s.text()))
                s.setBackgroundColor(randomColor)
            self._pair[1].append(shaderList)
        #print self._pair
        
    def on_listWidget_itemClicked(self, itemListWidget):
        self.listIcon.clear()
        mesh = itemListWidget.text()
        paint = False
        if mesh in self._pair[0]:
            paint = True
        shaders = transferFunction.getShaderFromNodes(str(mesh))
        for shader in shaders:
            xmlPath = cmds.getAttr(shader + '.RawPath')
            iconPath = xmlPath.replace('.xml','_swatch_' + str(128) + '.bmp')
            #name = os.path.split(os.path.splitext(iconPath)[0])[1].replace('_swatch_' + str(128),'')
            icon = QtGui.QIcon(iconPath)
            paletteShaderItem = QtGui.QListWidgetItem(icon,shader,self.listIcon, QtGui.QListWidgetItem.Type)
            self.listIcon.addItem(paletteShaderItem)
            if paint:
                id = self._pair[0].index(mesh)
                if name in self._pair[1][id]:
                    paletteShaderItem.setBackgroundColor(QtGui.QColor(0,255,0, 125))
           
    def loadScene(self):
        self.listWidget.clear()
        nodes = cmds.ls(transforms = True)
        #mesh = []
        for n in nodes:
            childNode = cmds.listRelatives(n, shapes = True)
            if cmds.nodeType(childNode) != 'camera':
                #mesh.append(n)
                item = QtGui.QListWidgetItem(n)
                self.listWidget.addItem(item)

    def createRightClickonMenu_on_selectedItems(self, pos):
        RightClickMenu = QtGui.QMenu(self)
        RightClickMenu.addAction(self.actionMark)
        RightClickMenu.addAction(self.actionUnMark)
        RightClickMenu.exec_(QtGui.QCursor.pos())
        
#    def makingXMLFromPairObjects(self):
#        xmlDoc = xml.Document()
#        root = xmlDoc.createElement('root')
#        root.setAttribute('name', self.ldtMayaFile.text())
#        xmlDoc.appendChild(root)
#        for index in range(len(self._pair)):
#            pairNode = xmlDoc.createElement('pair')
#            #
#            pairItemNodeScene = xmlDoc.createElement('meshScene')
#            pairItemNodeScene.setAttribute('name', self._pair[index][0][0])
#            pairItemNodeScene.setAttribute('shader', self._pair[index][0][1])
#            pairItemNodeScene.setAttribute('uvSet', self._pair[index][0][2])
#            #
#            pairNode.appendChild(pairItemNodeScene)
#            #
#            pairItemNodeFile = xmlDoc.createElement('meshFile')
#            pairItemNodeFile.setAttribute('name', self._pair[index][1][0])
#            pairItemNodeFile.setAttribute('shader', self._pair[index][1][1])
#            pairItemNodeFile.setAttribute('uvSet', self._pair[index][1][2])
#            #
#            pairNode.appendChild(pairItemNodeFile)
#            #
#            root.appendChild(pairNode)
#        transferFunction.writeXML(xmlDoc,xmlPairFile) 
#    
#    def loadpairObjectFromXML(self):
#        xmlDoc = xml.parse(xmlPairFile)
#        pairNodes = xmlDoc.getElementsByTagName('pair')
#        for p in pairNodes:
#            pair = []
#            targetNode = p.getElementsByTagName('meshScene')[0].getAttribute('name') + '__' + p.getElementsByTagName('meshScene')[0].getAttribute('shader') + '_target_unwrapped'
#            pair.append(targetNode)
#            sourceNode = 'temp:' + p.getElementsByTagName('meshFile')[0].getAttribute('name') + '__' + p.getElementsByTagName('meshFile')[0].getAttribute('shader') + '_source_unwrapped'
#            pair.append(sourceNode)
#            self._pair.append(pair)
#    
#    def loadXMLExtractMeshData(self):
#        xmlDoc = xml.parse(xmlPairFile)
#        pairNodes = xmlDoc.getElementsByTagName('pair')
#        for pair in pairNodes:
#            mesh = pair.getElementsByTagName('meshScene')[0].getAttribute('name')
#            print mesh
#            shader = pair.getElementsByTagName('meshScene')[0].getAttribute('shader')
#            print shader
#            transferFunction.getFaceFromSelectedShaderAndSelectedMesh(shader, mesh)
#            newname = mesh + '__' + shader + '_target_unwrapped'
#            cmds.rename(newname)         
#        
#    def transferUV(self):
#        self.makingXMLFromPairObjects()
#        self._pair = list()
#        self.killBatch()
#        cmds.pause(sec = 1) 
#        t0 = time.time()
#        mayaPython = '"python(\\\"import sys;sys.path.append(\'' + fileDirCommmon + '\'); import transferFunction; transferFunction.loadXMLExtractMeshData()\\\")"'
#        errorOutput = '"' + transferFunction.root + 'error_01.txt"'
#        p = subprocess.Popen('"' + mayaPath + " -log " + errorOutput + " -c " + mayaPython + '"', shell = True)
#        delta = 0
#        while not os.path.exists(storedDataFile) & (delta < 20):
#            delta = time.time() - t0
#            #cmds.pause(sec = 1)
#        self.loadXMLExtractMeshData()
#        # reference file
#        cmds.file(storedDataFile, r = True, namespace = 'temp')
#        self.loadpairObjectFromXML()
#        for p in self._pair:
#            cmds.transferAttributes(p[1] + 'Shape', p[0] + 'Shape', uvs = 2)
#            # clean up object
#            cmds.select(p[0])
#            mel.eval('DeleteHistory')
#            # attach target node to oirigin
#            origin = p[0].split('__')[0]
#            try:
#                print 'multi material'
#                cmds.select(origin, r = True)
#                cmds.select(p[0], add = True)
#                attachFileSource = fileDirCommmon + '/flattenCombine.mel'
#                mel.eval('source \"{f}\";'.format(f = attachFileSource))
#                cmds.polyMergeVertex(origin, d = 0.001)
#            except ValueError: # object has only one material and cannot extract faces.
#                print 'single material'
#                cmds.select(p[0], r = True)
#                cmds.rename(origin)
#
#        # unreference maya file
#        cmds.file(storedDataFile, rr = True)
#        # refresh view and clean data
#        self.refreshSceneView()
#        self.refreshFileView()
#        self.cleanUp()
#
#    def clearSceneView(self):
#        self._masterListTargetModel.clear()
#        self._pair = list()
#        self.initView(self._masterListTargetModel, self.tbvScene) 
#    
#    def clearFileView(self):
#        self._masterListSourceModel.clear()
#        self._pair = list()
#        self.initView(self._masterListSourceModel, self.tbvFile)
#        
#    def updateListIconWidget(self, mesh, meshS):
#        self.listWidget.clear()
#        shaders = list()
#        for p in self._pair: 
#            print p[0][0]
#            print p[1][0]
#            print '---------------'
#            print mesh
#            print meshS
#            if (p[0][0] == mesh) & (p[1][0] == meshS):                
#                shaders.append(p[0][1])
#                shaders.append(p[1][1])
#        shaders = list(set(shaders))
#        print shaders
#        ATGShaderPath = list()
#        for s in shaders:
#            xmlPath = cmds.getAttr(str(s) + '.RawPath')#.replace('.xml','_swatch_' + str(128) + '.bmp')
#            iconPath = xmlPath.replace('.xml','_swatch_' + str(128) + '.bmp')
#            name = os.path.split(os.path.splitext(iconPath)[0])[1].replace('_swatch_' + str(128),'')
#            icon = QtGui.QIcon(iconPath)
#            paletteShaderItem = QtGui.QListWidgetItem(icon,name,self.listWidget, QtGui.QListWidgetItem.Type)
#            self.listWidget.addItem(paletteShaderItem)
#                        
#    def getEncounters(self, name):
#        result = re.search('(.*)_LOD[1-9]',name)
#        if result:
#            return result.group(1)  
#        else:
#            result = name + '_LOD'
#        
#    def on_tbvScene_clicked(self, index):
#        row = index.row()
#        mesh = ''
#        shader = ''
#        uv = ''
#        meshS = ''
#        if self.chkAutoMatching.isChecked():
#            for i in self.tbvScene.selectedIndexes():
#                if i.column() == 0:
#                    mesh = i.data().toString()
#                if i.column() == 1:
#                    shader = i.data().toString()
#                if i.column() == 2:    
#                    uv = i.data().toString()  
#            for i in range(len(self._listSource)):
#                if self._listSource[i][0] == self.getEncounters(mesh):
#                    indexS = self._masterListSourceModel.createIndex(i,0)
#                    meshS = self._listSource[i][0]
#                    self.tbvFile.setCurrentIndex(indexS)
#                    idSShader = self._masterListSourceModel.createIndex(i,1)
#                    self.tbvFile.update()
#            self.updateListIconWidget(mesh,meshS)
#             
#        
#    def on_tvbFile_clicked(self, index):
#        pass