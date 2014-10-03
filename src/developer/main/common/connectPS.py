import clr, sys, _winreg
import maya.cmds as cmds
sys.path.append(r'Z:\ge_Tools\psrc\bin\Release')
clr.AddReference('psrc')
from psrc import PSObject

def openJSFile():
    exp = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Adobe\Photoshop\80.0')
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
    

