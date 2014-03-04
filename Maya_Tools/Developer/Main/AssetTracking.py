# Author: Tran Quoc Trung - GlassEgg Digtal Media
# Date: 9-SEP-2012

import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic

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
dirUI= fileDirCommmon +'/UI/AssetTracking.ui'
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
    
class taskTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, headers, data):
        super(taskTreeModel,self).__init__()
        self.header = Task(headers)
        self.setModelData(data, self.header)
    
    def columnCount(self, parent = QtCore.QModelIndex()):
        return self.header.getColumnCount()
        
    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole or role != QtCore.Qt.EditRole:
            return None
        
    def flags(self, index):
        if not index.isValid():
            return None
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def getItem(self, index):
        if not index.isValid():
            return self.header
        else:
            item = index.internalPointer()
            if item:
                return item 
            
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False
        item = self.getItem(index)
        result = item.setData(index.column(), value)
        if result:
            self.dataChanged.emit(index, index)
            
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header.getData(section)
        return None
    
    def setHeaderData(self, section, orientation, value, role = QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False
        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result
    
    def rowCount(self):
        pass
        
    def setModelData(self, data, parent):
        parents = [parent]
        num = 0
        while num < len(data):
            pass

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
            self.setText(self._name)
        
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
    
class AssetTracking(form_class,base_class):
    def __init__(self, managers, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools_Test;UID=geuser;PWD=Aa@123456')
        #self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=QUOCTRUNG-PC\SQLEXPRESS;DATABASE=Gem_Tools;UID=sa;PWD=trungswat@521987')
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
        # startup loadings
        model = QtGui.QStringListModel(status)
        self.cbbAssetStatus.setModel(model) # display status in asset view
        self.cbbIssueStatus.setModel(model) # display status in issue view
        self.cbbTaskStatus.setModel(model)  # display status in task view
        
        self.loadUIStartUp()
        
    def showAllAsset(self, projectName):
        self.listWidgetAsset.clear()
        cursor = self.cnxn.cursor()
        if self._userID in (self._techDepts + self._artDepts + self._producerDepts): 
            cursor.execute("SELECT Name, URL, Start_Date, End_Date FROM view_Asset")
            rows = cursor.fetchall()
            for i in rows:
                print i[0]
                asset = Asset(i[0], i[1], i[2], i[3], 'none')
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
        cursor.execute("SELECT Group_Name FROM view_Group_ProjName as v WHERE v.Name = '{project}'".format(project = str(self.cbbProjectName.currentText())))
        groups = [x[0] for x in cursor.fetchall()]
        groups.append('--All group--')
        model = QtGui.QStringListModel(groups)
        self.cbbGroup.setModel(model)
        self.cbbGroup.setCurrentIndex(groups.index('--All group--'))
        
    def loadUIStartUp(self):
        if self.checkRecentProject() in self._projectNames:
            self.cbbProjectName.setCurrentIndex(self._projectNames.index(self.checkRecentProject()))
        self.showAllAsset(self.checkRecentProject())
        headers = ['Task_ID','Artist','Description','File Name','Status']
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
        
    
        
        
        


        