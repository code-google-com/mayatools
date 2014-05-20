import maya.cmds as cmds

from PyQt4 import QtGui, QtCore, uic

import os,re

import socket,inspect 

filedir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
UIDir = filedir + "/UI/libraryTexturesUI.ui"
try:
    form_class, base_class = uic.loadUiType(UIDir)
except IOError:
    print (UIDir + ' not found.')

class LibTextureUi(form_class, base_class):
    def __init__(self,ProjectName,AssetDir):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Asset Projects: ' + ProjectName)
        self.TypeContent = list()
        self.FileType = list()
        self.IconSize = list()
        #-----------------------------------
        self.TextureType = list()
        self.ShaderType = list()
        self.ScriptType = list()
        self.ModelType = list()
        self.ActionType = list()
        #-----------------------------------
        self.ShowData = list()
        self.filterdata = list()
        
        self.TypeContent.append('TEXTURES')
        self.TypeContent.append('ACTIONS') 
        self.TypeContent.append('SHADERS')
        self.TypeContent.append('SCRIPTS')
        self.TypeContent.append('MODELS')
        self.TypeContent.append('ALL CONTENTS')
        #-------------------------------
       
        self.IconSize.append('128x128')
        self.IconSize.append('64x64')
        self.IconSize.append('32x32')
        self.IconSize.append('16x16')
        #-------------------------------
        self.TextureType.append('.psd')
        self.TextureType.append('.tga')
        self.TextureType.append('.jpg')
        self.TextureType.append('.png')
        self.TextureType.append('.bmp')
        self.TextureType.append('.tiff')
        self.TextureType.append('.*')
        #-------------------------------
        self.ShaderType.append('.hlsl')
        #-------------------------------
        self.ScriptType.append('.ms')
        self.ScriptType.append('.mel')
        self.ScriptType.append('.py')
        #-------------------------------
        self.ModelType.append('.max')
        self.ModelType.append('.ma')
        self.ModelType.append('.mb')
        self.ModelType.append('.ztl')
        #-------------------------------
        self.ActionType.append('.atn')
        #-------------------------------
        
        self.modelList = QtGui.QStringListModel(self.TypeContent)
        self.modeliconSize = QtGui.QStringListModel(self.IconSize)
        self.modelContentList = QtGui.QStringListModel(self.TextureType)
       
        #-------------------------------
        self.cbbiconList.setModel(self.modelList)
        self.cbbiconSize.setModel(self.modeliconSize)
        self.cbbiconContentList.setModel(self.modelContentList)
        
        #-------------show data on TreeWidget----------------------------
        self.model = QtGui.QFileSystemModel() 
#        self.model.setFilter(QtCore.QDir.Dirs)
        self.model.setRootPath(AssetDir)
        #----------------------------------------------------------------
        
        self.treeViewPath.setModel(self.model)
        self.treeViewPath.setRootIndex(self.model.index(AssetDir))
        self.treeViewPath.hideColumn(1)
        self.treeViewPath.hideColumn(2)
        self.treeViewPath.hideColumn(3)
        self.treeViewPath.hideColumn(4)
        
        self.listView.setModel(self.model)
        self.listView.setRootIndex(self.model.index(AssetDir))
        
        Size = QtCore.QSize(75,75)
        self.listView.setIconSize(Size)
        self.listView.setGridSize(Size)
        
        #-------------- Filter--------------------------
        self.cbbiconSize.currentIndexChanged.connect(self.updateIconSize)
#        
        #-------------- Right Click - Context Menus ------------------------------------
        self.listView.customContextMenuRequested.connect(self.createRightClickonMenu_on_selectedItems)
        self.actionMerge.triggered.connect(self.mergeFilestoMax)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionImport.triggered.connect(self.importFile)
        
    def updateIconSize(self):
        size = self.cbbiconSize.currentText()
        size = re.search('(?<=x)\w+', size)
        size = size.group(0)
        Size = QtCore.QSize(int(size)+ 30,int(size)+30)
        self.listView.setIconSize(Size)
        self.listView.setGridSize(Size)
        self.listView.update()
   
    def connectwith3dsMax(self,current):
        MAXapp = win32com.client.Dispatch('MAX.Application')
        MAXapp._FlagAsMethod('command_from_python')
        MAXapp.command_from_python('mergeMAXFile "C:/Python Project/test data/Models/{filename}'.format(filename=current.longtitle)+'"')
            
    def mergeFilestoMax(self):
        listSelecteditems = self.listView.selectedItems()
        for item in listSelecteditems:
            self.connectwith3dsMax(item)
        
    def createRightClickonMenu_on_selectedItems(self,pos):
            RightClickMenu = QtGui.QMenu(self)
            RightClickMenu.addAction(self.actionUp)
            RightClickMenu.addAction(self.actionOpen)
            RightClickMenu.addAction(self.actionImport)
            RightClickMenu.addAction(self.actionMerge)
            RightClickMenu.addAction(self.actionCopy)
            RightClickMenu.addAction(self.actionDelete)
            RightClickMenu.addAction(self.actionAssign_to_Shader)
            RightClickMenu.exec_(QtGui.QCursor.pos())
    
    def on_listView_doubleClicked(self,selectedItem):
        if os.path.isdir(str(self.model.filePath(selectedItem))):
            self.listView.setRootIndex(selectedItem)
                    
    def openFile(self):
        selectedIndexs = self.listView.selectedIndexes()
        for index in selectedIndexs:
            targetDir = str(self.model.filePath(index))
            if os.path.isdir(targetDir):
                self.listView.setRootIndex(index)
            if os.path.isfile(targetDir):
                if os.path.splitext(targetDir)[1] == '.ma':
                    cmds.file(targetDir,open = True,force=True)
    
    def importFile(self):
        selectedIndexs = self.listView.selectedIndexes()
        for index in selectedIndexs:
            targetDir = str(self.model.filePath(index))
            if os.path.isdir(targetDir):
                self.listView.setRootIndex(index)
            if os.path.isfile(targetDir):
                if os.path.splitext(targetDir)[1] == '.fbx':
                    cmds.file(targetDir,i = True,force=True)
        
    def copyFile(self):
        pass
            
                
               
         
            

        
    




        
            
            
    
        

            
        

            

       
        
