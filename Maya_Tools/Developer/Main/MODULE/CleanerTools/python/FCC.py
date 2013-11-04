import inspect, os
import maya.mel as mel

description = 'FCC on seelcted node'
name = 'FCC'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- FCC-------------------------'
    attachFileSource = os.path.split(fileDirCommmon)[0] + '/mel/geNFS14_SpecialFCCOnSelectedMeshes.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))