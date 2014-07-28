import pymel.core as py
from PyQt4 import QtGui, QtCore
from functools import wraps

def getSelectedNodeName():
    selNode = py.ls(sl = True)[0]
    return selNode
                
def renaming(newStr):
    '''
        Rename the first selected node to new name.
    '''
    selObj = py.ls(sl= True, transforms = True)
    if len(selObj) == 1:
        try:
            py.rename(selObj[0], newStr)
        except RuntimeError:
            QtGui.QMessageBox.warning(None,'Error','Khong the rename do ten khong hop le. Khong duoc dat so o dau tien.',QtGui.QMessageBox.Ok)                
    elif len(selObj) > 1:
            QtGui.QMessageBox.warning(None,'Error','Chon mot objec de rename',QtGui.QMessageBox.Ok)

def addPrefix(newStr):
    '''
        Add prefix to all selected nodes
    '''
    selObjs = py.ls(sl = True)
    for obj in selObjs:
        newname = newStr + obj 
        py.rename(obj, newname)
            
def addSuffix(newStr):
    '''
        Add suffix to all selected nodes
    '''
    selObjs = py.ls(sl =True)
    for obj in selObjs:
        newname = obj + newStr
        py.rename(obj, newname)
            
def replacedBy(searchStr, newStr, isHierarchy):
    '''
        Replace searchStr with newStr. If hierarchy is selected, this will be applied for entire hierarchy. 
    '''
    selObjs = py.ls(sl = True)
    if isHierarchy:
        for i in selObjs:
            newName = i.split('|')[-1].replace(searchStr, newStr)
            py.rename(i, newName)
        else:
            childNodes = py.listRelatives(ad = True, pa = True)
            for node in childNodes:
                newname = node.split('|')[-1].replace(searchStr, newStr)
                py.rename(node, newname)
            # rename selected nodes
            for node in selObjs:
                newName = node.split('|')[-1].replace(searchStr, newStr)
                py.rename(node, newname)
    
def upperCase(*arg):
    '''
        Uppercase for all of selected nodes's name 
    '''
    selObjs = py.ls(sl =True)
    for obj in selObjs:
        py.rename(obj, obj.upper())
            
def lowerCase(*arg):
    '''
        Lowercase for all of selected nodes's name 
    '''
    selObjs = py.ls(sl =True)
    for obj in selObjs:
        py.rename(obj, obj.lower())
        
def upperCaseOnFirstLetter(*arg):
    '''
        Uppercase for first letter of all selected nodes's name 
    '''
    selObjs = py.ls(sl = True)
    for obj in selObjs:
        # -- option 1:
        newName = '_'.join(j[0].upper() + j[1:] for j in obj.split('_'))
        # -- option 2:
        # newName = obj.title()
        py.rename(obj, newName)

def selectNode(param):
    '''
        Select nodes match with RegExp
    '''
    py.select(param)
    selObjects = py.ls(sl = True)
    message = 'Co ' + str(len(selObjects)) + ' object duoc chon.'
    QtGui.QMessageBox.Information(None,'Information', message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
    
def execute(afunc):
    @wraps
    def wrapper(*args, **kwargs):
        return afunc(*args, **kwargs)
    return wrapper
    

        
        