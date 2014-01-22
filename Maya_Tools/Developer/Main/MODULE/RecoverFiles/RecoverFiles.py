import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import functools

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
    def __init__(self, data = None, header = None, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(header)
        self.rootIndex = self.createIndex(0, 0, self.rootItem)
        self._headers = header
        if data is not None:
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
                
class CustomFilterSortModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(QtGui.QSortFilterProxyModel, self).__init__()
        self._fileStatus = 'All'
        
    def update(self, status):
        self._fileStatus = status
        
    def filterAcceptsRow(self, row_num, source_parent):
        srcId = self.sourceModel().index(row_num, 1, source_parent)
        if srcId.internalPointer().node() == 'file':
            return super(CustomFilterSortModel, self).filterAcceptsRow(row_num, source_parent) and self.filterMissingFiles(row_num, source_parent)
        if srcId.internalPointer().node() == 'path':
            return True
            #return self.hasChildrenAccepts(srcId)

    def hasChildrenAccepts(self, parent):
        result = False
        num = parent.internalPointer().childCount()
        id = 0
        while id < num and not result:
            result = self.filterAcceptsRow(id, parent)
            id += 1
        return result
    
    def filterMissingFiles(self, row, parent):
        if self._fileStatus == 'All':
            return True
        elif self._fileStatus == 'Found':
            item = self.sourceModel().index(row, 1, parent).internalPointer()
            if item.data(0) == True:
                return True
            else:
                return False
        elif self._fileStatus == 'Missing':
            item = self.sourceModel().index(row, 1, parent).internalPointer()
            if item.data(0) == True:
                return False
            else:
                return True
        
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
        self.btnchangeFormat.clicked.connect(functools.partial(self.changeFormatType,str(self.cbbTargetType.currentText())))
        self.cbbFilter.addItems(['All','Found','Missing'])
        self.cbbTargetType.addItems(['.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.cbbFileFormat.addItems(['All files','.psd','.tga','.png','.tif','.dds','.bmp','.jpg'])
        self.ldtNewName.returnPressed.connect(self.changeTextureFiles)
        self.treeViewResult.customContextMenuRequested.connect(self.createCustomContextMenu)
        
        self.actionSelect_Textures_Inside.triggered.connect(self.selectAllTextures)
        self.actionSelect_Missing_Files.triggered.connect(self.selectMissingTextures)
        self.actionAssign_to_Another_path.triggered.connect(self.assigntoAnotherDir)
        self.actionChange_Format.triggered.connect(self.changeFormatType)
        
        self._filterProxyModel = CustomFilterSortModel()#QtGui.QSortFilterProxyModel()
        self._filterProxyModel.setFilterKeyColumn(1)
        self._filterProxyModel.setDynamicSortFilter(True)
        #self._model = TreeModel(None, None, None)
        #self._filterProxyModel.setSourceModel(self._model)
        
        self.cbbFileFormat.currentIndexChanged.connect(self.setFilterForProxyModel)
        self.cbbFilter.currentIndexChanged.connect(self.setFilterForProxyModel)
        
    def setFilterForProxyModel(self):
        fileType = self.cbbFileFormat.currentText()
        fileStatus = self.cbbFilter.currentText()
        if fileStatus == 'All':
            self._filterProxyModel.update('All')
        elif fileStatus == 'Missing':
            self._filterProxyModel.update('Missing')
        elif fileStatus == 'Found':
            self._filterProxyModel.update('Found')
        
        if fileType == 'All files':
            self._filterProxyModel.setFilterRegExp('')
        else:
            self._filterProxyModel.setFilterRegExp(fileType)
            
        
        self.treeViewResult.expandAll()
        
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
                tag = QtGui.QPictureIO(str(f),'.tif')
                try:
                    res = str(int(f.outSizeX.get())) + 'x' + str(int(f.outSizeY.get()))
                except AttributeError:
                    res = 'not available'
                fileInfos = [status, name, res, tag.description(),str(f)]
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
        
        header = ('', 'File Name', 'Resolution','Tag', 'File Node')
        self._model = TreeModel(arrFilter, header)
        self._filterProxyModel.setSourceModel(self._model)
        self.treeViewResult.setModel(self._filterProxyModel)
        self.treeViewResult.expandAll()
        for i in range(len(header)):
            self.treeViewResult.resizeColumnToContents(i) 
            
    def selectItem(self, index):
        mappedIndex = self._filterProxyModel.mapToSource(index)
        item = mappedIndex.internalPointer()
        dir = item.parent().data(1)
        fullPath = dir + '/' + item.data(1).strip()
        try:
             cmds.select(item.data(4))
        except:
             pass
        self.signalChangeTexture.emit(fullPath)
        print index.row()
        
    def selectAllTextures(self):
        index = self.treeViewResult.selectedIndexes()[0]
        mappedIndex = self._filterProxyModel.mapToSource(index)
        item = mappedIndex.internalPointer()
        if item.node() == 'path':
            childCount = item.childCount()
            selectModel = self.treeViewResult.selectionModel()
            selectModel.clearSelection()     
            for id in range(childCount):
                idx = self._model.index(id,1,mappedIndex)
                mappedIdx = self._filterProxyModel.mapFromSource(idx)
                selectModel.select(mappedIdx, selectModel.Select|selectModel.Rows)
            
    def selectMissingTextures(self):
        index = self.treeViewResult.selectedIndexes()[0]
        mappedIndex = self._filterProxyModel.mapToSource(index)
        item = mappedIndex.internalPointer()
        if item.node() == 'path':
            childCount = item.childCount()
            selectModel = self.treeViewResult.selectionModel()
            selectModel.clearSelection()     
            for id in range(childCount):
                idx = self._model.index(id,1,mappedIndex)
                status = idx.internalPointer().data(0)
                if status == False:
                    mappedIdx = self._filterProxyModel.mapFromSource(idx)
                    selectModel.select(mappedIdx, selectModel.Select|selectModel.Rows)
        
    def createCustomContextMenu(self,pos):
        type_ID = [self._filterProxyModel.mapToSource(index).internalPointer().node() for index in self.treeViewResult.selectedIndexes()] 
        RightClickMenu = QtGui.QMenu(self)
        formatMenu = QtGui.QMenu('Change Format to',RightClickMenu)
        
        psdAction = QtGui.QAction('.psd', None)
        formatMenu.addAction(psdAction)
        
        tgaAction = QtGui.QAction('.tga', None)
        formatMenu.addAction(tgaAction)
        
        pngAction = QtGui.QAction('.pnj', None) 
        formatMenu.addAction(pngAction)
        
        tifAction = QtGui.QAction('.tif', None)
        formatMenu.addAction(tifAction)
        
        ddsAction = QtGui.QAction('.dds', None)
        formatMenu.addAction(ddsAction)
        
        bmpAction = QtGui.QAction('.bmp', None)
        formatMenu.addAction(bmpAction)
        
        jpgAction = QtGui.QAction('.jpg', None)
        formatMenu.addAction(jpgAction)
        
        if 'file'in type_ID:  
            #RightClickMenu.addAction(self.actionSelect_Missing_Files)
            RightClickMenu.addAction(self.actionAssign_to_Another_path)
            #RightClickMenu.addAction(self.actionChange_Format)
            RightClickMenu.addMenu(formatMenu)
            RightClickMenu.addAction(self.actionRename_File)
        if 'path' in type_ID:
            RightClickMenu.addAction(self.actionSelect_Textures_Inside)
            RightClickMenu.addAction(self.actionSelect_Missing_Files)
            RightClickMenu.addAction(self.actionAssign_to_Another_path)
            #RightClickMenu.addAction(self.actionChange_Format)
            RightClickMenu.addMenu(formatMenu)
            RightClickMenu.addAction(self.actionRename_File)
            
        psdAction.triggered.connect(functools.partial(self.changeFormatType,'.psd'))
        tgaAction.triggered.connect(functools.partial(self.changeFormatType,'.tga'))
        tifAction.triggered.connect(functools.partial(self.changeFormatType,'.tif'))
        pngAction.triggered.connect(functools.partial(self.changeFormatType,'.png'))
        jpgAction.triggered.connect(functools.partial(self.changeFormatType,'.jpg'))
        jpgAction.triggered.connect(functools.partial(self.changeFormatType,'.jpg'))
        ddsAction.triggered.connect(functools.partial(self.changeFormatType,'.dds')) 
            
        RightClickMenu.exec_(QtGui.QCursor.pos())
        
    def assigntoAnotherDir(self):
        if not self.treeViewResult.selectedIndexes():
            QtGui.QMessageBox.warning(self,'Select Files to redirect location','Please select files you need to redirect location! Thanks',QtGui.QMessageBox.Ok)
        else: 
            dirfile = os.path.split(cmds.file(q = True, sn = True))[0]
            returnfromDialog = QtGui.QFileDialog.getOpenFileNames(self,'Select a new location for files',dirfile)
            dir = os.path.split(str(returnfromDialog[0]))[0]
            for i in self.treeViewResult.selectedIndexes():
                mappedI = self._filterProxyModel.mapToSource(i)
                item = mappedI.internalPointer()
                if item.node() == 'path':
                    childCount = item.childCount()
                    for id in range(childCount):
                        try:
                            idx = self._model.index(id, 1, mappedI)
                            itemx = idx.internalPointer()
                            cmds.setAttr(itemx.data(4) + '.fileTextureName', dir + '/' + itemx.data(1).strip(), type = 'string')
                        except:
                            pass
                if item.node() == 'file':
                    cmds.setAttr(item.data(4) + '.fileTextureName', dir + '/' + item.data(1).strip(), type = 'string')
            self.analyzeScene()
    
    def changeFormatType(self, formatType):
        if not self.treeViewResult.selectedIndexes():
            QtGui.QMessageBox.warning(self,'Select Files to redirect location','Please select files you need to redirect location! Thanks',QtGui.QMessageBox.Ok)
        else: 
            for i in self.treeViewResult.selectedIndexes():
                mappedI = self._filterProxyModel.mapToSource(i)
                item = mappedI.internalPointer()
                parent = item.parent().data(1)
                if item.node() == 'file':
                    cmds.setAttr(item.data(4) + '.fileTextureName', parent + '/' + item.data(1).split('.')[0].strip() +  formatType, type = 'string')
        self.analyzeScene()
        
#     def selectAllMissingFiles(self):
#         numPath = self._model.rootItem.childCount()
#         selectModel = self.treeViewResult.selectionModel()
#         for i in range(numPath):
#             pathID = self._model.index(i, 1, self._model.rootIndex)
#             num = pathID.internalPointer().childCount()   
#             for id in range(num):
#                 idx = self._model.index(id, 1, pathID)
#                 status = idx.internalPointer().data(0)
#                 if status == False:
#                     mappedIdx = self._filterProxyModel.mapFromSource(idx)
#                     selectModel.select(mappedIdx, selectModel.Select|selectModel.Rows)
        
    def changeTextureFiles(self):
        print '-- execute'
        oldname = str(self.ldtOldName.text())
        newname = str(self.ldtNewName.text())
        if not self.treeViewResult.selectedIndexes():
             QtGui.QMessageBox.warning(self,'Select Files to change format','Please select files you need to change format! Thanks',QtGui.QMessageBox.Ok)
        else:
            for i in self.treeViewResult.selectedIndexes():
                mappedI = self._filterProxyModel.mapToSource(i)
                item = mappedI.internalPointer()
                if item.node() == 'file':
                    oldName = item.data(1)
                    newName = oldName.replace(oldname, newname).strip()
                    parent = item.parent().data(1)
                    fileNode = item.data(4)
                    cmds.setAttr(fileNode + '.fileTextureName',parent + '/' + newName,type='string')
        self.analyzeScene()    
        
def main():
    form = RecoverFiles()
    return form

    
    
    
    

    

