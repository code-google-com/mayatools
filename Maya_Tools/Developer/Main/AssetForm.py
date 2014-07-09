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
        
        # Dung cho du an Sony_LP1
        self.typeModel = QtGui.QStringListModel()
        self.workModel = QtGui.QStringListModel()
        #try:
        self.xmlAssetList = xml.dom.minidom.parse(self.Proj.AssetList)
        print('self.xmlAssetList: ',self.xmlAssetList)
            # Dung cho SONY_LP1
        if str(self.Proj.ProjectName)=='Sony_LP1':
                
            self.xmlNameTypeList = xml.dom.minidom.parse(self.Proj.NameTypeList)
            print('self.xmlAssetList',self.xmlAssetList)
        self.loadProjectData()
        self.resetToFileOpened()
        #except:
            #print 'Cannot locate asset list'
            
        self.currentAsset = ''
        self.currentGroup = ''
        
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
        
        self.btnToClient.clicked.connect(self.copyToClient)
        
        userID = getpass.getuser()
        if userID not in self.Proj.Technical() + self.Proj.Producer() + self.Proj.Art():
            #self.btnCreateServerFolders.setEnabled(False)
            #self.server.setEnabled(False)
            self.btnToClient.setEnabled(False)
        
        #if userID not in self.Proj.Technical():
            #self.btnToClient.setEnabled(False)
            
     #------------------Return Value of cbbAssets (THO THEM VAO)----------
    def returnAssetValue(self):
        var=''
        var = str(self.cbbAssets.currentText())
        return var 
    def retrunGroupValue(self):
        var =''
        
        var = str(self.cbbGroup.currentText())
        return var
    def copyToClient(self):
        print'--------------------------------------'
        assetValue = self.returnAssetValue()
        print('Asset Value: ',assetValue)
        groupValue = self.retrunGroupValue()
        print('Group Value:',groupValue)
        #--------- Duong dan server:
        group = str(self.cbbGroup.currentText())
        item = str(self.cbbAssets.currentText())
        type = str(self.cbbType.currentText())
        lod = str(self.cbbWorkingStage.currentText())
        # DUONG DAN LAY FILE TU SERVER:
        if lod == 'Not Available':
            if type == '':
                serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath.rstrip()# + str(type) + '/'# + str(lod)
                print('server Path:',serverPath)
            else:
                serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/'# + str(lod)
                
        else:
            serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/' + str(lod)
        # DUONG DAN COPY TOI:
        copyTo = self.Proj.ServerPath + 'To_Client'+ '/' + 'Today/'
        print('Copy To:', copyTo)
        #___________________________ BEGINNING COPY TO CLIENT____________________
        
        charToClientFolder = copyTo + assetValue
        if not os.path.exists(charToClientFolder):
            os.makedirs(str(charToClientFolder))
            
        #Access to folder on server
        charPath = serverPath
        print charPath
        if os.path.dirname(str(charPath)):
            fileNames = os.listdir(charPath)
            for fileName in fileNames:
                mayaFile = charPath +"/" + fileName
                #NEU LA FILE THI COPY FILE
                if os.path.isfile(str(mayaFile)):
                    nameMayaFile = mayaFile.split('/')[-1]
                    print('name Maya File:',nameMayaFile)
                    #nameMayaFile = nameMayaFile.split('.')[0]
                    if nameMayaFile == assetValue +'.mb':
                        print('Copy File',str(mayaFile))
                        shutil.copy(str(mayaFile), str(charToClientFolder))
                            
                # NEU LA THU MUC THI COPY FILE TRONG THU MUC
                if os.path.isdir(str(mayaFile)):
                    # Neu la Thu muc Textures:
                    folderName = mayaFile.split('/')[-1]
                    if folderName == 'Textures':
                        charToClientTexture = charToClientFolder +'/' + folderName
                        print('charToClientTexture: ',charToClientTexture)
                        if not os.path.exists(charToClientTexture):
                            os.makedirs(str(charToClientTexture))
                            
                        textureFolder =   charPath +  folderName + '/'
                        print('Texture folder: ',str(textureFolder))
                        textureFiles = os.listdir(textureFolder)
                        for textureFile in textureFiles:
                            textureFileName = textureFolder + textureFile
                            print('file texture:',str(textureFileName))
                            psdFile = textureFileName.split('/')[-1]
                            print('psd file: ',str(psdFile))
                            if psdFile == 'tex_'+assetValue+'_d01.png' or psdFile == 'tex_'+assetValue+'_d01.psd' or psdFile == 'tex_'+assetValue+'_d01_b.png' or psdFile == 'tex_'+assetValue+'_d01_b.psd':
                                print('Ban dang copy texture file:',str(psdFile))
                                shutil.copy(str(textureFileName), str(charToClientTexture))
                            #else:
                                #QtGui.QMessageBox.critical(None,'Ten Texture sai ','Ten Texture sai: '+str(psdFile) +', Vui long sua lai ten Texture: '+str('char_' + assetValue +'_texture'),QtGui.QMessageBox.Ok)
        QtGui.QMessageBox.critical(None,'Copy window ','Copy Done',QtGui.QMessageBox.Ok)

    #############___________________________END______________________
    
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
        if str(self.Proj.ProjectName) == "Sony_LP1":
            serverPath = self.Proj.ServerPath + group +'/'+ item
        
        elif str(self.Proj.ProjectName) == "Saber_Halo2":
            serverPath = self.Proj.ServerPath + group +'/'+ item
        
        else: #str(self.Proj.ProjectName) != "Sony_LP1":
            if lod == 'Not Available':
                if type == '':
                    serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath.rstrip()# + str(type) + '/'# + str(lod)
                else:
                    serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/'# + str(lod)
            else:
                serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + str(type) + '/' + str(lod)
        serverPath = serverPath.replace('/','\\')
        os.startfile(serverPath)
        
    def openLocalFolder(self):
        print "Project Name: " +self.Proj.ProjectName
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        type = self.cbbType.currentText()
        lod = self.cbbWorkingStage.currentText()
        if str(self.Proj.ProjectName) == "Sony_LP1":
            localPath = self.Proj.LocalPath + type +'/'+ lod +'/'+'Model'
        
        elif str(self.Proj.ProjectName) == "Saber_Halo2":
            localPath = self.Proj.LocalPath + group +'/' + item
        
        else: #str(self.Proj.ProjectName) != "Sony_LP1" and str(self.Proj.ProjectName) != "Saber_Halo2":
            if self.Proj.group == False:
                if lod == 'Not Available':
                    if self.Proj.ProjectLocalPath == ' ':
                        localPath = self.Proj.LocalPath + str(item) + '/'## + str(lod)
                    else:
                        localPath = self.Proj.LocalPath + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/'## + str(lod)
                else:
                    if self.Proj.ProjectLocalPath == ' ':
                        localPath = self.Proj.LocalPath + str(item) + '/'
                    else:
                        localPath = self.Proj.LocalPath + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/' + str(lod)
            else:
                if lod == 'Not Available':
                    if self.Proj.ProjectLocalPath == ' ':
                        localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/'## + str(lod)
                    else:
                        localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/'## + str(lod)
                else:
                    if self.Proj.ProjectLocalPath == ' ':
                        localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/'## + str(lod)
                    else:
                        localPath = self.Proj.LocalPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/' + str(lod)
               
        
        os.startfile(localPath)
        
    def createLocal(self):
        localFolder = ''
        group = self.cbbGroup.currentText()
        type = self.cbbType.currentText()
        working = self.cbbWorkingStage.currentText()
        
        item = self.cbbAssets.currentText()
        templateFile = os.path.split(fileDirCommmon)[0] + '/Project/' + self.Proj.ProjectName + '/' + self.Proj.templateFile
        #print 'template File'
        #print templateFile
        print('Local Folder:',self.Proj.structureFolders)
        print('Project Name:',str(self.Proj.ProjectName))
        
        if str(self.Proj.ProjectName) == "Sony_LP1":
                localFolder = self.Proj.LocalPath +  '/' + type +'/'+ working +'/'+ 'Model'
                textureFolder = localFolder + '/'+'Textures'
                workFolder = localFolder +'/'+'Workfiles'
                print('Thu muc:',str(localFolder))
                if not os.path.exists(localFolder):
                    os.makedirs(str(localFolder))
                if not os.path.exists(textureFolder):
                    os.makedirs(str(textureFolder))  
                if not os.path.exists(workFolder):
                    os.makedirs(str(workFolder))  
        
        if str(self.Proj.ProjectName) == "Saber_Halo2":
            localitem = self.Proj.LocalPath + group + '/'+ item
            sourceimages = self.Proj.LocalPath + group+'/' +'sourceimages'
            if not os.path.exists(localitem):
                os.makedirs(str(localitem))
            if not os.path.exists(sourceimages):
                os.makedirs(str(sourceimages))
              
        if str(self.Proj.ProjectName) != "Sony_LP1":
            for i in range(len(self.Proj.structureFolders)):
                
                if self.Proj.group == False:
                    localFolder = self.Proj.LocalPath + str(item) + '\\' + self.Proj.structureFolders[i]
                else:
                    localFolder = self.Proj.LocalPath + str(group) + '\\' + str(item) + '\\' + self.Proj.structureFolders[i]
                    print('localFolder: ',localFolder)
                
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
        print'BAT DAU TAO FOLEDER'
        serverFolder = ''
        group = self.cbbGroup.currentText()
        assets = list(self.cbbAssets.model().stringList())
        #templateFile = os.path.split(fileDirCommmon)[0] + '/Project/' + self.Proj.ProjectName + '/' + self.Proj.templateFile
        if str(self.Proj.ProjectName) == "Sony_LP1":
            # Tao folder tren scenes:
            for asset in assets:
                serverFolder = self.Proj.ServerPath + str(group) + '/' + str(asset) 
                modelFolder = serverFolder +'/'+ 'Model'
                textureFolder = modelFolder + '/'+'Textures'
                workFolder = modelFolder +'/'+'Workfiles'
                
                if not os.path.exists(serverFolder):
                    os.makedirs(str(serverFolder))
                if not os.path.exists(modelFolder):
                    os.makedirs(str(modelFolder))  
                if not os.path.exists(textureFolder):
                    os.makedirs(str(textureFolder)) 
                if not os.path.exists(workFolder):
                    os.makedirs(str(workFolder))
                '''  
                print('server Folder:',serverFolder)
                print('modelFolder:',modelFolder)
                print('textureFolder:',textureFolder)
                print('workFolder:',workFolder)
                '''
            # TAO FOLDER TREN FEEDBACK:
            for asset in assets:
                feedbackFolder_Ge = self.Proj.FeedbacksPath +'/'+'From_GE'+'/'+ str(group) + '/' + str(asset)
                feedbackFolder_Client = self.Proj.FeedbacksPath +'/' + 'From_Client'+'/'+ str(group) + '/' + str(asset) 
                print('feedbackFolder',feedbackFolder_Ge)
                print('feedbackFolder_Client',feedbackFolder_Client)
                if not os.path.exists(feedbackFolder_Ge):
                    os.makedirs(str(feedbackFolder_Ge))
                if not os.path.exists(feedbackFolder_Client):
                    os.makedirs(str(feedbackFolder_Client))
        if str(self.Proj.ProjectName) == "Saber_Halo2":
            # Tao folder tren scenes:
            for asset in assets:
                serverFolder = self.Proj.ServerPath + str(group) + '/' + str(asset)             
                if not os.path.exists(serverFolder):
                    os.makedirs(str(serverFolder))
                
            # TAO FOLDER TREN FEEDBACK:
            for asset in assets:
                feedbackFolder_Ge = self.Proj.FeedbacksPath +'From_GE'+ '/'+str(group) + '/' + str(asset)
                feedbackFolder_Client = self.Proj.FeedbacksPath +'From_Client'+'/'+ str(group) + '/' + str(asset) 
                print('feedbackFolder',feedbackFolder_Ge)
                print('feedbackFolder_Client',feedbackFolder_Client)
                if not os.path.exists(feedbackFolder_Ge):
                    os.makedirs(str(feedbackFolder_Ge))
                if not os.path.exists(feedbackFolder_Client):
                    os.makedirs(str(feedbackFolder_Client))
                    
        if str(self.Proj.ProjectName) != "Sony_LP1":
            for asset in assets:
                feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\'
                
                for i in range(len(self.Proj.structureFolders)):
                    serverFolder = self.Proj.ServerPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i]
                    try:
                        os.makedirs(serverFolder)
                    except:
                        pass
                    
                    try:
                                           
                        print'############################'
                        #print('self.Proj.structureProperties',self.Proj.structureProperties)
                        if len(self.Proj.structureFolders[i].split('/')) == 4:
                            print('feed back Folder',feedbackFolder)
                            if self.Proj.structureProperties==False:
                                
                                feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) 
                            else:
                                feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i].split('/')[-2] + '\\' + self.Proj.structureFolders[i].split('/')[-1] 
                            #print('feedbackFolder',feedbackFolder)
                            os.makedirs(feedbackFolder + '\\art')
                            os.makedirs(feedbackFolder + '\\tech')
                            os.makedirs(feedbackFolder + '\\client')
                        else:
                            print('feed back Folder',feedbackFolder)
                            if self.Proj.structureProperties==False:
                                
                                feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) 
                            else:
                                feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i].split('/')[-2] + '\\' + self.Proj.structureFolders[i].split('/')[-1] 
                            os.makedirs(feedbackFolder + '\\From_Art')
                            os.makedirs(feedbackFolder + '\\From_Tech')
                            os.makedirs(feedbackFolder + '\\From_Client')
                        
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
            if str(self.Proj.ProjectName) == "Sony_LP1":
                dirFile = (self.Proj.ServerPath + str(group) + '\\' + item + '\\'+'Model'+'\\').replace('\\','/')
                print('Duong dan server:',dirFile)
            if str(self.Proj.ProjectName) != "Sony_LP1":     
                dirFile = (self.Proj.ServerPath + str(group) + '\\' + dirFile + '\\').replace('\\','/')
                print('duong dan: server',dirFile)
        if self.local.isChecked():
            # Du an SONY_PL1:
            if str(self.Proj.ProjectName) == "Sony_LP1":
                dirFile = self.Proj.LocalPath +  '/' + type +'/'+ lod +'/'+ 'Model'
                
            if str(self.Proj.ProjectName) != "Sony_LP1":
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
        print('Ten du an:',str(self.Proj.ProjectName))
        print('L2:',self.Proj.L2)
        print('stages: ',self.Proj.stages)
        print('L1:',self.Proj.L1)
        print('LOD: ',self.Proj.LOD)
        if str(self.Proj.ProjectName) == 'Sony_LP1':
            self.cbbWorkingStage.addItems(self.Proj.L2)
        
        if str(self.Proj.ProjectName) != 'Sony_LP1':
            if len(self.Proj.stages) == 0:
                self.cbbWorkingStage.addItems(['Not Available'])
            else:
                self.cbbWorkingStage.addItems(self.Proj.stages)
        
        if str(self.Proj.ProjectName) == 'Sony_LP1':
            self.cbbType.addItems(self.Proj.L1) 
        if str(self.Proj.ProjectName) != 'Sony_LP1':
            self.cbbType.addItems(self.Proj.LOD)                  
  
    def on_cbbType_currentIndexChanged (self, groupName):
        workList = list()
        #groupList = self.typeModel.stringList()
        root = self.xmlNameTypeList.firstChild
        #listNodes = root.getElementsByTagName(content)[0]
        nodeList = root.getElementsByTagName('folder')
        #print('Node List: ',str(nodeList.nodeName))
        for node in nodeList:
            if node.getAttribute('type')=='L1':
                if node.getAttribute('name')== groupName:
                    print('@@@@@@,',node.getAttribute('name'))
                    #subNodes = node.childNodes
                    sublist=node.getElementsByTagName('folder')
                    for subNode in sublist:
                        if subNode.getAttribute("type")=='L2':
                            workName = subNode.getAttribute('name')
                            workList.append(workName)
        self.workModel.setStringList(sorted(workList))
        self.cbbWorkingStage.setModel(self.workModel) 
        
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
        type = self.cbbType.currentText()
        work = self.cbbWorkingStage.currentText()
        if str(self.Proj.ProjectName) == "Sony_LP1":
            localPath = self.Proj.LocalPath + str(type) + '/' + str(work)
        if str(self.Proj.ProjectName) != "Sony_LP1":
            if self.Proj.group:
                #print 'Group is True'
                localPath = self.Proj.LocalPath + str(group) + '/' + str(item)
                #serverPath = self.Proj.ServerPath + str(group)+ '/' + str(item)
            else:
                #print 'Group is False'
                localPath = self.Proj.LocalPath + str(item)
            #serverPath = self.Proj.ServerPath + str(item)
        serverPath = self.Proj.ServerPath + str(group)+ '/' + str(item)
        print('AlternativePath',self.Proj.AlternativePath)
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




        

    
                
            
        
                
            
            
        
                    
        
            
                
        
            
                  
             
        
            
               
            
                
    

        

                
