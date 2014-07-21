'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: project main entry

'''
import inspect,os
import pymel.core as py

from developer.main.common import mainEntry
from developer.main.common import commonFunctions as cf

reload(mainEntry) 

def loadProject(projName):
    ProjectXML = cf.getPath(__file__, 2) + '/projects/' + projName + '/xml/' + projName + '.xml'
    if py.window('ProjectUIWindow', q = True, ex= True):
        py.deleteUI('ProjectUIWindow')    
    form = mainEntry.projectUI(ProjectXML)
    form.show()