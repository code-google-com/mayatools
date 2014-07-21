import maya.mel as mel
import os
from developer.main.common import commonFunctions as cf

icon = cf.getPath(__file__, 1) + '/icons/ddoMaterialManager_2013.png'
tooltip = 'Gan color ID dua theo tung loai chat lieu. Dung chung voi dDo tools.'

def main():
    dir = (cf.getPath(__file__, 2) + '/fn/mel/ddoMaterialManager_2013').replace('\\','/')
    mel.eval('source \"{path}\";'.format(path = dir))
    mel.eval('ddoManager();')