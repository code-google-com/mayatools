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

def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().deleteLater()

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
                    
def saveFileIncrement():
        #print 'OK'
        curentFileName = os.path.split(cmds.file(q = True, sn = True))[1]
        #print curentFileName
        strList = os.path.splitext(os.path.split(curentFileName)[1])[0].split('_')
        try:
            index = int(strList[len(strList)-1].replace('v', ''))
        except:
            index = 0
        namefile = os.path.split(cmds.file(q = True, sn = True))[0] + '\\' + self.combineString(strList) + 'v' + str(index + 1) + '.mb'
        cmds.file(rn = namefile)
        cmds.file(s = True, type = 'mayaBinary')
        
