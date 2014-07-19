import inspect, os

import maya.mel as mel


description = 'FCO on scene.'
tooltip = ''

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- FCC-------------------------'
    attachFileSource = fileDirCommmon + '/geNFS14_FixCorruptObject.mel'
    mel.eval('source \"{f}\";'.format(f = attachFileSource))
    mel.eval('geNFS14_FixCorruptObjectGUI();')