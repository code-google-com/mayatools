'''
Created on May 26, 2014

@author: trungtran
'''

import xml.dom.minidom

class projectBase():
    '''
    project base class: to create a very base class that contains some features
    
    '''
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
        self.AssetList = self.projectData + '/AssetList.xml'
        self.moduleList = list()
        self.readXMLFile(XMLRootFile)
                       
    def readXMLFile (self,XMLRootFile):
        xmldoc = xml.dom.minidom.parse(XMLRootFile)
        ProjectNode = xmldoc.firstChild
        #-- get project's name
        self.ProjectName = ProjectNode.getAttribute('name')
        #-- done get project's name
        
        #-- get project's path
        dirRoot = ProjectNode.getElementsByTagName("Directories")[0]
        self.ServerPath = dirRoot.getElementsByTagName("ServerPath")[0].getAttribute("path")
        self.LocalPath = dirRoot.getElementsByTagName("LocalPath")[0].getAttribute("path")
        self.DocumentsPath = dirRoot.getElementsByTagName("DocumentPath")[0].getAttribute("path")
        self.FeedbacksPath = dirRoot.getElementsByTagName("FeedbackPath")[0].getAttribute("path")
        self.ReferencesImagePath = dirRoot.getElementsByTagName("ReferencesImagePath")[0].getAttribute("path")
                
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
            
        # get managers    
        ManagerDepts = ProjectNode.getElementsByTagName("Managers")[0]
        for dept in ManagerDepts.childNodes:
            if dept.hasChildNodes():
                userlist = list()
                for person in dept.childNodes:
                    if person.firstChild != None:
                        userlist.append(person.getAttribute("name"))
                self.managers.append(list(set(userlist)))
                                    
    def Technician(self):
        return self.managers[0]

    def Art(self):
        return self.managers[1]

    def Producer(self):
        return self.managers[2]