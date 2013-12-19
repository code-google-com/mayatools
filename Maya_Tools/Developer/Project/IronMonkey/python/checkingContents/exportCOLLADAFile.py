description = 'Export collada file.'
name = 'fixUvSet'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os
from PyQt4 import QtGui

car_dir = 'E:/Project/RR_2014/marmoset/app/res/master/textures/cars/'
common_dir = car_dir + 'common/'

def execute():
    print '--------------- ASSIGN TEXTURES TO CORRECT PATH-------------------------'

    