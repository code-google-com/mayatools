'''
Created on May 26, 2014

@author: trungtran
@decription:
    projectBase is quite simple class that read XMl data to generate all of infos

'''

import xml.dom.minidom

class projectBase():
   
    def __init__(self,XMLRootFile):
        self.ProjectName = ""
        self.managers = list()
        self.ServerPath = ""
        self.ClientPath = ""
        self.LocalPath = ""
        self.ProjectLocalPath = ""
        self.DocumentsPath = ""
        self.ReferencesImagePath = ""
        self.FeedbacksPath = ""
        self.AssetList = ''
        self.moduleList = list()
        self.readXMLFile(XMLRootFile)
                       
    def readXMLFile (self,XMLRootFile):
        xmldoc = xml.dom.minidom.parse(XMLRootFile)
        ProjectNode = xmldoc.firstChild
        #-- get project's name
        self.ProjectName = ProjectNode.getAttribute('name')
        #-- done get project's name
        
        #-- get project's paths
        dirRoot = ProjectNode.getElementsByTagName("Directories")[0]
        self.ServerPath = dirRoot.getElementsByTagName("ServerPath")[0].getAttribute("path")
        self.LocalPath = dirRoot.getElementsByTagName("LocalPath")[0].getAttribute("path")
        self.DocumentsPath = dirRoot.getElementsByTagName("DocumentsPath")[0].getAttribute("path")
        self.FeedbacksPath = dirRoot.getElementsByTagName("FeedbacksPath")[0].getAttribute("path")
        self.ReferencesImagePath = dirRoot.getElementsByTagName("ReferencesImagePath")[0].getAttribute("path")
                
        # get module
        pkgNodes = ProjectNode.getElementsByTagName('package')
        for pkg in pkgNodes:
            names = list()
            names.append(pkg.getAttribute('name'))
            print pkg.getAttribute('name')
            for mod in pkg.getElementsByTagName('module'):
                #print '\t|_' + mod.getAttribute('name')
                names.append(mod.getAttribute('name'))
            self.moduleList.append(names)
            
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