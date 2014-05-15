import maya.cmds as cmds
import maya.mel as mel
import os, sys, re, inspect , imp, shutil
from pymel.core import *
from PyQt4 import QtGui, QtCore, uic
import sip
from xml.dom.minidom import *
import maya.OpenMayaUI as OpenMayaUI
import getpass

import CommonFunctions as cf

try:
    reload(UploadForm)
except:
    import UploadForm 
    
try:
    reload(LibTextureUi)
except:
    import LibTextureUi 
    
try:
    reload(ProjectBaseClass)
except:
    from ProjectBaseClass import *
    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/AssetForm.ui'

try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def loadModule(moduleName):
    sys.path.append(fileDirCommmon + '/MODULE/' + moduleName)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()
    
class AssetForm(form_class,base_class):
    def __init__(self, XMLProject, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('ProjectUIWindow')
        self.Proj = ProjectBaseClass(XMLProject)
        self.setWindowTitle(self.Proj.ProjectName)
        self.assetGroupModel = QtGui.QStringListModel()
        self.assetListModel = QtGui.QStringListModel()
        try:
            self.xmlAssetList = xml.dom.minidom.parse(self.Proj.AssetList)
            self.loadProjectData()
            self.resetToFileOpened()
        except:
            print 'Cannot locate asset list'
            
        self.currentAsset = ''
        self.currentGroup = ''
        self.currentLOD = ''
        self.currentStage = ''
        
        #-------------- FUNCTION UI
        self.btnCreateLocalFolders.clicked.connect(self.createLocal)
        self.btnCreateServerFolders.clicked.connect(self.createServer)
        self.btnOpenLocalFolder.clicked.connect(self.openLocalFolder)
        self.btnOpenServerFolder.clicked.connect(self.openServerFolder)
        self.btnOpenfile.clicked.connect(self.openMayafile)
        self.btnFeedbacks.clicked.connect(self.openFeedbacksFolder)
        self.btnOpenDocuments.clicked.connect(self.openDocumentsFolder)
        self.btnSaveIncrement.clicked.connect(cf.saveFileIncrement)
        self.btnUploadandDownload.clicked.connect(self.syncFileWithServer)
        self.cbbAssets.currentIndexChanged.connect(self.updateCurrentAsset)
        self.cbbGroup.currentIndexChanged.connect(self.updateCurrentAsset)
        
        userID = getpass.getuser()
        if userID not in self.Proj.Technical() + self.Proj.Producer() + self.Proj.Art():
            self.btnCreateServerFolders.setEnabled(False)
            self.server.setEnabled(False)
        
        if userID not in self.Proj.Technical():
            self.btnToClient.setEnabled(False)
            
    def updateCurrentAsset(self):
        self.currentAsset = str(self.cbbAssets.currentText())
        self.currentGroup = str(self.cbbGroup.currentText())
        
    def openFeedbacksFolder(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        lod = self.cbbType.currentText()
        stage = self.cbbWorkingStage.currentText()
        if stage =='Not Available':
            dirFile = self.Proj.FeedbacksPath +'/'+ str(group) + '/' + str(item)
            print dirFile
        else:
            dirFile = self.Proj.FeedbacksPath + str(group) + '/' + str(item) + '/' + str(lod) + '/' + str(stage)
        if not os.path.isdir(dirFile):
            dirFile = self.Proj.FeedbacksPath
        dirFile = dirFile.replace('/','\\')
        os.startfile(dirFile)
   
    def openDocumentsFolder(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        dirFile = self.Proj.ReferencesImagePath + str(group) + '/' + str(item) + '/'
        if not os.path.isdir(dirFile):
            dirFile = self.Proj.ReferencesImagePath + str(group) + '/' 
            if not os.path.isdir(dirFile):
                dirFile = self.Proj.ReferencesImagePath
        os.startfile(dirFile.replace('/','\\'))

    def openServerFolder(self):
        group = str(self.cbbGroup.currentText())
        item = str(self.cbbAssets.currentText())
        type = str(self.cbbType.currentText())
        lod = str(self.cbbWorkingStage.currentText())
        if lod == 'Not Available':
            if type == '':
                serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath.rstrip()
            else:
                serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/'
        else:
            serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/' + str(lod)
        serverPath = serverPath.replace('/','\\')
        os.startfile(serverPath)
        
    def openLocalFolder(self):
        print "Project Local: " +self.Proj.ProjectLocalPath
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        type = self.cbbType.currentText()
        lod = self.cbbWorkingStage.currentText()
        if self.Proj.group == False:
            if lod == 'Not Available':
                if self.Proj.ProjectLocalPath == ' ':
                    localPath = self.Proj.LocalPath + str(item) + '/'
                else:
                    localPath = self.Proj.LocalPath + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/'
            else:
                if self.Proj.ProjectLocalPath == ' ':
                    localPath = self.Proj.LocalPath + str(item) + '/'
                else:
                    localPath = self.Proj.LocalPath + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/' + str(lod)
        else:
            if lod == 'Not Available':
                if self.Proj.ProjectLocalPath == ' ':
                    localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/'
                else:
                    localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/'
            else:
                localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/' + str(lod)    
        os.startfile(localPath)
        
    def createLocal(self):
        localFolder = ''
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        templateFile = os.path.split(fileDirCommmon)[0] + '/Project/' + self.Proj.ProjectName + '/' + self.Proj.templateFile
        for i in range(len(self.Proj.structureFolders)):
            if self.Proj.group == False:
                localFolder = self.Proj.LocalPath + str(item) + '\\' + self.Proj.structureFolders[i]
            else:
                localFolder = self.Proj.LocalPath + str(group) + '\\' + str(item) + '\\' + self.Proj.structureFolders[i]
            try:
                os.makedirs(localFolder)
            except:
                pass
            if self.Proj.placeFileAndName[i] != '':
                try:
                    shutil.copyfile(templateFile,(localFolder + '\\' + str(item) +  self.Proj.placeFileAndName[i]))
                except:
                    pass
                
    def createServer(self):
        serverFolder = ''
        group = self.cbbGroup.currentText()
        assets = list(self.cbbAssets.model().stringList())
        for asset in assets:
            feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\'
            for i in range(len(self.Proj.structureFolders)):
                serverFolder = self.Proj.ServerPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i]
                try:
                    os.makedirs(serverFolder)
                except:
                    pass
                try:
                    if len(self.Proj.structureFolders[i].split('/')) == 4:
                        feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i].split('/')[-2] + '\\' + self.Proj.structureFolders[i].split('/')[-1] 
                        os.makedirs(feedbackFolder + '\\art')
                        os.makedirs(feedbackFolder + '\\tech')
                        os.makedirs(feedbackFolder + '\\client')
                except:
                    pass
                if self.Proj.placeFileAndName[i] != '':
                    try:
                        shutil.copyfile(templateFile,(serverFolder + '\\' + str(asset) +  self.Proj.placeFileAndName[i]))
                    except:
                        pass
            
    def openMayafile(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        type = self.cbbType.currentText()
        lod = self.cbbWorkingStage.currentText()
        if str(type) =='':
            dirFile = str(item) 
            print('duong dan local__:',dirFile)
        else:
            dirFile = str(item) + '\\' + self.Proj.ProjectLocalPath + str(type)
        print('ProjectLocal',self.Proj.ProjectLocalPath)
        if str(self.cbbWorkingStage.currentText()) != 'Not Available':
            dirFile += '\\' + str(lod) 
            print' duong dan Mya'
            print dirFile
        else:
            print 'Duong dan Maya File'
            print dirFile
            
        if self.server.isChecked():
            dirFile = (self.Proj.ServerPath + str(group) + '\\' + dirFile + '\\').replace('\\','/')
            print('duong dan: server',dirFile)
        if self.local.isChecked():
            if self.Proj.group:
                dirFile = (self.Proj.LocalPath + str(group) + '\\' + dirFile + '\\').replace('\\','/')
                print('duong dan: local1',dirFile)
            else:
                dirFile = self.Proj.LocalPath + dirFile
                print('duong dan: local',dirFile)
        if self.vLast.isChecked():
            try:
                filename = ''
                if str(self.cbbWorkingStage.currentText()) !='Not Available':
                    filename = dirFile + '\\' + str(item) + '_' + str(self.cbbType.currentText()) + '_' + str(self.cbbWorkingStage.currentText()) + '_vLast.mb'
                else:
                    filename = dirFile + '\\' + str(item) + '_' + str(self.cbbType.currentText()) + '_vLast.mb'
                cmds.file(filename, f = True, o = True)
            except:
                QtGui.QMessageBox.information(self,'Error','Khong mo duoc file Vlast. Vui long mo bang any version',QtGui.QMessageBox.Ok)
        else:
            dirFile = dirFile.replace('/','\\')
            filename = QtGui.QFileDialog.getOpenFileNames(self, 'Open File', dirFile)
            try:
                ftype = ''
                cmds.file(str(filename[0]), f = True, o = True)
                if os.path.splitext(str(filename[0]))[1] == '.mb':
                    ftype = 'mayaBinary'
                if os.path.splitext(str(filename[0]))[1] == '.ma':
                    ftype = 'mayaAscii'
                print ftype
                mel.eval('addRecentFile("{fileName}","{fileType}")'.format(fileName = filename[0].replace('\\','/'), fileType = ftype))
            except RuntimeError:
                pass
        
    def loadProjectData(self):
        stringList = list()
        rootNode= self.xmlAssetList.firstChild
        assetNodes = rootNode.getElementsByTagName('asset')
        groupNodes = rootNode.getElementsByTagName('group')
        for group in groupNodes:
            name = group.getAttribute('name')
            stringList.append(name)
        self.assetGroupModel.setStringList(stringList)
        self.cbbGroup.setModel(self.assetGroupModel)
        if len(self.Proj.stages) == 0:
            self.cbbWorkingStage.addItems(['Not Available'])
        else:
            self.cbbWorkingStage.addItems(self.Proj.stages) 
        self.cbbType.addItems(self.Proj.LOD)   
        
    def updateAssetStatus(self):             
  
    def on_cbbGroup_currentIndexChanged (self, groupName):
        assetList = list()
        groupList = self.assetGroupModel.stringList()
        groupNodes = self.xmlAssetList.getElementsByTagName('group')
        for i in range(len(groupList)):
            if groupList[i] == groupName:
                assetNodes = groupNodes[i].getElementsByTagName('asset')
                for asset in assetNodes:
                    assetName = asset.getAttribute('name')
                    assetList.append(assetName)
        self.assetListModel.setStringList(sorted(assetList))
        self.cbbAssets.setModel(self.assetListModel)
        
    def syncFileWithServer(self):
        #currentFile = cmds.file(q = True, n = True)
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        if self.Proj.group:
            #print 'Group is True'
            localPath = self.Proj.LocalPath + str(group) + '/' + str(item)
            #serverPath = self.Proj.ServerPath + str(group)+ '/' + str(item)
        else:
            #print 'Group is False'
            localPath = self.Proj.LocalPath + str(item)
            #serverPath = self.Proj.ServerPath + str(item)
        serverPath = self.Proj.ServerPath + str(group)+ '/' + str(item)
        syncForm = UploadForm.UploadForm(localPath, serverPath, self.Proj.AlternativePath)
        syncForm.show()
        
    def validateCurrentFile(self):
        fileName = cmds.file(q = True, sn = True)
        groups = self.xmlAssetList.getElementsByTagName('group')
        for g in groups:
            assets = g.getElementsByTagName('asset')
            for a in assets:
                if a.getAttribute('name') in fileName:
                    return(g.getAttribute('name'), a.getAttribute('name'))
        return(False, False)
                
    def resetToFileOpened(self):
        result = self.validateCurrentFile()
        print result
        if result != (False, False):
            self.cbbGroup.setCurrentIndex(list(self.cbbGroup.model().stringList()).index(result[0]))
            self.cbbAssets.setCurrentIndex(list(self.cbbAssets.model().stringList()).index(result[1]))




        

    
                
            
        
                
            
            
        
                    
        
            
                
        
            
                  
             
        
            
               
            
                
    

        

                
