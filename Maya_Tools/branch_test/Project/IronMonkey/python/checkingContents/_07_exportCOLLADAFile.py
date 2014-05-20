description = 'Export collada file.'
name = 'fixUvSet'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os
from PyQt4 import QtGui
import subprocess as s

model_dir = 'C:/development/marmoset/app/res/master/models/cars/'
prefab_dir = 'C:/development/marmoset/app/res/master/prefabs/cars/'
build_file = 'C:/development/marmoset/scripts/Windows/build_all.bat'

def execute():
    cmds.loadPlugin('COLLADA.mll') 
    print '--------------- Export Collada files ------------------------'
    mel.eval('showHidden -all;')
    car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    f_dir = model_dir + car_name
    if os.path.isdir(f_dir):
        cmds.select('car')
        cmds.file(f_dir + '/' + car_name + '.dae', type = 'COLLADA exporter', es = True, f = True)
        # master if dae
        os.system('{b_f} {s_f}'.format(b_f = build_file, s_f = f_dir + '/' + car_name + '.dae'))
        # master prefab file
        os.system('{b_f} {s_f}'.format(b_f = build_file, s_f = prefab_dir + '/' + car_name + '.prefabs.xml'))
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please correct filename following asset name.',QtGui.QMessageBox.Ok)
    