'''
Created on Jul 20, 2014

@author: Trung
'''

import maya.mel as mel
import os
from developer.main.common import commonFunctions as cf

def main():
    dir = cf.getPath(__file__, 2) + '/sourcecode/mel/ddoMaterialManager_2013'
    mel.eval('source \"{path}\";'.format(path = dir))
    mel.eval('materialManager();')