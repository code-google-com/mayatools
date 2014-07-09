# Author: Tran Quoc Trung - GlassEgg Digtal Media
# Date: 9-SEP-2012

import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, QtSql, uic

import functools
import maya.OpenMayaUI as OpenMayaUI
import os, sys, inspect
import imp
from datetime import *
import sip
import pyodbc
import random
import getpass
from xml.dom.minidom import *
import CommonFunctions as cf

status = ['Pending_WIP', 'WIP', 'to Art', 'to Tech', 'to Client', 'to Artist']
piority = {'#ff0000':'Highest', '#':'High', '#00ff00':'Normal', '#':'Low', '#0000ff':'Lowest'}
# get username to load data 
try:
    reload(Source.IconResource_rc)
except:
    import Source.IconResource_rc

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ProjectBoard.ui'
try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class Task(object):
    def __init__(self, data, parent = None):
        self.TaskID = data[0]
        self.parent = parent
        self.data = data
        self.childTasks = []
    
    def getChildTask(self, num):
        return self.childTasks[num]
    
    def getNumChild(self):
        return len(self.childTasks)
    
    def getChildNum(self):
        if parent != None:
            return self.parent.childTasks.index(self)
        return 0
    
    def getColumnCount(self):
        return len(self.data)
    
    def getData(self, num):
        return self.data[num]
    
    def getParent(self):
        return self.parent
    
    def setData(self, value, column):
        if column < 0 or column > len(self.data):
            return False
        self.itemData[column] =  value
        return True
    
    def insertChildTask(self, task):
        if task.getParent.TaskID == self.TaskID:
            self.childTasks.append(task)
            return True
        else:
            False
        
    def removeChildTask(self, child):
        if child in self.childTasks:
            self.childTasks.remove(child)
            return True
        else:
            return False
    
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
    def __init__(self, data, header, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(header)
        self._headers = header
        self._missingIndexes = list()
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
                if f[0] == False:
                    #print data[1][id].index(f)
                    #print pathID.row()
                    if pathID.isValid():
                        miss_Id = self.index(0, 1, pathID)
                        print miss_Id.row()
                        self._missingIndexes.append(miss_Id)

class Issue():
    def __init__(self):
        pass
    
    def receiver(self):
        pass
    
    def getReceiver(self):
        pass
    
    def setIssueDone(self):
        pass

class Asset(QtGui.QListWidgetItem):
    def __init__(self, name, image, start_date, end_date, status):
        super(Asset, self).__init__()
        icon = QtGui.QIcon()
        self._name = name
        self._status = status
        self._startdate = start_date
        self._enddate = end_date
        try:
            if not os.path.exists(image):
                raise 'Cannot found this image', image
            icon.addFile(image)
        except:
            icon.addFile(':/Project/empty.tif')
        finally:
            self.setIcon(icon)
            #self.setText(self._name)
        
    def time(self):
        now = datetime.today()
        remain = self._enddate - now  
        spent  = now - self._startdate
        
    def getTask(self):
        ID = ''
    
    def getIssue(self):
        pass
    
    def createTask (self):
        pass
    
    def createIssue(self):
        pass
    
    def showToolTips(self):
        pass
    
class delegateColorPriority(QtGui.QAbstractItemDelegate):
    pass
    
class ProjectBoard(form_class,base_class):
    def __init__(self, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        #self.listWidgetAsset.clear()
        asset = list()
        #headers = ['Project ID','Group_ID','Name','File Name','Status']
        #cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools_Test;UID=geuser;PWD=Aa@123456')
        #cursor = cnxn.cursor()
        #cursor.execute("select Project_ID, Group_ID,Name,Start_Date, End_Date from tbl_Asset")
        #rows = cursor.fetchall()
        #for row in rows:
            #i=1
            #asset = Asset(row[0], row[1], row[2], row[3], row[4])
            #asset.append(row[0])
            #asset.append(row[1])
            #asset.append(row[2])
            #asset.append(row[3])
            #asset.append(row[4])
            #self.listWidgetAsset.insertRow(i)
            #self.listWidgetAsset.addItem(str(row[0]))
            #self.listWidgetAsset.addItem(str(row[1]))
            #self.listWidgetAsset.addItem(str(row[2]))
            #self.listWidgetAsset.addItem(str(row[3]))
            #self.listWidgetAsset.addItem(str(row[4]))
            #i=i+1
            #asset = ""
        #self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools_Test;UID=geuser;PWD=Aa@123456')
        # Your database needs to be created so you can pass it to your model
        
        '''
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools;UID=geuser;PWD=Aa@123456')
        cursor = self.cnxn.cursor()
        cursor.execute("{call sp_sel_List_Project}")
        rows = cursor.fetchall()
        # variables 
        self._projectNames = [x.Name for x in rows]
        
        self.cbbProjectName.addItems(self._projectNames)
        self.cbbProjectName.currentIndexChanged.connect(self.loadProjectDataInWIP)
        self._techDepts      = managers[0]
        self._artDepts       = managers[1]
        self._producerDepts  = managers[2]
        self._userID = getpass.getuser()
        '''
        # startup loadings
        #model = QtGui.QStringListModel(status)
        #self.cbbAssetStatus.setModel(model) # display status in asset view
        #self.cbbIssueStatus.setModel(model) # display status in issue view
        #self.cbbTaskStatus.setModel(model)  # display status in task view
        # BUTTON ACTION:
        self.btnSearch.clicked.connect(self.displayData)
        #self.loadUIStartUp()
        # CODE TEST
        '''
        header = ('', 'File Name', 'Dimension','Tag', 'File Node')
        model = taskTreeModel(5,header)
        self.listWidgetAsset.setModel(model)
        self.listWidgetAsset.expandAll()
        for i in range(len(header)):
            self.listWidgetAsset.resizeColumnToContents(i) 
        '''
    
    def displayData(self):
        
        db = QtSql.QSqlDatabase.addDatabase("SQL Server", "Gem_Tools_Test")
        db.setHostName("GESVR05")
        db.setPort(1433)
        db.setDatabaseName("Gem_Tools_Test")
        db.setUserName("geuser")
        db.setPassword("Aa@123456")
        
        if not db.open():
            QtGui.QMessageBox.Warning(
                self,
                "Database Connection Error", 
                "Database Error" 
            )
            
            print "Data khong ket noi"
            #sys.exit(1)  # you want your whole program to exit?
        
        #self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools;UID=geuser;PWD=Aa@123456')
        #cursor = self.cnxn.cursor()
        #cursor.execute("select Project_ID, Group_ID,Name,Start_Date, End_Date from tbl_Asset")
        #rows = cursor.fetchall()
        self.db = db

        # pass the database to the model
        self.model = QtSql.QSqlTableModel(self, self.db)
        self.model.setTable('items')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)

        # create the view and set the model
        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.model)
    def updateDatatoView(self):
        header = ('Project ID','Group_ID','Name','File Name','Status')
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools_Test;UID=geuser;PWD=Aa@123456')
        cursor = cnxn.cursor()
        cursor.execute("select Project_ID, Group_ID,Name,Start_Date, End_Date from tbl_Asset")
        rows = cursor.fetchall()
        data = list()
        items = []
        for row in rows:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, unicode(row[0]))
            items.append(item)
        self.treeViewProject.insertTopLevelItems(0, items)
        #for row in rows:
            #print row
            #data.append(row)
            #print data
        #model = TreeModel(data, header)
        #self.treeViewResult.setModel(model)
        #for i in range(len(header)):
         #   self.treeViewResult.resizeColumnToContents(i) 
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
                res = str(int(f.outSizeX.get())) + 'x' + str(int(f.outSizeY.get()))
                fileInfos = [status, name, res, '',str(f)]
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
        
        header = ('', 'File Name', 'Dimension','Tag', 'File Node')
        model = TreeModel(arrFilter, header)
        self.treeViewResult.setModel(model)
        self.treeViewResult.expandAll()
        for i in range(len(header)):
            self.treeViewResult.resizeColumnToContents(i) 
    def showAllAsset(self, projectName):
        self.listWidgetAsset.clear()
        cursor = self.cnxn.cursor()
        #if self._userID in (self._techDepts + self._artDepts + self._producerDepts): 
            #cursor.execute("SELECT Name, URL, Start_Date, End_Date FROM view_Asset_ProjName as a WHERE a.Project_Name = '{project}'".format(project = projectName))
        cursor.execute("SELECT Name, URL, Start_Date, End_Date FROM view_Asset_ProjName")
        rows = cursor.fetchall()
        for i in rows:
            asset = Asset(i[0], i[1], i[2], i[3], i[4])
            self.listWidgetAsset.addItem(asset)
                
