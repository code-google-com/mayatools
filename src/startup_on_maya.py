# import os, sys, imp
# 
# def loadProject(projName):
#     if os.environ.get('PROJECT_DIR') + projName not in sys.path:
#         sys.path.append(os.environ.get('PROJECT_DIR') + projName)
#     file, pathname, description = imp.find_module(projName)
#     try:
#         print pathname
#         return imp.load_module(projName, file, pathname, description)
#     except:
#         print 'cannot load project'
#     finally:
#         if file: file.close() 
# 
# proj = loadProject('template_proj')
# proj.main()

import maya.cmds as cmds
import maya.mel as mel

mainWindow = mel.eval('global string $gMainWindow; $temp = $gMainWindow')
if cmds.menu('Foxforest', q= True, exists = True):
    cmds.deleteUI('Foxforest', menu = True)
menu = cmds.menu('Foxforest', parent = mainWindow, tearOff = True)