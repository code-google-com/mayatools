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
            
    def node(self):
        try:
            if self._itemData[1].split('.')[1]:
                return 'file'
        except:
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
        self._missingIndexes = list()
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            if index.column() != 0:
                item = index.internalPointer()
                return item.data(index.column())
            
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 1:
                item = index.internalPointer()
                result = item.data(0)
                if item.node() == 'file':
                    if result == True:
                        pixmap = QtGui.QPixmap(':/Project/Check.png')
                        icon = QtGui.QIcon(pixmap)
                        return icon
                    else:
                        pixmap = QtGui.QPixmap(':/Project/Delete.png')
                        icon = QtGui.QIcon(pixmap)
                        return icon

                elif item.node() == 'path':
                    pixmap = QtGui.QPixmap(':/Project/Open.png')
                    icon = QtGui.QIcon(pixmap)
                    return icon
                    
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.TextAlignmentRole:
           return int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        if role == QtCore.Qt.DisplayRole:
            return self._headers[section]

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            #print 'parent not Valid'
            parentItem = self.rootItem
        else:
            #print 'parent Valid'
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
        # filter parents
        for id in range(len(data[0])):
            pathNode = TreeItem(['',data[0][id],'','', ''], parent)
            pathID = self.index(id, 1, QtCore.QModelIndex())
            for f in data[1][id]:
                f[1] = ' '*10 + f[1]
                fileNode = TreeItem(f, pathNode)
                if f[0] == False:
                    #print data[1][id].index(f)
                    #print pathID.row()
                    if pathID.isValid():
                        miss_Id = self.index(0, 1, pathID)
                        print miss_Id.row()
                        self._missingIndexes.append(miss_Id)
                    
class RecoverFiles(form_class,base_class):
    signalChangeTexture = QtCore.pyqtSignal('QString', name = 'textureChanged')
    def __init__(self):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'File Managers'
        self.btnAnalyzeScene.clicked.connect(self.analyzeScene)
        self.treeViewResult.clicked.connect(self.selectItem)
        self.btnSelectMissingTextures.clicked.connect(self.selectMissingTextures)
        self.btnAssigntoDirectories.clicked.connect(self.assigntoAnotherDir)
        self.cbbFileFormat.currentIndexChanged.connect(self.updateFormat)
        self.cbbFilter.currentIndexChanged.connect(self.updateStatus)
        self.btnchangeFormat.clicked.connect(self.changeFormatType)
        self.cbbFilter.addItems(['All','Found','Missing'])
        self.cbbTargetType.addItems(['.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.cbbFileFormat.addItems(['All files','.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.ldtNewName.returnPressed.connect(self.changeTextureFiles)
        self.treeViewResult.customContextMenuRequested.connect(self.createCustomContextMenu)
        
        self.actionSelect_Textures_Inside.triggered.connect(self.selectAllTextures)
        self.actionSelect_Missing_Files.triggered.connect(self.selectMissingTextures)
        self.actionAssign_to_Another_path.triggered.connect(self.assigntoAnotherDir)
        
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
                path = os.path.split(f.fileTextureName.get())[0].lower()
                res = str(int(f.outSizeX.get())) + 'x' + str(int(f.outSizeY.get()))
                fileInfos = [status, name, res, '',str(f)]
            else:
                status = os.path.isfile(f.shader.get())
                name = os.path.split(f.shader.get())[1]
                path = os.path.split(f.shader.get())[0]
                fileInfos = [status, name, 'N/A', '',str(f)]
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
        
        header = ('', 'File Name', 'Dimension','Tag', 'File Node')
        model = TreeModel(arrFilter, header)
        self.treeViewResult.setModel(model)
        self.treeViewResult.expandAll()
        for i in range(len(header)):
            self.treeViewResult.resizeColumnToContents(i) 
            
    def selectItem(self, index):
        item = index.internalPointer()
        dir = item.parent().data(1)
        fullPath = dir + '/' + item.data(1).strip()
        try:
            cmds.select(item.data(4))
        except:
            pass
        self.signalChangeTexture.emit(fullPath)
        print str(index.row()) + ' ' + str(index.column())
        
    def selectAllTextures(self):
        index = self.treeViewResult.selectedIndexes()[0]
        item = index.internalPointer()
        if item.node() == 'path':
            childCount = item.childCount()
            selectModel = self.treeViewResult.selectionModel()
            selectModel.clearSelection()     
            for id in range(childCount):
                idx = self.treeViewResult.model().index(id,1,index)
                selectModel.select(idx, selectModel.Select|selectModel.Rows)
            
    def selectMissingTextures(self):
        index = self.treeViewResult.selectedIndexes()[0]
        item = index.internalPointer()
        if item.node() == 'path':
            childCount = item.childCount()
            selectModel = self.treeViewResult.selectionModel()
            selectModel.clearSelection()     
            for id in range(childCount):
                idx = self.treeViewResult.model().index(id,1,index)
                status = idx.internalPointer().data(0)
                if status == False:
                    selectModel.select(idx, selectModel.Deselect|selectModel.Rows)
        
    def createCustomContextMenu(self,pos):
        type_ID = [f.internalPointer().node() for f in self.treeViewResult.selectedIndexes()] 
        if 'file'in type_ID:  
            RightClickMenu = QtGui.QMenu(self)
            #RightClickMenu.addAction(self.actionSelect_Missing_Files)
            RightClickMenu.addAction(self.actionAssign_to_Another_path)
            RightClickMenu.addAction(self.actionChange_Format)
            RightClickMenu.addAction(self.actionRename_File)
            RightClickMenu.exec_(QtGui.QCursor.pos())
        if 'path' in type_ID:
            RightClickMenu = QtGui.QMenu(self)
            RightClickMenu.addAction(self.actionSelect_Textures_Inside)
            RightClickMenu.addAction(self.actionSelect_Missing_Files)
            RightClickMenu.addAction(self.actionAssign_to_Another_path)
            RightClickMenu.addAction(self.actionChange_Format)
            RightClickMenu.addAction(self.actionRename_File)
            
            RightClickMenu.exec_(QtGui.QCursor.pos())
        
    def assigntoAnotherDir(self):
        if not self.treeViewResult.selectedIndexes():
            QtGui.QMessageBox.warning(self,'Select Files to redirect location','Please select files you need to redirect location! Thanks',QtGui.QMessageBox.Ok)
        else: 
            dirfile = os.path.split(cmds.file(q = True, sn = True))[0]
            returnfromDialog = QtGui.QFileDialog.getOpenFileNames(self,'Select a new location for files',dirfile)
            dir = os.path.split(str(returnfromDialog[0]))[0]
            for i in self.treeViewResult.selectedIndexes():
                item = i.internalPointer()
                if item.node() == 'path':
                    childCount = item.childCount()
                    for id in range(childCount):
                        try:
                            idx = self.treeViewResult.model().index(id, 1, i)
                            itemx = idx.internalPointer()
                            cmds.setAttr(itemx.data(4) + '.fileTextureName', dir + '/' + itemx.data(1), type = 'string')
                        except:
                            pass
                if item.node() == 'file':
                    cmds.setAttr(item.data(4) + '.fileTextureName', dir + '/' + item.data(1), type = 'string')
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

    
    
    
    

    

