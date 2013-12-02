import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui
import maya.OpenMayaUI as OpenMayaUI
from xml.dom.minidom import *
import sys, os, shutil

def gcd(a, b):
    while b:
        a,b = b, a % b
    return a

def lcm(a, b):
    return a * b/gcd(a,b)

def convertArrayListToList(ArrayList):
    out = list()
    for arr in ArrayList:
        for e in arr:
            out.append(e)
    return out

def backupData(file):
    if os.path.isfile(file):
        backupFile = file.replace(os.path.splitext(file)[1],'.bak')
        if os.path.isfile(backupFile):
            os.remove(backupFile)
        os.rename(file, backupFile)
        os.system('attrib +h {file}'.format(file = backupFile))

def loadModule(moduleName):
    sys.path.append(fileDirCommmon + '/MODULE/' + moduleName)
    file, pathname, description = imp.find_module(moduleName)
    try:
        return imp.load_module(moduleName, file, pathname, description)
    finally:
        if file: file.close()

def writeXML(xmlDoc, location):
    #print xmlDoc.toprettyxml()
    openStream = open(location, 'w')
    openStream.write(xmlDoc.toprettyxml())
    openStream.close()
    
def writeXML_v2(xmlDoc, location, fileName):
    #print xmlDoc.toprettyxml()
    if not os.path.exists(location):
        os.makedirs(location)
    openStream = open(location + fileName, 'w')
    openStream.write(xmlDoc.toprettyxml())
    openStream.close()

def getDataFromClipboard():
    clipboard = QtGui.QApplication.clipboard()
    out = str(clipboard.text())
    return out
    
def setDataToClipboard(text):
    clipboard = QtGui.QApplication.clipboard()
    out = clipboard.setText(text)

def selectFaceByShaderPerMesh(mesh, shader):
    # get shading group from shader
    try:
        shape = cmds.listRelatives(mesh, shapes = True)[0]
    except ValueError:
        return
    shadingGroups = py.listConnections(shader, type = 'shadingEngine')
    #print shadingGroups
    faceList = py.sets(shadingGroups, q = True)
    #print faceList
    selectedFaces = []
    for f in faceList:
        shapefromFace = f.split('.')[0]
        if shapefromFace == shape:
            selectedFaces.append(f)
    #print selectedFaces
    if shape not in selectedFaces:
        cmds.select(selectedFaces)
        if len(cmds.ls(sl = True, fl = True)) == cmds.polyEvaluate(mesh, f = True):# in case selected faces is equal to the number of  faces
            cmds.select(mesh)
        else:
            #attachFileSource = fileDirCommmon + '/detachComponent.mel'
            #mel.eval('source \"{f}\";'.format(f = attachFileSource))
            cmds.select(selectedFaces)
    else: # object has only one material
        #print 'select: ' + mesh
        cmds.select(mesh)

def copytreewithFilter(src, dst, filter, backup = True):
        if os.path.isfile(src):
            backupData(dst)
            if os.path.splitext(src)[1] in filter:
                shutil.copyfile(src, dst)
            else:
                print "cannot copy files"
        if os.path.isdir(src):
            names = os.listdir(src)
            try:
                os.makedirs(dst)
            except:
                pass
            errors = []
            for name in names:
                srcname = os.path.join(src, name)
                dstname = os.path.join(dst, name)
                try:
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname)
                    if os.path.isfile(srcname):
                        backupData(dstname)
                        if os.path.splitext(srcname)[1] in filter:
                            shutil.copyfile(srcname, dstname)
                        else:
                            print "cannot copy files"
            # XXX What about devices, sockets etc.?
                except (IOError, os.error) as why:
                    errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
                except Error as err:
                    errors.extend(err.args[0])
                try:
                    shutil.copystat(src, dst)
                except WindowsError:
            # can't copy file access times on Windows
                    pass
                except OSError as why:
                    errors.extend((src, dst, str(why)))
                if errors:
                    pass

def copytree(src, dst, backup = True):
        if os.path.isfile(src):
            backupData(dst)
            shutil.copyfile(src, dst)
            
        if os.path.isdir(src):
            names = os.listdir(src)
            try:
                os.makedirs(dst)
            except:
                pass
            errors = []
            for name in names:
                srcname = os.path.join(src, name)
                dstname = os.path.join(dst, name)
                try:
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname)
                    if os.path.isfile(srcname):
                        backupData(dstname)
                        shutil.copyfile(srcname, dstname)
                    
            # XXX What about devices, sockets etc.?
                except (IOError, os.error) as why:
                    errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
                except Error as err:
                    errors.extend(err.args[0])
                try:
                    shutil.copystat(src, dst)
                except WindowsError:
            # can't copy file access times on Windows
                    pass
                except OSError as why:
                    errors.extend((src, dst, str(why)))
                if errors:
                    pass
                    #raise Error(errors)
        
def getShadersFromMesh(mesh):                    
        # get shader from nodes
        shapeNode = cmds.listRelatives(mesh, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
        for sg in sgs:
            print sg
            if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                shaders.append(shader)
        return shaders
    