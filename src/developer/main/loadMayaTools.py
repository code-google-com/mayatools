import pymel.core as py

try:
    reload(mainEntry)
except:
    from developer.main.common import mainEntry
    
from developer.main.common import commonFunctions as cf

def loadProject(projName):
    ProjectXML = cf.getPath(__file__, 2) + '/projects/' + projName + '.xml'
    if py.window('ProjectUIWindow', q = True, ex= True):
        py.deleteUI('ProjectUIWindow')    
    form = mainEntry.projectUI(ProjectXML)
    form.show()