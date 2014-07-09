import maya.cmds as cmds
import maya.mel as mel
import os, sys, re, inspect , imp, shutil
from pymel.core import *
from PyQt4 import QtGui, QtCore, uic
import sip
from xml.dom.minidom import *
import maya.OpenMayaUI as OpenMayaUI
import functools, imp
import CommonFunctions as cf

try:
    reload(ProjectBoard)
except:
    import ProjectBoard 
    
try:
    reload(LibTextureUi)
except:
    import LibTextureUi 
    
try:
    reload(ProjectBaseClass)
except:
    from ProjectBaseClass import *
    
serverPath =""
clientPath=""
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ArtLead.ui'
#fileDirXML = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
#fileDirXML = inspect.getouterframes(inspect.currentframe())[0][0]
fileDir = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
#fiel1 = os.path.abspath(os.path.join(fileDirXML, os.pardir)) #fileDirXML.split('/',-1)
customPath = os.path.split(os.path.split(os.path.split(fileDir)[0])[0])[0]

try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def loadXML(xmlFile, content):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        listNodes = root.getElementsByTagName(content)[0]
        #print listNodes
        for d in listNodes.childNodes:
            print "Notes ne pa con"
            name = d.nodeName
            print name
            if name == "folder":
                kit.append(d.getAttribute("name"))
            if name == "asset":
                kit.append(d.getAttribute("name"))
            if name == "ServerPath":
                kit.append(d.childNodes[0].data)
            if name == "LocalPath":
                kit.append(d.childNodes[0].data)               
        
        return kit
def coppyFiles(name,sourcePath,targetPath):
        if os.path.isfile(name):
            if name != 'Thumbs.db':
                shutil.copy(name,targetPath)
           
def loadModule(moduleName):
    sys.path.append(fileDirCommmon + '/MODULE/' + moduleName)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()
   
