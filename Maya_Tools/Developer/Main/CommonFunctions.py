import maya.cmds as cmds
import pymel.core as py
from pymel import versions
import maya.OpenMayaUI as OpenMayaUI
from xml.dom.minidom import *
import sys, os, shutil, re, imp

def getMayaVersion():
    return versions.current()

try:
    from PySide import QtGui, QtCore
    import pysideuic
except:
    from PyQt4 import QtCore, QtGui, uic

def loadUIPySide(uiFile):
    from PySide import QtGui, QtCore
    import pysideuic
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(uiFile, 'r') as f:
            o = StringIO()
            frame = {}
            
            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame
            
            #Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('QtGui.%s'%widget_class)
    return form_class, base_class

def loadUIPyQt(uiFile):
    try:
        form_class, base_class = uic.loadUiType(uiFile)
        return form_class, base_class
    except IOError:
        print (dirUI + ' not found')
    
def loadUI(uiFile):
    try:
        loadUIPySide(uiFile)
    except:
        loadUIPyQt(uiFile)
    
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
        
def loadModule_v2(moduleDir):
    sys.path.append(moduleDir.replace(moduleDir.split('/')[-1],''))
    file, pathname, description = imp.find_module(moduleDir.split('/')[-1].split('.')[0])
    try:
        return imp.load_module(moduleDir.split('/')[-1].split('.')[0], file, pathname, description)
    finally:
        if file: file.close()
        
def loadProject(projectName):
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
        currentFileName = os.path.split(cmds.file(q = True, sn = True))[1]
        if re.search('.*_v[0-9]*\.*', currentFileName):
            index = os.path.splitext(os.path.split(currentFileName)[1])[0].split('_v')[-1]
            nameFile = currentFileName.replace(index, '0' + str(int(index)+1))
            print nameFile 
        else:
            nameFile = os.path.splitext(currentFileName)[0] + '_v00' + os.path.splitext(currentFileName)[1] 
            print nameFile
        cmds.file(rn = nameFile)
        cmds.file(s = True, type = 'mayaBinary')
        
