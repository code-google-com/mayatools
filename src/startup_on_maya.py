import os, sys, imp
import maya.cmds as cmds
import maya.mel as mel

def getNumProjects():
    globalProjects = [p for p in os.listdir(os.environ.get('PROJECT_DIR')) if 'py' not in p]
    return globalProjects

def loadProject(projName):
    if os.environ.get('PROJECT_DIR') + projName not in sys.path:
        sys.path.append(os.environ.get('PROJECT_DIR') + projName)
    file, pathname, description = imp.find_module(projName)
    try:
        return imp.load_module(projName, file, pathname, description)
    except:
        print 'cannot load project'
    finally:
        if file: file.close() 

def createMenu():
    projects = getNumProjects()
    mainWindow = mel.eval('global string $gMainWindow; $temp = $gMainWindow')
    if cmds.menu('Foxforest', q= True, exists = True):
        cmds.deleteUI('Foxforest', menu = True)
    menu = cmds.menu('Foxforest', parent = mainWindow, tearOff = True)
    cmds.menuItem('Project', parent = menu, subMenu = True)
    for p in projects:
        cmds.menuItem(l = p, c = 'startup_on_maya.loadProject(\'{proj}\')'.format(proj = p))
    cmds.setParent('..', menu = True)

print '-----------------------------------------'
print '--------------START TOOLS----------------'
print '-----------------------------------------'
print '--------------LOAD MENU------------------'

createMenu()