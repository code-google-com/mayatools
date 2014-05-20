import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import shutil
import inspect, os, sip
import maya.OpenMayaUI as OpenMayaUI

import CommonFunctions as cf

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/UploadAsset.ui'
try:    
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found.')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def backupData(file):
    if os.path.isfile(file):
        backupFile = file.replace(os.path.splitext(file)[1],'.bak')
        if os.path.isfile(backupFile):
            os.remove(backupFile)
            os.rename(file, backupFile)
	
class UploadForm(form_class,base_class):
    def __init__(self, LocalPath, ServerPath, AlternativePath, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.showData(LocalPath, ServerPath)
        self.showdataonLocal = LocalPath
        self.showdataonServer = ServerPath
        self.showdataonAlternativePath = AlternativePath
        self.btntoServer.clicked.connect(self.toServer)
        self.btntoLocal.clicked.connect(self.toLocal)
        self.btnAlternativePath.clicked.connect(self.alternatePath)
        self.actionOpenFolder.triggered.connect(self.openFolder)
        self.actionRefFile.triggered.connect(self.referenceFile)
        self.actionImportFile.triggered.connect(self.importFile)
        self.actionOpenFile.triggered.connect(self.openFile)
        self.treeViewLocal.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
        self.treeViewServer.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
        self.treeViewLocal.clicked.connect(self.loadLocalPathInfoToQLineLocal)
        self.treeViewServer.clicked.connect(self.loadServerPathInfoToQLineServer)
        self.lineLocal.setText(LocalPath)
        self.lineServer.setText(ServerPath)
        
    def loadLocalPathInfoToQLineLocal(self):
        index = self.treeViewLocal.selectedIndexes()[0]
        filePathLocal = str(index.model().filePath(index))
        self.lineLocal.setText(filePathLocal)
        
    def loadServerPathInfoToQLineServer(self):
        index = self.treeViewServer.selectedIndexes()[0]
        filePathServer = str(index.model().filePath(index))
        self.lineServer.setText(filePathServer)
        
    def showData(self, pLocal, pServer):
        modelLocal = QtGui.QFileSystemModel()
        modelServer = QtGui.QFileSystemModel()
        
        modelLocal.setRootPath(pLocal)
        modelServer.setRootPath(pServer)
        
        self.treeViewLocal.setModel(modelLocal)
        self.treeViewLocal.setRootIndex(modelLocal.index(pLocal))
        self.treeViewLocal.hideColumn(2)
        
        self.treeViewServer.setModel(modelServer)
        self.treeViewServer.setRootIndex(modelServer.index(pServer))
        self.treeViewServer.hideColumn(2)
        
    def copyTo(self, pathSrc, pathDes):
        pass
    
    def toLocal(self):
        localIndex = list()
        serverIndex = list()
        #print self.showdataonServer
        #print self.showdataonLocal
        for index in self.treeViewServer.selectedIndexes():
            fpathServer = str(index.model().filePath(index))
            serverIndex.append(fpathServer)
            fpathLocal =  fpathServer.replace(self.showdataonServer,self.showdataonLocal)
            #print fpathLocal
            localIndex.append(fpathLocal)
        localIndex = sorted(list(set(localIndex)))
        #print localIndex
        serverIndex = sorted(list(set(serverIndex)))
        #print serverIndex
        for i in localIndex:
            cf.copytree(serverIndex[localIndex.index(i)],i)
        QtGui.QMessageBox.information(self,'Copy Asset','Copy done',QtGui.QMessageBox.Ok)
    
    def toServer(self):
        localIndex = list()
        serverIndex = list()
        for index in self.treeViewLocal.selectedIndexes():
            fpathLocal = str(index.model().filePath(index))
            localIndex.append(fpathLocal)
            fpathServer =  fpathLocal.replace(self.showdataonLocal, self.showdataonServer)
            serverIndex.append(fpathServer)
        localIndex = sorted(list(set(localIndex)))
        #print localIndex
        #print serverIndex
        serverIndex = sorted(list(set(serverIndex)))
        for i in localIndex:
            cf.copytree(i,serverIndex[localIndex.index(i)])
        QtGui.QMessageBox.information(self,'Copy Asset','Copy done',QtGui.QMessageBox.Ok)
        self.showData(self.showdataonLocal, self.showdataonServer)
                
    def openFolder(self):
        folderLocation = ''
        try:
            indexLocal = self.treeViewLocal.selectedIndexes()[0]
            folderLocation = indexLocal.model().filePath(indexLocal)
        except:
            pass
        try:
            indexServer = self.treeViewServer.selectedIndexes()[0]
            folderLocation = indexServer.model().filePath(indexServer).replace('/','\\')
        except:
            pass
        os.startfile(folderLocation)
            
    def refreshServer(self, index):
        pass
    
    def referenceFile(self):
        fileRef = ''
        try:
            indexLocal = self.treeViewLocal.selectedIndexes()[0]
            fileRef = str(indexLocal.model().filePath(indexLocal))
        except:
            pass
        try:
            indexServer = self.treeViewServer.selectedIndexes()[0]
            fileRef = str(indexServer.model().filePath(indexServer).replace('/','\\'))
        except:
            pass
        if os.path.splitext(fileRef)[1] in ['.mb','.ma','.fbx','.obj']:
            #print fileRef
            cmds.file(fileRef, r = True)
        else:
            QtGui.QMessageBox.information(self,'Wrong File Format','Khong the reference file co dinh dang {type}'.format(type = os.path.splitext(fileRef)[1]),QtGui.QMessageBox.Ok)
        
    def importFile(self):
        fileImport = ''
        try:
            indexLocal = self.treeViewLocal.selectedIndexes()[0]
            fileImport = str(indexLocal.model().filePath(indexLocal))
        except:
            pass
        try:
            indexServer = self.treeViewServer.selectedIndexes()[0]
            fileImport = str(indexServer.model().filePath(indexServer).replace('/','\\'))
        except:
            pass
        if os.path.splitext(str(fileImport))[1] in ['.mb','.ma','.fbx','.obj']:
            cmds.file(fileImport, i = True)
        else:
            QtGui.QMessageBox.information(self,'Wrong File Format','Khong the import file co dinh dang {type}'.format(type = os.path.splitext(fileImport)[1]),QtGui.QMessageBox.Ok)
            
    def openFile(self):
        fileOpen = ''
        try:
            indexLocal = self.treeViewLocal.selectedIndexes()[0]
            fileOpen = str(indexLocal.model().filePath(indexLocal))
        except:
            pass
        try:
            indexServer = self.treeViewServer.selectedIndexes()[0]
            fileOpen = str(indexServer.model().filePath(indexServer).replace('/','\\'))
        except:
            pass
        if os.path.splitext(fileOpen)[1] in ['.mb','.ma']:
            #print fileRef
            cmds.file(fileOpen, o = True, f = True)
        else:
            QtGui.QMessageBox.information(self,'Wrong File Format','Khong the reference file co dinh dang {type}'.format(type = os.path.splitext(fileOpen)[1]),QtGui.QMessageBox.Ok)

    def alternatePath(self):
        self.lineLocal.setText()
        
    def createRightClickonMenu_on_selectedItems(self,pos):
        RightClickMenu = QtGui.QMenu(self)
        RightClickMenu.addAction(self.actionRefFile)
        RightClickMenu.addAction(self.actionOpenFolder)
        RightClickMenu.addAction(self.actionOpenFile)
        RightClickMenu.addAction(self.actionImportFile)
        RightClickMenu.exec_(QtGui.QCursor.pos())

