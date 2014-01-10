description = 'Create To Client.'
name = 'fixUvSet'
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import distutils.core
import os, sys, re, inspect , imp, shutil
from xml.dom.minidom import *
from PyQt4 import QtGui, QtCore, uic
import subprocess as s
f1_dir =[]
f2_dir=[]
tempDir = []
published_dir = 'C:/development/marmoset/app/res/published/data/car_descriptions'
master_dir = 'C:/development/marmoset/app/res/master/data/car_descriptions'
localPath = 'Z:/Project/RR_2014'

        
def execute(self):
    file1=[]
    localFolder=[]
    #tempDir = []
    print '--------------- Export Collada files ------------------------'
    mel.eval('showHidden -all;')
    # Get Carname
    car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    #get LocalPath
    #LocalPath = readXMLFile(xmlDir)
    localFolder = localPath +'/'+ 'Cars'+'/'+ car_name +'/'+'To_Client'
    f1_dir = published_dir +'/'+car_name +'.sb'
    file1 = f1_dir.split('/',2)
    path,file = os.path.split(f1_dir)
    

    
    f2_dir = master_dir +'/'+car_name +'.sx'
    print 'file1'
    print file1
    print 'duong dan thu muc'
    print localFolder
    print'file collada F1:'
    print f1_dir
    print 'f2_dir'
    print f2_dir
    
    if not os.path.exists(localFolder):
        os.makedirs(localFolder)
    
    if os.path.dirname(f1_dir):
        tempDir = 'marmoset/app/res/published/data/car_descriptions/'    
        dstdir = os.path.join(localFolder, os.path.dirname(tempDir))
        print 'dstdir'
        print dstdir
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        shutil.copy(f1_dir, dstdir)
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please import car to Collada before copy file.',QtGui.QMessageBox.Ok)
     
    if os.path.dirname(f1_dir):
        temDir1 = 'marmoset/app/res/master/data/car_descriptions/'
        dstdir2 = os.path.join(localFolder, os.path.dirname(temDir1))
        print 'dstdir2'
        print dstdir2
        if not os.path.exists(dstdir2):
            os.makedirs(dstdir2)
        shutil.copy(f2_dir, dstdir2)
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please import car to Collada before copy file.',QtGui.QMessageBox.Ok)
         
