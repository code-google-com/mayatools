description = 'Assign textures to correct path.'
name = 'fixUvSet'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os
from PyQt4 import QtGui
import shutil

textures_dir = 'C:/development/marmoset/app/res/master/textures/cars/'
build_file = 'C:/development/marmoset/scripts/Windows/build_all.bat'
common_dir = textures_dir + 'common/'

def execute():
    print '--------------- ASSIGN TEXTURES TO CORRECT PATH-------------------------'
    textures = py.ls(tex = True)
    car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    f_dir = textures_dir + car_name
    if os.path.isdir(f_dir):
        for t in textures:
            if 'common' in t.getAttr('fileTextureName'):
                new_dir = common_dir + t.getAttr('fileTextureName').split('/')[-1]
                t.setAttr('fileTextureName', new_dir, type='string')
            else:
                try:
                    new_dir = f_dir + '/' + t.getAttr('fileTextureName').split('/')[-1]
                    if not os.path.isfile(new_dir): # file texture not in engine folder
                        shutil.copyfile(t.getAttr('fileTextureName'), str(new_dir))
                        os.system('{b_f} {s_f}'.format(b_f = build_file, s_f = new_dir))
                    t.setAttr('fileTextureName', new_dir, type='string')    
                except:
                    pass
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please correct filename following asset name.',QtGui.QMessageBox.Ok)
    