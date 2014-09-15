import maya.mel as mel
import os
from developer.main.common import commonFunctions as cf

icon = cf.getPath(__file__, 1) + '/icons/froXnormal.png'
tooltip = 'Dung XNormal de bake normal. Can install XNormal de su dung.'

def main():
    dir = (cf.getPath(__file__, 2) + '/fn/mel/froXnormal').replace('\\','/')
    mel.eval('source \"{path}\";'.format(path = dir))
    mel.eval('froXno();')