import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import maya.mel as mel
import os, sys, inspect, re, shutil
import pymel.core as py
import pymel.core.datatypes as dt
import functools 
from xml.dom.minidom import *

PathToClient= 'T:/Scenes/FrontierWave_characters/To_Client/Today/'
PathCharacter ='T:/Scenes/FrontierWave_characters/'


import AssetForm
reload(AssetForm)


    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/CustomNamingTool.ui'

form_class, base_class = uic.loadUiType(dirUI)    

class CustomNamingTool(form_class,base_class):
    signalGet = QtCore.pyqtSignal('QString', name = 'AssetValue')
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        
        self.btnUpdateFile.clicked.connect(self.readFileText)
        self.btnPreview.clicked.connect(self.updateText)
        self.btnNext.clicked.connect(self.loadText)
        self.btnLoadKey.clicked.connect(self.loadFileTXT)
        self.btnCopyToClient.clicked.connect(self.copyToClient)
        
        
    def copyToClient(self):
        xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/FrontierWave.xml'
        ass = AssetForm.AssetForm(xmlFile)
        assetValue = ass.returnAssetValue()
        groupValue = ass.retrunGroupValue()
        
        # CHECK THU MUC CHARRACTER O TO_CLIENT NEU CHUA CO TAO MOI
        charToClientFolder = PathToClient + assetValue
        if not os.path.exists(charToClientFolder):
            os.makedirs(str(charToClientFolder))
        
        #Access to folder on server
        charPath = PathCharacter + groupValue +'/'+ assetValue +'/'
        print charPath
        if os.path.dirname(str(charPath)):
            fileNames = os.listdir(charPath)
            for fileName in fileNames:
                mayaFile = charPath +"/" + fileName
                #NEU LA FILE THI COPY FILE
                if os.path.isfile(str(mayaFile)):
                    nameMayaFile = mayaFile.split('/')[-1]
                    nameMayaFile = nameMayaFile.split('.')[0]
                    if nameMayaFile == nameMayaFile:
                        print('Copy File',str(mayaFile))
                        shutil.copy(str(mayaFile), str(charToClientFolder))
                        
                # NEU LA THU MUC THI COPY FILE TRONG THU MUC
                if os.path.isdir(str(mayaFile)):
                    # Neu la Thu muc Textures:
                    folderName = mayaFile.split('/')[-1]               
                    if folderName == 'Textures':
                        charToClientFolder = charToClientFolder +'/' + folderName
                        if not os.path.exists(charToClientFolder):
                            os.makedirs(str(charToClientFolder))
                        
                        textureFolder =   charPath +  folderName + '/'
                        print('Texture folder: ',str(textureFolder))
                        textureFiles = os.listdir(textureFolder)
                        for textureFile in textureFiles:
                            textureFileName = textureFolder + textureFile
                            print('file texture:',str(textureFileName))
                            psdFile = textureFileName.split('/')[-1]
                            print('psd file: ',str(psdFile))
                            if psdFile == 'char_'+assetValue+'_Texture.psd':
                                print('Ban dang copy texture file:',str(psdFile))
                                shutil.copy(str(textureFileName), str(charToClientFolder))
            
        
    def readFileText(self):
        fileNameTXT = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.txt'
        #folderName = os.path.split(cmds.file(q= True, sn = True))[0]
        #print('Ten folder la:',fileNameTXT)
        if os.path.isfile(fileNameTXT):
            textFile = open(fileNameTXT,'r')
        else:
            print"Khong co file"
    
    def loadFileTXT(self):
        #textFile = os.open(fileTXT,os.O_RDWR)
        fileNameTXT = os.path.splitext(cmds.file(q= True, sn = True))[0] + '.txt'
        if os.path.isfile(fileNameTXT):
            textFile = open(fileNameTXT,'r')
            lists = textFile.readlines() 
            numbers = list()
            for line in lists:
                temStr =''
                for char in line:
                    if char.isdigit():
                       temStr +=char
                    elif char =='-' and temStr !='':
                        numbers.append(int(temStr))
                        temStr =''
                if temStr.isdigit():
                    numbers.append(int(temStr))
            print numbers
            textFile.close()
            for num in range(0,len(numbers)):
                #print numbers[num]
                if num ==0:
                    self.txtStart1.setText(str(numbers[num]))
                if num ==1:
                    self.txtEnd1.setText(str(numbers[num]))
                if num ==2:
                    self.txtStart2.setText(str(numbers[num]))
                if num ==3:
                    self.txtEnd2.setText(str(numbers[num]))
                if num ==4:
                    self.txtStart3.setText(str(numbers[num]))
                if num ==5:
                    self.txtEnd3.setText(str(numbers[num]))
                if num ==6:
                    self.txtStart4.setText(str(numbers[num]))
                if num ==7:
                    self.txtEnd4.setText(str(numbers[num]))
        else:
            QtGui.QMessageBox.critical(None,'Files is Wrong','Please create file txt for Animation, thanks.',QtGui.QMessageBox.Ok)
        
    def updateText(self):
        print"Text"
    def loadText(self):
        print'text'
    def previewAnimation(self):
        print"text"
    def nextAnimation(self):
        print"text"
         
   
        
def main():
    xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/FrontierWave_CustomNamingTool.xml'
    form = CustomNamingTool(xmlFile)
    return form 