#    def showAllIssue(self, projectName):
#        self.listWidgetIssue.clear()
#        cursor = self.cnxn.cursor()
#        if self._userID in (self._techDepts + self._artDepts + self._producerDepts): 
#            cursor.execute("SELECT * FROM view_Issue_ProjName as a WHERE a.Project_Name = '{project}'".format(project = projectName))
#            rows = cursor.fetchall()
#            for i in rows:
#                issue = Issue(i[0], i[1], i[2], i[3], 'none')
#                self.listWidgetIssue.addItem(issue)
                
    def getProjectGroup(self, projectName):
        cursor = self.cnxn.cursor()
        #cursor.execute("SELECT Group_Name FROM view_Group_ProjName as v WHERE v.Name = '{project}'".format(project = str(self.cbbProjectName.currentText())))
        cursor.execute("SELECT Group_Name FROM view_Group_ProjName")
        groups = [x[0] for x in cursor.fetchall()]
        groups.append('--All group--')
        model = QtGui.QStringListModel(groups)
        self.cbbProject.setModel(model)
        self.cbbProject.setCurrentIndex(groups.index('--All group--'))
        
    def loadUIStartUp(self):
        #if self.checkRecentProject() in self._projectNames:
        #    self.cbbProjectName.setCurrentIndex(self._projectNames.index(self.checkRecentProject()))
        #self.showAllAsset(self.checkRecentProject())
        #showAllAsset(self.checkRecentProject())
        headers = ['Project ID','Group_ID','Name','File Name','Status']
        #self.showAllIssue(self.checkRecentProject())
            
    def checkRecentProject(self):
        # check whether setting file in exist
        # get the most recent project if file exist
        if os.path.exists('c:\ProgramData\GESettings\settings.xml'):
            xmlDoc = xml.dom.minidom.parse('c:\ProgramData\GESettings\settings.xml')
            recentProName = xmlDoc.getElementsByTagName('RECENT_PROJECT')[0].getAttribute('Name')
            return recentProName
                
    def updateCurrentProject(self):
        try:
            xmlDoc = xml.dom.minidom.parse('c:/ProgramData/GESettings/settings.xml')
            xmlDoc.getElementsByTagName('RECENT_PROJECT')[0].setAttribute('Name', str(self.cbbProjectName.currentText()))
        except:
            xmlDoc = xml.dom.minidom.Document()
            recentProjectNode = xmlDoc.createElement('RECENT_PROJECT') 
            recentProjectNode.setAttribute('Name', str(self.cbbProjectName.currentText()))   
            xmlDoc.appendChild(recentProjectNode)
        finally:
            cf.writeXML_v2(xmlDoc, 'c:/ProgramData/GESettings/','settings.xml')
        
    def loadProjectDataInWIP(self):
        currentProject = str(self.cbbProjectName.currentText())
        self.updateCurrentProject()
        # update Asset View
        self.showAllAsset(currentProject) # display all assets of selected project
        self.getProjectGroup(currentProject) # display all group of selected project
        # update Issue View
        #self.showAllIssue(currentProject) # display all issues of selected project
        
    
    def createIssue(self, AssetID):
        pass
    
    def createTask(self, AssetID):
        pass
    
    def editIssue(self, IssueID):
        pass
    
    def deteleIssue(self):
        pass
    
    def closeEvent(self):
        self.cnxn.close()
        
    
        
        
        


        