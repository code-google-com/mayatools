# Author: Tran Quoc Trung - GlassEgg Digtal Media
# Date: 9-SEP-2012

#from array import *

import maya.OpenMayaUI as OpenMayaUI
import inspect, os, sys
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as OpenMayaUI
import sip
import functools
import imp
from xml.dom.minidom import *

#import MySQLdb
from MODULE.ShaderTools import ShaderTools as st
reload(st)

from MODULE.PolyTools import PolyTools as pt
reload(pt)

import CommonFunctions as cf
reload(cf)

import dockWidget as dW
reload(dW)

import Source.IconResource_rc
reload(Source.IconResource_rc)

import getShaderATG
reload(getShaderATG)

import CommonFunctions
reload(CommonFunctions)


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/GE_QA_v3.ui'
try:
   form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def loadRequest(request):
    sys.path.append(fileDirCommmon + '/MODULE/CheckList_QA/')
    sys.path.append(fileDirCommmon + '/MODULE/' + request)
    file, pathname, description = imp.find_module(request)
    try:
        return imp.load_module(request, file, pathname, description)
    finally:
        if file: file.close()
        
class itemDelegate(QtGui.QAbstractItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        return editor
    
    def setEditorData (self, editor, index):
        if index.isValid():
            value = index.model().data(index, QtCore.Qt.DisplayRole)
            iter = editor.findText(value,QtCore.Qt.MatchExactly)
            editor.setCurrentIndex(iter)
                
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
        
class GE_QAModel(QtCore.QAbstractTableModel):
    def __init__(self, objects, checklist, boolArray):
        super(GE_QAModel, self).__init__()
        self.geometry = objects
        self.chkList = checklist
        self.value = boolArray
        
    def rowCount(self, parent =None):
        return len(self.geometry)
    
    def columnCount(self, parent=None):
        return (len(self.chkList) + 1)
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def data(self, index, role):
        if role == QtCore.Qt.TextAlignmentRole:
           return int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter) 
       
        if role == QtCore.Qt.ForegroundRole:
            column = index.column()
            if column != 0:
                brush = QtGui.QBrush()
                color = QtGui.QColor(255, 156, 0, 255)
                brush.setColor(color)
                return brush
        
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                return self.geometry[index.row()]
            elif self.value[column-1][row] not in [False, True]:
                return self.value[column-1][row]
            
        if role == QtCore.Qt.DecorationRole:
            if index.column() != 0:
                result = self.value[index.column() - 1 ][index.row()]
                if result == True:
                    pixmap = QtGui.QPixmap(':/Project/Check.png')
                    icon = QtGui.QIcon(pixmap)
                    return icon
                elif result == False:
                    pixmap = QtGui.QPixmap(':/Project/Delete.png')
                    icon = QtGui.QIcon(pixmap)
                    return icon
            
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return 'DAG Node'
                else:
                    return self.chkList[section - 1]
            if orientation == QtCore.Qt.Vertical:
                return section
            
    def setData(self, index, inValue, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column != 0:
                self.value[row][column] = inValue
                self.dataChanged.emit(index, index) 
                return True
        return False
             
class GE_hintModel(QtCore.QAbstractTableModel): 
    def __init__(self, checkName, message, arr):
        super(GE_hintModel, self).__init__()
        self._check = checkName
        self._messages = message
        #self._details = details
        self._arr = arr
    
    def rowCount(self,parent = None):
        return len(self._messages)
    
    def columnCount(self, parent = None):
        return 3
    
    def headerData(self, section, orientation , role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return 'CHECK'
                if section == 1:
                    return 'EXPLAIN'
                if section == 2:
                    return 'HOW TO FIX' 
                
    def data(self, index, role):
        column = index.column()
        row = index.row()
        
        if role == QtCore.Qt.TextAlignmentRole:
           return int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter) 
       
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():       
                if column == 0:
                    return self._check[row]
                if column == 1:
                    return self._messages[row]
                #if column == 2:
                 #   return self._details[row]
                
        if role == QtCore.Qt.ForegroundRole:
            brush = QtGui.QBrush()
            if self._arr[row] == False:
                color = QtGui.QColor(255, 0, 0, 255)
                brush.setColor(color)
            elif self._arr[row] == True:
                color = QtGui.QColor(0, 255, 0, 255)
                brush.setColor(color)
            elif self._arr[row] == 'Not Available':
                color = QtGui.QColor(255, 156, 0, 255)
                brush.setColor(color)
            else:
                color = QtGui.QColor(255, 156, 0, 255)
                brush.setColor(color)
            return brush
                
    def setData(self, index, value, role):
        if index.isValid():
            column = index.column()
            row = index.row()
            if column == 1:
                self._messages[row] = str(value)
            #if column == 2:
            #    self._details[row] = str(value)
            if column == 3:
                self._arr[row] = value
            self.dataChanged.emit(index, index)
            return True
        return False
                
class GE_QA(form_class,base_class):
    def __init__(self, projData, checkList, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.btnRefresh.clicked.connect(self.getDAGNodeinScene)
        self.btnStartQA.clicked.connect(self.startQA)
        #self.listShader.itemClicked.connect(self.selectFacesOnSelectedItem)
        #self.listShader.itemDoubleClicked.connect(self.selectShaderForEditing)
        #self.scriptjobQA = cmds.scriptJob(e = ['SelectionChanged', self.updateInverseFromScene] , protected = True)
        self._checkList = checkList 
        self._data = projData
        self.valueQA = [] # list return value after checking.
        self.hintListQA = []
        self.tmpArr = [] # list of DAG Node need to be checked.
        self.fileInfo = ''
        self.load()
    
    def updateInverseFromScene(self):
        selectNode = cmds.ls(sl = True)[0]
        stringList = self.lstViewDAGNode.model().stringList()
        id = stringList.indexOf(selectNode)
        # because two models above have the same order, we will get only index and then apply for two those things.
        index = QtCore.QModelIndex(id,0)
        self.lstViewDAGNode.setCurrentIndex(index)
        self.tableQAResult.setCurrentIndex(index)
        
    def getDAGNodeinScene(self):
        selObjs = cmds.ls(type = 'mesh')
        for obj in selObjs:
            parentNode = cmds.listRelatives(obj, parent = 1, type = 'transform', f= True)[0]
            self.tmpArr.append(parentNode)
        
    def load(self):
        self.updateFileInfo()
        textureForm = loadRequest('RecoverFiles')
        textureView = loadRequest('textureView')    
        self.form = textureForm.main()
        self.view = textureView.main()
        self.formLayout_2.addWidget(self.form)
        self.formLayout_3.addWidget(self.view)
        #newway:
        self.form.textureChanged.connect(self.view.showImage)
        if os.path.isfile(self._data + '/shaderDefinition.xml'):
            formshader = shaderValidator(self._data + '/shaderDefinition.xml')
        else:
            formshader = shaderValidator()
        self.formLayout_6.addWidget(formshader)

    def startQA(self):
        self.hintListQA = []
        self.tmpArr = []
        checkName = []
        totalQA = []
        totalMessage = []
        totalDetails = []
        self.getDAGNodeinScene()
        for column in range(1,(len(self._checkList) + 1)):
            resultQA = [] 
            message = []
            details = []
            instance_rc = loadRequest(self._checkList[column-1])
            checkName.append(instance_rc.__name__)
            for row in range(len(self.tmpArr)):
                result = instance_rc.run(self.tmpArr[row])
                resultQA.append(result[0]) # right or wrong 
                message.append(result[1]) # message from checked module
                try:
                    details.append(result[2])
                except:
                    pass
            #print details
            totalQA.append(resultQA)
            totalMessage.append(message) # store output message from each check list
            totalDetails.append(details) # store output additional info from each check list like the number of component error
            
        self.hintListQA.append(checkName)   # this line is a litte bit bad as no need to store checkName of each module
        self.hintListQA.append(totalMessage)
        self.hintListQA.append(totalDetails)
        self.hintListQA.append(totalQA)
        nodeName = [x.split('|')[-1] for x in self.tmpArr]
        modelQA = GE_QAModel(nodeName, self._checkList, self.hintListQA[len(self.hintListQA) - 1])
        self.tableQAResult.setModel(modelQA)
            
    def on_lstViewDAGNode_clicked(self, index):
        model = self.lstViewDAGNode.model()
        if index.isValid():
            row = index.row()
            column = index.column()
            id = model.createIndex(row, column)
            geometryName = model.data(id, QtCore.Qt.DisplayRole)
            cmds.select(str(geometryName.toString()))
            self.displayPaletteShader(str(geometryName.toString()))
            cmds.select(str(geometryName.toString()))
            
    def selectShaderForEditing(self):
        itemWidget = self.listShader.selectedItems()[0]
        shaderName = str(itemWidget.text())
            
    def selectFacesOnSelectedItem(self):
        itemWidget = self.listShader.selectedItems()[0]
        shaderName = str(itemWidget.text())
        id = self.lstViewDAGNode.selectedIndexes()[0]
        mesh = str(id.data(QtCore.Qt.DisplayRole).toString())
        selFaces = CommonFunctions.selectFaceByShaderPerMesh(shaderName, mesh)
        cmds.select(selFaces)
        
    def on_tabViewHint_clicked(self,index):
        indexTableQA = self.tableQAResult.selectedIndexes()[0]
        rowTableQA = indexTableQA.row()
        geometryIndex = indexTableQA.model().createIndex(rowTableQA, 0)
        geometryName = indexTableQA.model().data(geometryIndex, QtCore.Qt.DisplayRole)
        cmds.select(geometryName)
        selObj = cmds.ls(sl = True)[0]
        id = self.tmpArr.index(selObj)
        if index.isValid():
            model = self.tabViewHint.model()
            row = index.row()
            try:
                cmds.select(self.hintListQA[1][row][id])
            except:
                pass
                
    def on_tableQAResult_clicked(self,index):
        model = self.tableQAResult.model()
        tmpList = []
        if index.isValid():
            row = index.row()
            column = 0
            geometryIndex = model.createIndex(row, column)
            geometryName = model.data(geometryIndex, QtCore.Qt.DisplayRole)
            cmds.select(geometryName)
            #----------------------------------------------------------------
            messages = [] #-- message ouput to comprehend evrything
            display = []  #-- right or wrong to highlight red or green
            checkName = self.hintListQA[len(self.hintListQA) - 1]
            for iter in range(len(self._checkList)):
                messages.append(self.hintListQA[0][iter][row])
                display.append(self.hintListQA[2][iter][row])
            checkName = self._checkList
                
            #----set hint info to model
            for i in range(len(messages)):
                index = self.hintModel.createIndex(i,0)
                self.hintModel.setData(index, checkName[i], QtCore.Qt.DisplayRole)
                index = self.hintModel.createIndex(i,1)
                self.hintModel.setData(index, messages[i], QtCore.Qt.DisplayRole)    
                index = self.hintModel.createIndex(i,3)
                self.hintModel.setData(index, display[i], QtCore.Qt.DisplayRole)
                
    def updateFileInfo(self):
        self.fileInfo = 'File Name: \t' + cmds.file(q = True, sn = True) + '\n'
        self.fileInfo += 'Unit SetUp: \t' + '\n'
        self.fileInfo += ''
        self.txtFileInfo.setPlainText(self.fileInfo)
        
    def displayPaletteShader(self, node):
        self.listShader.clear()
        (iconList, nameList) = getShaderATG.dataShaderFromNode(node)
        for i in range(len(iconList)):
            icon = QtGui.QIcon(iconList[i])
            paletteShaderItem = QtGui.QListWidgetItem(icon,nameList[i],self.listShader, QtGui.QListWidgetItem.Type)
            #self.listShader.addItem(paletteShaderItem)

        
    def refreshList(self):
        refreshList = []
        for i in self._checkList:
            eList = []
            eList.append(i)
            refreshList.append(eList)
        indexList = self.tableQAResult.selectedIndexes()
        for index in indexList:
            row = index.row()
            column = index.column()
            if column != 0:
                refreshList[column-1].append(self.tmpArr[row])
        return refreshList
                  
    def refreshQA(self):
        updateList = self.refreshList()
        for row in updateList:
            instance_rc = loadRequest(updateList[row][0])
            for node in updateList[row]:
                if node == row: 
                    continue
                else:
                    instance_rc.run(node)
                          
description = 'Select Mesh using wrong shader'
name = 'selectWrongShaderNode'

color_code = {'right':['00dc00', '00ff00'], 'wrong':['fa0000','ff0000'], 'missing':['ffdc00','ffff00'], 'undefined':['','']}
status = {1: 'mesh', -1: 'shader'}

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/shader_Validator.ui'
try:    
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found.')
    

    
class shaderButton(QtGui.QPushButton):
    def __init__(self, mesh, shader, color = None):
        super(shaderButton, self).__init__()
        self._mesh = mesh
        self._shader = shader
        #self._color = color
        self.setText(shader)
        self.clicked.connect(functools.partial(st.selectFaceByShaderPerMesh, self._mesh, self._shader))
        self.setStyleSheet('''QPushButton*
                            color: black;
                            background-color: #{color0};
                            border-color: #339;
                            border-style: solid;
                            border-radius: 5;
                            padding: 3px;
                            font-size: 14px;
                            padding-left: 2px;
                            padding-right: 2px;@
                            
                            QPushButton:hover*
                            color: black;
                            background-color: #{color1};
                            border-color: #339;
                            border-style: solid;
                            border-radius: 5;
                            padding: 3px;
                            font-size: 14px;
                            padding-left: 2px;
                            padding-right: 2px;@'''.format(color0 = color[0], color1 = color[1]).replace('*','{').replace('@','}'))
        
    def checkShader(self):
        pass
        
class shaderDockWidget(dW.DockWidget):
    def __init__(self, mesh, node = None):
        super(shaderDockWidget, self).__init__(mesh)
        self._mesh = mesh
        self._widget= QtGui.QWidget()
        self.setWidget(self._widget)
        self._shaderValidator = node
        self.loadShadersOfMesh()
        
    def loadShadersOfMesh(self):
        layout = QtGui.QVBoxLayout()
        margins = QtCore.QMargins(1,1,1,1)
        layout.setSpacing(1)
        layout.setContentsMargins(margins) 
        self._widget.setLayout(layout)
        shadersInMesh = st.getShadersFromMesh(self._mesh)
        shadersInXMLNode = ''
        if self._shaderValidator:
            shadersInXMLNode = [shader.getAttribute('name') for shader in self._shaderValidator.getElementsByTagName('shader')]
            conds = [c.getAttribute('use') for c in self._shaderValidator.getElementsByTagName('shader')]
            shaders = list(set(shadersInXMLNode + shadersInMesh))
        else:
            shaders =  shadersInMesh
        for s in shaders:
            try:
                result = 'undefined'
                if s not in shadersInMesh:
                    if conds[shadersInXMLNode.index(s)] != 'No_use':
                        result = 'missing'
                elif s not in shadersInXMLNode:
                    if conds[0] == 'Only':
                        result = 'wrong'
                else:
                    if conds[shadersInXMLNode.index(s)] == 'No_use':
                        result = 'wrong'
                    else:
                        result = 'right'
            except:
                result = 'undefined'
            #print result        
            button = shaderButton(self._mesh, s, color_code[result])
            layout.addWidget(button)
            
    def loadMeshesUseShader(self):
        pass
    
class shaderValidator(form_class, base_class):
    def __init__(self, xmlFile = None, parent = getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self._status = 1
        if xmlFile:
            self.xmlDoc = xml.dom.minidom.parse(xmlFile)
        self.startup()
        self.btnRefresh.clicked.connect(self.startup)
        self.ldtFind.returnPressed.connect(self.startup)
        
    def startup(self):
        cf.clearLayout(self.formLayout) # remove all items in layout if possible
        shapeNode = ''
        try:
            if self.ldtFind.text() == '':
                shapeNode = [node for node in py.ls(type = 'transform') if py.nodeType(node.listRelatives(c= True)[0]) == 'mesh']
            else:
                shapeNode = [node for node in py.ls('*' + str(self.ldtFind.text()) + '*', type = 'transform') if py.nodeType(node.listRelatives(c= True)[0]) == 'mesh']
        except:
            pass 
        for s in shapeNode:
            try:
                node  = [node for node in self.xmlDoc.getElementsByTagName('mesh') if node.getAttribute('name')  == s][0]
                #print node.getAttribute('name')
                dockWidget = shaderDockWidget(str(s), node)
                self.formLayout.addWidget(dockWidget)
            except:
                #print 'No XML file to filter'
                dockWidget = shaderDockWidget(str(s))
                self.formLayout.addWidget(dockWidget)
                
    def changeStatus(self):
        cf.clearLayout(self.formLayout)
        shaders = cmds.ls(materials = True)
        for s in shaders:
            pass
        
            
    def reload(self):
        pass
        
    
                    
