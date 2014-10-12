import os, sys, imp
import maya.cmds as cmds
import maya.mel as mel

def getNumProjects():
    projDir = os.environ.get('PROJECT_DIR') + 'projects\\'
    globalProjects = [p for p in os.listdir(projDir) if 'py' not in p]
    return globalProjects

def loadProject(projName):
    sys.path.append(os.environ.get('PROJECT_DIR') + 'main\\')
    file, pathname, description = imp.find_module('loadMayaTools')
    mod = imp.load_module('loadMayaTools', file, pathname, description)
    mod.loadProject(projName)    

def createMenu():
    print 'A new project has been added to system ...............................................\n\n\n'
    projects = getNumProjects()
    mainWindow = mel.eval('global string $gMainWindow; $temp = $gMainWindow')
    if cmds.menu('Foxforest', q= True, exists = True):
        cmds.deleteUI('Foxforest', menu = True)
    menu = cmds.menu('Foxforest', parent = mainWindow, tearOff = True)
    cmds.menuItem('Project', parent = menu, subMenu = True)
    for p in projects:
        cmds.menuItem(l = p.split('.')[0], c = 'startup_on_maya.loadProject(\'{proj}\')'.format(proj = p.split('.')[0]))
    cmds.setParent('..', menu = True)

print '-----------------------------------------'
print '--------------START TOOLS----------------'
print '-----------------------------------------'
print '--------------LOAD MENU------------------'

createMenu()