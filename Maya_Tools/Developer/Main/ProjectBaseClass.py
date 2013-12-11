import os, sys, re
from xml.dom.minidom import *

def isParentinList(lst, node):
    if node in lst:
        return (True, node)
    for i in lst:
        sepaNodes = i.split('/')
        if node in sepaNodes:
            return (True, i)
    return  (False, node)

def filterParentFolders(listFolders):
    out = list()
    for i in range(len(listFolders)):
        for j in range(i,len(listFolders)):
            if not re.search(r'(.*){sample}(.*)'.format(sample = listFolders[j]), listFolders[i], re.I):
                out.append(listFolders[i])
    return out

class ProjectBaseClass():
    def __init__(self,XMLRootFile):
        self.ProjectName = ""
        self.Managers = list()
        self.ServerPath = ""
        self.ClientPath = ""
        self.LocalPath = ""
        self.ProjectLocalPath = ""
        self.DocumentsPath = ""
        self.ReferencesImagePath = ""
        self.FeedbacksPath = ""
        self.LibraryPath = ""
        self.PluginsPath = ''
        self.projectData = os.path.split(XMLRootFile)[0]
        self.AssetList = self.projectData + '/AssetList.xml'
        self.NamingConvetion = ""
        self.LOD = list()
        self.stages = list()
        self.managers = list()
        self.structureFolders = list()
        self.placeFileAndName = list()
        self.moduleList = list()
        self.checkList = list()
        self.workingStage = list()
        self.templateStructure = ''
        
        self.group = False
        self.readXMLFile(XMLRootFile)
   
    def getFolderFromNode(self, node):
        for child in node.childNodes:
            try:
                parent = child.parentNode.getAttribute('name')
            except:
                parent = 'node'
            if isParentinList(self.structureFolders, parent)[0]:
                try:
                    #self.structureFolders.remove(parent)
                    #self.structureFolders.remove(isParentinList(self.structureFolders, parent)[1])
                    self.structureFolders.append(isParentinList(self.structureFolders, parent)[1] + '/' + child.getAttribute('name'))
                    if child.hasAttribute('filetype'):
                        self.placeFileAndName.append(child.getAttribute('filename') + '.' + child.getAttribute('filetype'))
                    else:
                        self.placeFileAndName.append('')
                except:
                    pass
            else:
                try:
                    self.structureFolders.append(child.getAttribute('name'))
                    if child.hasAttribute('filetype'):
                        self.placeFileAndName.append(child.getAttribute('filename') + '.' + child.getAttribute('filetype'))
                    else:
                        self.placeFileAndName.append('')
                except:
                    pass
            self.getFolderFromNode(child) 
                        
    def readXMLFile (self,XMLRootFile):
        xmldoc = xml.dom.minidom.parse(XMLRootFile)
        ProjectNode = xmldoc.firstChild
        self.ProjectName = ProjectNode.getAttribute('name')
        dir = ProjectNode.getElementsByTagName("Directories")[0]
        for d in dir.childNodes:
            name = d.nodeName
            if name == "ClientPath":
                self.ClientPath = d.childNodes[0].data
            if name == "ServerPath":
                self.ServerPath = d.childNodes[0].data
            if name == "LocalPath":
                self.LocalPath = d.childNodes[0].data
            if name == "ProjectLocalPath":
                self.ProjectLocalPath = d.childNodes[0].data
            if name == "DocumentsPath":
                self.DocumentsPath = d.childNodes[0].data
            if name == "FeedbacksPath":
                self.FeedbacksPath = d.childNodes[0].data
            if name == "ReferencesImagePath":
                self.ReferencesImagePath = d.childNodes[0].data
            if name == "LibraryPath":
                self.LibraryPath = d.childNodes[0].data
            if name == "PluginsPath":
                self.PluginsPath = d.childNodes[0].data
                
        ProjectData = ProjectNode.getElementsByTagName("ProjectData")[0]
                
        # get module
        names = list()
        params = list()
        moduleNode = ProjectNode.getElementsByTagName('Module')[0]
        for module in moduleNode.getElementsByTagName('module'):
            nameModule = module.getAttribute('name')
            if module.getAttribute('params'):
                paramsModule = self.ProjectName + '.' + module.getAttribute('params')
            else:
                paramsModule= ''
            names.append(nameModule)
            params.append(paramsModule)
        self.moduleList.append(names)
        self.moduleList.append(params)    
        # get checklist
        checkListNode = ProjectNode.getElementsByTagName('CheckList')[0]
        for check in checkListNode.getElementsByTagName('check'):
            nameCheck = check.getAttribute('name')
            self.checkList.append(nameCheck)
            
        # get managers    
        ManagerDepts = ProjectNode.getElementsByTagName("Managers")[0]
        for dept in ManagerDepts.childNodes:
            if dept.hasChildNodes():
                userlist = list()
                for person in dept.childNodes:
                    if person.firstChild != None:
                        userlist.append(person.firstChild.nodeValue)
                self.managers.append(list(set(userlist)))
                
        StructureNode = xmldoc.getElementsByTagName('Structures_Asset')[0]
        self.getFolderFromNode(StructureNode)
        print self.placeFileAndName
        # get template
        
        # get LOD
        lodNodes = ProjectNode.getElementsByTagName("folder")
        for node in lodNodes:
            if node.getAttribute("type") == "LOD":
                self.LOD.append(node.getAttribute("name"))
                #print node.getAttribute("name")
        self.LOD = sorted(list(set(self.LOD)))
                
        # get stage
        stages = ProjectNode.getElementsByTagName("folder")
        for node in stages:
            if node.getAttribute("type") == "stage":
                self.stages.append(node.getAttribute("name"))
        self.stages = sorted(list(set(self.stages)))
        
        # get group
        if StructureNode.getAttribute('group') == 'True':
            self.group = True
        else:
            self.group = False
        
        templateNode =  ProjectNode.getElementsByTagName('Template')[0]
        self.templateFile = 'template' + '/' + templateNode.getAttribute('file')
        
        # get project data 
        
        print self.templateFile
            
    def Technical(self):
        return self.managers[0]

    def Art(self):
        return self.managers[1]

    def Producer(self):
        return self.managers[2]
    
#cc = ProjectBaseClass('I:\\MayaToolSystem\\Developer\\Project\\Sony\\XMLfiles\\Sony.xml')
    
    
