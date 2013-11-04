import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/RecoverFiles.ui'

form_class, base_class = uic.loadUiType(dirUI)        

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
        self.tableWidgetResult.setHorizontalHeaderLabels(['Status','Name','Location','Node'])
        #self.tableWidgetResult.setColumnHidden(2, True) 
        self.tableWidgetResult.setColumnHidden(3, True) 
        
    def analyzeScene(self):
        self.tableWidgetResult.clearContents()
        row = 0
        files = cmds.ls(typ = ['file','psdFileTex','mentalrayTexture'])
        self.tableWidgetResult.setRowCount(len(files))
        for f in files:
            fullpath = cmds.getAttr(f + '.fileTextureName')
            filename = os.path.split(fullpath)[1]
            FileName = QtGui.QTableWidgetItem(filename,QtGui.QTableWidgetItem.Type)
            FileLocation = QtGui.QTableWidgetItem(fullpath,QtGui.QTableWidgetItem.Type)
            FileNode = QtGui.QTableWidgetItem(f,QtGui.QTableWidgetItem.Type)
            FileStatus = QtGui.QTableWidgetItem(QtGui.QTableWidgetItem.UserType)
            if os.path.isfile(fullpath):
                FileStatus.setText('Found')
                FileStatus.setTextColor(QtGui.QColor(0,255,0,255))
            else:
                FileStatus.setText('Missing')
                FileStatus.setTextColor(QtGui.QColor(255,0,0,255))
            self.tableWidgetResult.setItem(row,0,FileStatus)
            self.tableWidgetResult.setItem(row,1,FileName)
            self.tableWidgetResult.setItem(row,2,FileLocation)
            self.tableWidgetResult.setItem(row,3,FileNode)
            row += 1
        self.tableWidgetResult.show()
           
    def on_tableWidgetResult_cellClicked(self,row,column):
        files = cmds.ls(typ = ['file','psdFileTex','mentalrayTexture'])
        for file in files:
            path = cmds.getAttr(file + '.fileTextureName')
            itemSelected = self.tableWidgetResult.item(row,2)
            if itemSelected.text() == path:
                cmds.select(file)
                self.signalChangeTexture.emit(path)
                break
            
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
#        row = self.tableWidgetResult.rowCount()
#        for i in range(row):
#            self.tableWidgetResult.setRowHidden(i,False)
#            filter = self.tableWidgetResult.item(i,0)
#            filtertext = str(filter.text())
#            if self.cbbFilter.currentText() == 'All':
#                self.tableWidgetResult.setRowHidden(i,False)
#            else:
#                if filtertext == self.cbbFilter.currentText():
#                    self.tableWidgetResult.setRowHidden(i,False)
#                else:
#                    self.tableWidgetResult.setRowHidden(i,True)
        status = self.cbbFilter.currentText()
        type = self.cbbFileFormat.currentText()
        self.reloadTableWidgetResult(status, type)
    
    def updateFormat(self):
#        row = self.tableWidgetResult.rowCount()
#        for i in range(row):
#            self.tableWidgetResult.setRowHidden(i,False)
#            filter = self.tableWidgetResult.item(i,0)
#            filtertext = str(filter.text())
#            if self.cbbFilter.currentText() == 'All':
#                self.tableWidgetResult.setRowHidden(i,False)
#            else:
#                if filtertext == self.cbbFilter.currentText():
#                    self.tableWidgetResult.setRowHidden(i,False)
#                else:
#                    self.tableWidgetResult.setRowHidden(i,True)
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
        
def main():
    form = RecoverFiles()
    return form

    
    
    
    

    

