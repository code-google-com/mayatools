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
build_file = 'C:/development/marmoset/scripts/Windows/build_add.bat'

def execute():
    print '--------------- Export Collada files ------------------------'
    car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    f_dir = model_dir + car_name
    if os.path.isdir(f_dir):
        cmds.select('car')
        cmds.file(f_dir + '/' + car_name + '.dae', type = 'COLLADA exporter', es = True, f = True)
        # master if dae
        p = s.Popen([build_file, f_dir + '/' + car_name + '.dae'], stdout = PIPE, stderr=PIPE)
        output, errors = p.communicate() 
        p.wait()
        # master prefab file
        p = s.Popen([build_file, f_dir.replace(model_dir, prefab_dir) + '/' + car_name + '.prefabs'], stdout = PIPE, stderr=PIPE)
        output, errors = p.communicate() 
        p.wait()
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please correct filename following asset name.',QtGui.QMessageBox.Ok)
    