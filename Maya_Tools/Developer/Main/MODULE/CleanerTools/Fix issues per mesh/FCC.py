import inspect, os
import maya.mel as mel

description = 'FCC on selected node.'
name = 'FCC'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- FCC-------------------------'
    attachFileSource = fileDirCommmon + '/geNFS14_SpecialFCCOnSelectedMeshes.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))