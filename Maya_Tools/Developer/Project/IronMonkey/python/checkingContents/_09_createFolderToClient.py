description = 'Create copy To client.'
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
#serverPath = '//glassegg.com/Scenes/RR_2014/To_Client/Today'
serverPath = 'T:/Scenes/RR_2014/To_Client/Today'
clientPath ='Z:/Project/RR_2014/Cars/'
        
def execute(self):
    file1=[]
    localFolder=[]
    #tempDir = []
    print '--------------- Create Copy To Client ------------------------'
    mel.eval('showHidden -all;')
    # Get Carname
    car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    car_folder = serverPath +'/'+ car_name
    
    f1_dir = published_dir +'/'+car_name +'.sb'
    #file1 = f1_dir.split('/',2)
    #path,file = os.path.split(f1_dir)
        
    f2_dir = master_dir +'/'+car_name +'.sx'
   
   
    if not os.path.exists(car_folder):
        os.makedirs(car_folder)
    
    if os.path.dirname(f1_dir):
        tempDir = 'marmoset/app/res/published/data/car_descriptions/'    
        dstdir = os.path.join(car_folder, os.path.dirname(tempDir))
        #print 'dstdir'
        #print dstdir
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        shutil.copy(f1_dir, dstdir)
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please import car to Collada before copy file.',QtGui.QMessageBox.Ok)
     
    if os.path.dirname(f2_dir):
        temDir2 = 'marmoset/app/res/master/data/car_descriptions/'
        dstdir2 = os.path.join(car_folder, os.path.dirname(temDir2))
        #print 'dstdir2'
        #print dstdir2
        if not os.path.exists(dstdir2):
            os.makedirs(dstdir2)
        shutil.copy(f2_dir, dstdir2)
    else:
        QtGui.QMessageBox.critical(None,'Wrong car name','Please import car to Collada before copy file.',QtGui.QMessageBox.Ok)

    carPath = clientPath + car_name
    carName_copy = carPath + '/' + 'maya' +'/'+'car'+'/'+'lod00' +'/'+ car_name +'.mb'
    if os.path.isfile(carName_copy):
        shutil.copy(carName_copy,car_folder)
    
    
