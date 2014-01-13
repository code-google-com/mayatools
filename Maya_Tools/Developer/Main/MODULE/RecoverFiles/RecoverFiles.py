import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect

import Source.IconResource_rc

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/RecoverFiles.ui'

form_class, base_class = uic.loadUiType(dirUI)  

class TreeItem(object):
    def __init__(self, data, parent=None):
        self._parent = parent
        self._itemData = data
        self._children = []
        
        if parent is not None:
            parent.addChild(self)
            
    def nodeType(self):
        if os.path.isfile(data[1]):
            return 'file'
        if os.path.isdir(data[1]):
            return 'path'

    def addChild(self, item):
        self._children.append(item)

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def columnCount(self):
        return len(self._itemData)

    def data(self, column):
        try:
            return self._itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        return 0
    
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, header, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(header)
        self._headers = header
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None
        else:
            if index.column() != 0:
                item = index.internalPointer()
                return item.data(index.column())
        
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                item = index.internalPointer()
                #children = item.childCount()
                if item.nodeType() == 'file':
                    result = self._data[self._data.index(parent.data(0))][0][0]
                    if result == True:
                        pixmap = QtGui.QPixmap(':/Project/Check.png')
                        icon = QtGui.QIcon(pixmap)
                        return icon
                    elif result == False:
                        pixmap = QtGui.QPixmap(':/Project/Delete.png')
                        icon = QtGui.QIcon(pixmap)
                        return icon
            if index.column() == 1:
                item = index.internalPointer()
                if item.nodeType() == 'path':
                    pixmap = QtGui.QPixmap(':/Project/Documents.png')
                    icon = QtGui.QIcon(pixmap)
                    return icon
                    
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return self._headers[section]

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, data, parent):
        parents = [parent]
        indentations = [0]
        # filter parents
        for id in range(len(data[0])):
            pathNode = TreeItem(['',data[0][id],'',''], parent)
            #parent.addChild(pathNode)
#         number = 0
# 
#         while number < len(lines):
#             position = 0
#             while position < len(lines[number]):
#                 if lines[number][position] != ' ':
#                     break
#                 position += 1
# 
#             lineData = lines[number][position:].trimmed()
# 
#             if lineData:
#                 # Read the column data from the rest of the line.
#                 columnData = [s for s in lineData.split('\t') if s]
# 
#                 if position > indentations[-1]:
#                     # The last child of the current parent is now the new
#                     # parent unless the current parent has no children.
# 
#                     if parents[-1].childCount() > 0:
#                         parents.append(parents[-1].child(parents[-1].childCount() - 1))
#                         indentations.append(position)
# 
#                 else:
#                     while position < indentations[-1] and len(parents) > 0:
#                         parents.pop()
#                         indentations.pop()
# 
#                 # Append a new item to the current parent's list of children.
#                 parents[-1].appendChild(TreeItem(columnData, parents[-1]))
# 
#             number += 1
 

