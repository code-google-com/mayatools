from PyQt4 import QtGui, QtCore, uic
#import maya.cmds as cmds
#import maya.mel as mel
#from pymel.core import *
import os, sys, inspect
import xml.dom.minidom as doc
from ProjectBaseClass import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/GE_TeamWork.ui'

form_class, base_class = uic.loadUiType(dirUI)

class GETeamWorkDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() == "File Name":
            editor = QtGui.QLineEdit(parent)
            self.connect(editor,SIGNAL('returnPressed()'),self.commitAndCloseEditor)
            return editor
        elif index.column() == "Owner":
            editor = QtGui.QComboBox(parent)
            return editor
        elif index.column() == 'Status':
            editor = QtGui.QCheckBox(parent)
            return editor
        elif index.column() == 'Reference':
            pass
        return editor

    def setEditorData(self, checkbox, index):
        checkState = index.model().data(index, QtCore.Qt.DecorativeRole)
        checkbox.setCheckState(checkState)

    def setModelData(self, checkbox, model, index):
        checkState = checkbox.checkState()
        model.setData(index,checkState, QtCore.Qt.EditRole)

class GEXMLModel(QtCore.QAbstractItemModel):
    def __init__(self,parent,XMLRootNode):
        super(GEXMLModel,self).__init(parent)

    def header(self):
        pass

class GETeamWork (form_class, base_class):
    def __init__(self,GEProjectXMLAssetList):
        super(base_class,self).__init__()
        self.setupUi(self)  
        self.xmldir = GEProjectXMLAssetList
        self.loadAssetList()
        self.showheaders()
        
    def addmember(self,asset_part,username,filename):
        xmldoc = doc.parse(self.xmldir)
        node = xmldoc.createElement("file")
        node.setAttribute("username", username)
        node.setAttribute("filename", filename)
        pnode = xmldoc.getElementsByTagName("asset_part")[0]
        pnode.appendChild(node)
        writetodoc = open(self.xmldir,'w')
        writetodoc.write(xmldoc.toprettyxml())
        writetodoc.close()
        
    def loadAssetList(self):
        assetlist = list()
        xmldoc = doc.parse(self.xmldir)
        AssetNodes = xmldoc.getElementsByTagName('asset')
        for asset in AssetNodes:
            name = asset.getAttribute('asset_name')
            assetlist.append(name)
        assetModel = QtGui.QStringListModel(assetlist)
        self.cbbAssetList.setModel(assetModel)

    def showheaders(self):
        header = []
        xmldoc = doc.parse(self.xmldir)
        AssetNodeSample = xmldoc.getElementsByTagName('file')[0]
        for i in range(AssetNodeSample.attributes.length):
            print (AssetNodeSample.attributes.item(i).name)
            header.append(AssetNodeSample.attributes.item(i).name)
        #header.append('status')
        header.append('Reference')
        self.trWiGet.setHeaderLabels(header)

    def loadAllAssetInfo(self,seekingAsset):#load info  of asset to form.
        xmldoc = doc.parse(self.xmldir)
        AssetNodes = xmldoc.getElementsByTagName('asset')
        for asset in AssetNodes:
            if seekingAsset == asset.getAttribute('asset_name'):
                getfiles = asset.getElementsByTagName('file')

    def loadAsset(self,username,filename,status,ref):
        pass
               


        
        
