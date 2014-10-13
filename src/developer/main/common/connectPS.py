
import maya.cmds as cmds
import shutil, os, sys

try:
    os.makedirs('C:/pythonNet')
except: 
    pass
sys.path.append(r'C:\pythonNet')

shutil.copyfile(r'\\glassegg.com\tools\TECHNICAL_SCRIPT\Projects\MayaToolSystem\MAYA_2014\clr.pyd', r'C:\pythonNet\clr.pyd')
shutil.copyfile(r'\\glassegg.com\tools\TECHNICAL_SCRIPT\Projects\MayaToolSystem\MAYA_2014\Python.Runtime.dll', r'C:\pythonNet\Python.Runtime.dll')
shutil.copyfile(r'\\glassegg.com\tools\TECHNICAL_SCRIPT\Projects\MayaToolSystem\MAYA_2014\psrc.dll', r'C:\pythonNet\psrc.dll')

import clr, sys, _winreg
clr.AddReference('psrc')
from psrc import PSObject

def openJSFile():
    exp = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Adobe\Photoshop\60.0')
    path = _winreg.QueryValueEx(exp, 'ApplicationPath')[0]
    fOpen = cmds.fileDialog2(startingDirectory  = path, fileFilter='JavaScript (*.js *.jsx)', fm = 1)
    return fOpen
    
def connectToPS(path):
    ps = PSObject()
    ps.executeJSScript(path)
    
def main():
    path = openJSFile()[0]
    connectToPS(path)
    
main()