class RecoverFiles(form_class,base_class):
    signalChangeTexture = QtCore.pyqtSignal('QString', name = 'textureChanged')
    def __init__(self):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'File Managers'
        self.btnAnalyzeScene.clicked.connect(self.analyzeScene)
        self.btnSelectMissingTextures.clicked.connect(self.selectMissingTexture)
        self.btnAssigntoDirectories.clicked.connect(self.assigntoAnotherDir)
        self.cbbFileFormat.currentIndexChanged.connect(self.updateFormat)
        self.cbbFilter.currentIndexChanged.connect(self.updateStatus)
        self.btnchangeFormat.clicked.connect(self.changeFormatType)
        self.cbbFilter.addItems(['All','Found','Missing'])
        self.cbbTargetType.addItems(['.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.cbbFileFormat.addItems(['All files','.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.ldtNewName.returnPressed.connect(self.changeTextureFiles)
        
    def analyzeScene(self):
        textureNodes = py.ls(typ = ['file','psdFileTex','mentalrayTexture'])
        shaderNodes = py.ls(type = ['cgfxShader', 'hlslShader', 'dx11Shader'])
        #-- filter location: filter for first element in files list
        arrFilter = list()
        arrFilter.append([])
        arrFilter.append([])
        #----
        for f in textureNodes + shaderNodes:
            fileInfos = list()
            # -- get texture infos
            path = ''
            if f in textureNodes:
                status =  os.path.isfile(f.fileTextureName.get())
                name = os.path.split(f.fileTextureName.get())[1]
                path = os.path.split(f.fileTextureName.get())[0]
                res = str(int(f.outSizeX.get())) + 'x' + str(int(f.outSizeY.get()))
                fileInfos = [status, name, res]
            else:
                status = os.path.isfile(f.shader.get())
                name = os.path.split(f.shader.get())[1]
                path = os.path.split(f.shader.get())[0]
                fileInfos = [status, name, 'N/A']
            # -- 
            if not path in arrFilter[0]: # new texture not in list
                fileNamesPerPath = list()
                fileNamesPerPath.append(fileInfos)
                arrFilter[0].append(path)
                arrFilter[1].append(fileNamesPerPath)
            else: # texture already stay in list
                id = arrFilter[0].index(path)
                arrFilter[1][id].append(fileInfos)        
        #-- create treeView model:
        
        header = ('', 'File Name', 'Dimension','Tag')
        model = TreeModel(arrFilter, header)
        self.treeViewResult.setModel(model)
        
           
    def on_tableWidgetResult_cellClicked(self,row,column):
        files = cmds.ls(typ = ['file','psdFileTex','mentalrayTexture'])
        for file in files:
            path = cmds.getAttr(file + '.fileTextureName')
            itemSelected = self.tableWidgetResult.item(row,2)
            if itemSelected.text() == path:
                cmds.select(file)
                self.signalChangeTexture.emit(path)
                break
            
    def on_tableWidgetResult_cellDoubleClicked(self, row, column):
        print 'Okie'
            
    def selectMissingTexture(self):
        row = self.tableWidgetResult.rowCount()
        column = self.tableWidgetResult.columnCount()
        self.tableWidgetResult.setRangeSelected(QtGui.QTableWidgetSelectionRange(0,0,row-1,column-1),False)
        for i in range(row):
            setitem = self.tableWidgetResult.item(i,0)
            if setitem.text() == 'Missing':
                fileName = self.tableWidgetResult.item(i,1)
                fileLocation = self.tableWidgetResult.item(i,2)
                fileNode = self.tableWidgetResult.item(i,3)
                #self.tableWidgetResult.selectRow(i)
                self.tableWidgetResult.setItemSelected (setitem,True)
                self.tableWidgetResult.setItemSelected (fileName,True)
                self.tableWidgetResult.setItemSelected (fileLocation,True)
                self.tableWidgetResult.setItemSelected (fileNode,True)
                
        self.tableWidgetResult.show()
    
    def assigntoAnotherDir(self):
        #-- get dir of current scene
        dirfile = os.path.split(cmds.file(q= True,sn= True))[0]
        #-- get selected items from Table widget
        listSelectedFiles = self.tableWidgetResult.selectedItems()
        #-- warnning if nothing is selected
        if (len(listSelectedFiles) == 0):
             QtGui.QMessageBox.warning(self,'Select Files to redirect location','Please select files you need to redirect location! Thanks',QtGui.QMessageBox.Ok)
        else:
            print dirfile
            returnfromDialog = QtGui.QFileDialog.getOpenFileNames(self,'Select a new location for files',dirfile)
            Dir = os.path.split(str(returnfromDialog[0]))[0]
            for file in listSelectedFiles:
                row = self.tableWidgetResult.row(file)
                if self.tableWidgetResult.column(file) == 2:
                    filename = self.tableWidgetResult.item(row,1)
                    file.setText(Dir + '/' +  filename.text())
                    fileNode = self.tableWidgetResult.item(row,3)
                    cmds.select(str(fileNode.text()))
                    cmds.setAttr(str(fileNode.text()) + '.fileTextureName',Dir + '/' +  str(filename.text()),type='string')
        self.analyzeScene()
        
    def updateStatus(self):
        status = self.cbbFilter.currentText()
        type = self.cbbFileFormat.currentText()
        self.reloadTableWidgetResult(status, type)
    
    def updateFormat(self):
        status = self.cbbFilter.currentText()
        type = self.cbbFileFormat.currentText()
        self.reloadTableWidgetResult(status, type)
    
    def reloadTableWidgetResult(self, status, type):

        row = self.tableWidgetResult.rowCount()
        for i in range(row):
            self.tableWidgetResult.setRowHidden(i,False)
            filterStatus = self.tableWidgetResult.item(i,0).text()
            filterFormat = os.path.splitext(str(self.tableWidgetResult.item(i,1).text()))[1]
            if status == 'All':
                if type == 'All files':
                    self.tableWidgetResult.setRowHidden(i,False)
                else:
                    if filterFormat == type:
                        self.tableWidgetResult.setRowHidden(i,False)
                    else:
                        self.tableWidgetResult.setRowHidden(i,True)
            else:
                if type == 'All files':
                    if filterStatus == status:
                        self.tableWidgetResult.setRowHidden(i,False)
                    else:
                        self.tableWidgetResult.setRowHidden(i,True)
                else:
                    if filterFormat == type and filterStatus == status:
                        self.tableWidgetResult.setRowHidden(i,False)
                    else:
                        self.tableWidgetResult.setRowHidden(i,True)
            
    def changeFormatType(self):
        listSelectedFiles = self.tableWidgetResult.selectedItems()
        if (len(listSelectedFiles) == 0):
             QtGui.QMessageBox.warning(self,'Select Files to change format','Please select files you need to change format! Thanks',QtGui.QMessageBox.Ok)
        else:
            for file in listSelectedFiles:
                row = self.tableWidgetResult.row(file)
                if self.tableWidgetResult.column(file) == 2:
                    filename = self.tableWidgetResult.item(row,2)
                    changedName = os.path.splitext(str(filename.text()))[0] + str(self.cbbTargetType.currentText())
                    fileNode = self.tableWidgetResult.item(row,3)
                    cmds.select(str(fileNode.text()))
                    cmds.setAttr(str(fileNode.text()) + '.fileTextureName',changedName,type='string')
        self.analyzeScene()
        
    def changeTextureFiles(self):
        print '-- execute'
        oldname = str(self.ldtOldName.text())
        newname = str(self.ldtNewName.text())
        listSelectedFiles = self.tableWidgetResult.selectedItems()
        if (len(listSelectedFiles) == 0):
             QtGui.QMessageBox.warning(self,'Select Files to change format','Please select files you need to change format! Thanks',QtGui.QMessageBox.Ok)
        else:
            for file in listSelectedFiles:
                row = self.tableWidgetResult.row(file)
                if self.tableWidgetResult.column(file) == 2:
                    filename = self.tableWidgetResult.item(row,2)
                    changedName = str(filename.text()).replace(oldname, newname)
                    fileNode = self.tableWidgetResult.item(row,3)
                    cmds.select(str(fileNode.text()))
                    cmds.setAttr(str(fileNode.text()) + '.fileTextureName',changedName,type='string')
        self.analyzeScene()    
        
def main():
    form = RecoverFiles()
    return form

    
    
    
    

    

