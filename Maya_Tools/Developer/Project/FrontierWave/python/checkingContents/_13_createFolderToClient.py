description = 'Create copy To client.'
name = 'CreateCopyToClient'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import distutils.core
import os, sys, re, inspect , imp, shutil
from xml.dom.minidom import *
from PyQt4 import QtGui, QtCore, uic
import subprocess as s
# Tho them vao:
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT

################################### IMPORT MAIL #####################

################################## END IMPORT MAIL #################################

PathToClient= 'T:/Scenes/FrontierWave_characters/To_Client/Today/'
PathCharacter ='T:/Scenes/FrontierWave_characters/'


#import AssetForm
#reload(AssetForm)

    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
#fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]


def execute():
    ####################### COPY TO CLIENT ###########################
    #xmlFile = os.path.split(fileDirCommmon)[0] + '/XMLfiles/FrontierWave.xml'
    #signalChange = QtCore.QObject(SIGNAL('currentIndexChanged(int)'))
    
    try:
        reload(AssetForm)
    except:
        import AssetForm
     
    xmlFile = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/FrontierWave.xml'
    ass = AssetForm.AssetForm(xmlFile)
    #assetValue = ass.returnAssetValue()
    assetValue =''
    groupValue =''
    #assetValue = signalChange(ass.returnAssetValue())
    assetValue = ass.returnAssetValue()
    print('asset dang copy:',assetValue)
    groupValue = ass.retrunGroupValue()
    print('group dang copy:',groupValue)
    
      
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
    
   
    