class ArtLead(form_class,base_class):
    def __init__(self,inputFile):
        super(base_class,self).__init__()
        
        self.setupUi(self)
        self.__name__ = 'Art Lead'
        self._projectName = inputFile.split('.')[0]
        fileDirXML = customPath +"/Project/"+self._projectName+"/XMLfiles/"+self._projectName+".xml"
        carXML = customPath +"/Project/"+self._projectName+"/XMLfiles/" + "AssetList.xml"
        # lay du lieu cho Group
        kits = loadXML(fileDirXML, "folder")
        for kit in kits:
            self.cbbGroup.addItem(kit)
        # Lay du lieu Cars
        cars = loadXML(carXML, "group")
        for car in cars:
            self.cbbAssets.addItem(car)
        
        # LAY THU MUC CLIENT VA SERVER
        dirPath = loadXML(fileDirXML, "Directories")
        serverPath = dirPath[0] +"Cars"
            
        clientPath = dirPath[1]+ "Cars"
        print ("client Path",clientPath)
        #clientPaht = loadXML(xmlFile, content)
        print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print self._projectName
        print inputFile
        print "FileXML"
        print fileDirXML
        print "customPath"
        print customPath
        print"Notes: ####"
        print kit
        print"Path Server: "
        print serverPath
        #self.Proj = ProjectBaseClass(XMLProject)
        #self.xmlAssetList = xml.dom.minidom.parse(self.Proj.AssetList)
        #self.loadProjectData()
        print "########################################"
        
        self.btnOpenLocalFolder.clicked.connect(functools.partial(self.openLocalFolder,clientPath))
        self.btnOpenServerFolder.clicked.connect(self.openServerFolder)
        #self.btnCopyFile.clicked.connect(self.coppyToLocal,clientPath,serverPath)
        self.btnCopyFile.clicked.connect(functools.partial(self.coppyToLocal,clientPath,serverPath))
        # PROJECT DASHBOARD
        self.btnOpenProjectBoard.clicked.connect(self.openProjectBoard)
        self.btnFeedbacks.clicked.connect(self.openFeedbacksFolder)
        self.btnOpenDocument.clicked.connect(self.openDocumentFolder)
        #self.btnSaveIncrement.clicked.connect(cf.saveFileIncrement)
        #self.btnUploadandDownload.clicked.connect(self.syncFileWithServer)
                
    
    def coppyToLocal(self,clientPath,serverPath):
        CarName =str(self.cbbAssets.currentText())
        clientPath = clientPath + "/" + CarName
        serverPathL0 = serverPath +"/"+ CarName
        print"In ra truoc"
        print("Server L0",serverPathL0)
        if not os.path.exists(serverPathL0):
            print "files khong ton tai!"
                    
        if not os.path.exists(clientPath):
            print "Tao local Folder:"
            os.makedirs(clientPath)
        names = os.listdir(serverPathL0)
        for name in names:
            filePath = serverPathL0 + "/" + name
            if os.path.isfile(filePath):
                print("ten file: ",filePath)
                #coppyFiles(name,serverPath,clientPath)
                if sub != 'Thumbs.db':
                    shutil.copy(filePath,clientPath) 
                
            serverPathL1 = serverPathL0 + "/" + name
            #print("Server L1",serverPathL1)
            if os.path.isdir(serverPathL1):
                temClientPath = os.path.join(clientPath,name)
                subfiles = os.listdir(serverPathL1)
                if not os.path.exists(temClientPath):
                    os.makedirs(temClientPath)
                # LAY FILE TRONG THU MUC XE
                for su in subfiles:
                    filePath_su = serverPathL1 + "/" + su
                    if os.path.isfile(filePath_su):
                        #print("ten file: ",filePath_su)
                        #coppyFiles(filePath_su,serverPath,temClientPath)
                        if sub != 'Thumbs.db':
                            shutil.copy(filePath_su,temClientPath)      
                    serverPathL2 = serverPathL1+"/"+su
                    print("Server L2",serverPathL2)
                    if os.path.isdir(serverPathL2):
                        tem1ClientPath = os.path.join(temClientPath,su)
                        subfiles1 = os.listdir(serverPathL2)
                        if not os.path.exists(tem1ClientPath):
                            os.makedirs(tem1ClientPath)
                # LAY FILE TRONG THU MUC MAY A
                        for sub in subfiles1:
                            filePath_sub = serverPathL2 + "/" + sub
                            if os.path.isfile(filePath_sub):
                                #print("ten1 file: ",filePath_sub)
                                #coppyFiles(filePath_sub,serverPath,tem1ClientPath)
                                if sub != 'Thumbs.db':
                                    shutil.copy(filePath_sub,tem1ClientPath)  
                            serverPathL3 = serverPathL2 + "/" + sub
                            #print("Server L3",serverPathL3)
                            if os.path.isdir(serverPathL3):
                                tem2ClientPath = os.path.join(tem1ClientPath,sub)
                                subfiles2 = os.listdir(serverPathL3)
                                if not os.path.exists(tem2ClientPath):
                                    os.makedirs(tem2ClientPath)
                # LAY FILE TRONG THU MUC CAR
                                for subb in subfiles2:
                                    filePath_subb = serverPathL3 + "/" + subb
                                    #print ("server path: ",serverPath)
                                    #print("Thu muc Car",filePath_subb)
                                    if os.path.isfile(filePath_subb):
                                        #print("ten 2 file: ",filePath_subb)
                                        if subb != 'Thumbs.db':
                                            shutil.copy(filePath_subb,tem2ClientPath)     
                                    serverPathL4 = serverPathL3 +"/" +subb
                                    #print("Server L4",serverPathL4)
                                    if os.path.isdir(serverPathL4):
                                        tem3ClientPath = os.path.join(tem2ClientPath,subb)
                                        subfiles3 = os.listdir(serverPathL4) 
                                        #print ("subfiles3: ",subfiles3)
                                        if not os.path.exists(tem3ClientPath):
                                            os.makedirs(tem3ClientPath)
                # LAY FILE TRONG THU MUC SCENES
                                        
                                        for  subbb in subfiles3:
                                            #print ("tem3ClientPath",tem3ClientPath)
                                            #print("ten3 file: ",subbb)
                                            filePath_subbb = serverPathL4 + "/" + subbb
                                            if os.path.isfile(filePath_subbb):
                                                #print("ten3 file: ",filePath_subbb)
                                                #coppyFiles(subbb,serverPath,tem3ClientPath)
                                                if subbb != 'Thumbs.db':
                                                    shutil.copy(filePath_subbb,tem3ClientPath)                
        QtGui.QMessageBox.information(self,'Copy files','Copy done',QtGui.QMessageBox.Ok)
                        
                
                                
        #else:
            #coppyFiles(serverPath,clientPath)
       
    def openProjectBoard(self):
        dashBoardForm = ProjectBoard.ProjectBoard()
        dashBoardForm.show()
    def openFeedbacksFolder(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        lod = self.cbbType.currentText()
        stage = self.cbbWorkingStage.currentText()
        if stage =='Not Available':
            print 'Feedback Path: '
            print self.Proj.FeedbacksPath
            dirFile = self.Proj.FeedbacksPath +'/'+ str(group) + '/' + str(item) #+ '/' #+ str(lod) + '/' #+ str(stage)
            print dirFile
        else:
            dirFile = self.Proj.FeedbacksPath + str(group) + '/' + str(item) + '/' + str(lod) + '/' + str(stage)
        #if not os.path.isdir(dirFile):
        #    dirFile = self.Proj.FeedbacksPath + str(group) + '/' + str(item)
        dirFile = dirFile.replace('/','\\')
        print "Thu muc file: "
        print dirFile
        os.startfile(dirFile)
        #os.startfile(dirFile.replace('/','\\'))
            
    def openDocumentFolder(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        lod = self.cbbType.currentText()
        stage = self.cbbWorkingStage.currentText()
        if stage =='Not Available':
            print 'Feedback Path: '
            print self.Proj.FeedbacksPath
            dirFile = self.Proj.DocumentsPath #+'/'+ str(group) #+ '/' + str(item) #+ '/' #+ str(lod) + '/' #+ str(stage)
            print dirFile
        else:
            dirFile = self.Proj.FeedbacksPath + str(group) + '/' + str(item) + '/' + str(lod) + '/' + str(stage)
        #if not os.path.isdir(dirFile):
        #    dirFile = self.Proj.FeedbacksPath + str(group) + '/' + str(item)
        dirFile = dirFile.replace('/','\\')
        print "Thu muc file: "
        print dirFile
        os.startfile(dirFile)
        
    def openServerFolder(self):
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        type = self.cbbType.currentText()
        lod = self.cbbWorkingStage.currentText()
        if lod == 'Not Available':
            serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/'# + str(lod)
            print serverPath
            print"Local Path"
            print self.Proj.ProjectLocalPath
        else:
            serverPath = self.Proj.ServerPath + str(group) + '/' + str(item) + '/' + self.Proj.ProjectLocalPath + '/' + str(type) + '/' + str(lod)
        serverPath = serverPath.replace('/','\\')
        os.startfile(serverPath)
        
    def openLocalFolder(self,clientPath):
        CarName =str(self.cbbAssets.currentText())
        partAsset = str(self.cbbGroup.currentText())
        print("Client ne:",clientPath)
        localPath = clientPath + "/" + CarName + "/" +"maya" + "/" + partAsset +"/"+ "scenes" + "/" + CarName+".mb"
        cmds.file(localPath, f = True, o = True)    
        #os.startfile(localPath)
        
    def createLocal(self):
        localFolder = ''
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        templateFile = os.path.split(fileDirCommmon)[0] + '/Project/' + self.Proj.ProjectName + '/' + self.Proj.templateFile
        print 'template File'
        print templateFile
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
        #templateFile = os.path.split(fileDirCommmon)[0] + '/Project/' + self.Proj.ProjectName + '/' + self.Proj.templateFile
        for asset in assets:
            feedbackFolder = self.Proj.FeedbacksPath + str(group) + '\\' + str(asset) + '\\'
            for i in range(len(self.Proj.structureFolders)):
                #print self.Proj.structureFolders[i]
                serverFolder = self.Proj.ServerPath + str(group) + '\\' + str(asset) + '\\' + self.Proj.structureFolders[i]
                #print serverFolder
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
        dirFile = str(item) + '\\' + self.Proj.ProjectLocalPath + str(type)
        if str(self.cbbWorkingStage.currentText()) != 'Not Available':
            dirFile += '\\' + str(lod) 
            print' duong dan Mya'
            print dirFile
        else:
            print 'Duong dan Maya File'
            print dirFile
            
        if self.server.isChecked():
            dirFile = (self.Proj.ServerPath + str(group) + '\\' + dirFile + '\\').replace('\\','/')
            print dirFile
        if self.local.isChecked():
            if self.Proj.group:
                dirFile = (self.Proj.LocalPath + str(group) + '\\' + dirFile + '\\').replace('\\','/')
            else:
                dirFile = self.Proj.LocalPath + dirFile
            print dirFile
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
            #print dirFile
            filename = QtGui.QFileDialog.getOpenFileNames(self, 'Open File', dirFile)
            #print filename
            try:
                cmds.file(str(filename[0]), f = True, o = True)
            except RuntimeError:
                #cmds.file(filename, o = True)
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
  
           
    def syncFileWithServer(self):
        #currentFile = cmds.file(q = True, n = True)
        group = self.cbbGroup.currentText()
        item = self.cbbAssets.currentText()
        if self.Proj.group:
            localPath = self.Proj.LocalPath + str(group) + '/' + str(item)
        else:
            localPath = self.Proj.LocalPath + str(item)
        serverPath = self.Proj.ServerPath + str(group)+ '/' + str(item)
        syncForm = UploadForm.UploadForm(localPath, serverPath)
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




        
def main(xmlFile):
    form = ArtLead(xmlFile)
    return form 
    
                
            
        
                
            
            
        
                    
        
            
                
        
            
                  
             
        
            
               
            
                
    

        

                
