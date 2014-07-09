
description = 'Check file Text is wrong.'
name = 'Checkfiletextiswrong'
import os, sys, inspect, re, shutil
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import sys

def Check2Space(line):
    matches = re.findall(r'\s+', line.strip())
    return not any(m for m in matches if m != '  ')
def isDoubleSpace(line):
    #return '  '.join(line.split())== line.strip()
    #re.sub( '\line{2,}', ' ', line ).strip()
    #line.strip()
    #while '  ' in line:
    #    line = line.replace('  ', '')
    tem = line.split('  ')
    if len(tem)>1:
        QtGui.QMessageBox.critical(None,'Multiple whitespace','Co nhieu hon 2 khoang trang trong: '+ line,QtGui.QMessageBox.Ok)

def execute():
    print '--------------- CHECK TEXT FILE WRONG-------------------------'
    lines = list()
    new_lines = []
    fileName = os.path.splitext(cmds.file(q= True, sn = True))[0]
    folderName = os.path.split(cmds.file(q= True, sn = True))[0]
    #car_name= cmds.file(q= True, sn = True).split('/')[-1].split('.')[0]
    #car_namelocal = os.path.splitext(cmds.file(q= True, sn = True))[0]
    print('File Name: ',fileName)
    print('Folder Name: ',folderName)
    MayaFile = fileName.split('/')[-1]
    headlight = folderName + '/' + 'headlight' + '.txt'
    print headlight
    if os.path.isfile(headlight):
        file = open(headlight,'r')
        lines = file.readlines()
        i= 0
        for line in lines:
            #2space = Check2Space(line)
            i=i+1
            print'----------------Bat dau------'
            print line
            print"______________"
            if Check2Space(line) is True:
               QtGui.QMessageBox.critical(None,'Line whitespace','Dong thu: '+ str(i) + ' khong co noi dung.',QtGui.QMessageBox.Ok)
            
            isDoubleSpace(line)
            print"+++++++++++++++++++++++"
            print line
            print'----------------Ket Thuc------'
            '''
            for line in sys.stdin:
                if not re.match(r'(?:\S|(?<!\s)  (?!\s))*$', line):
                    print(repr(line)) # failed
            '''
            #ok = re.match(r'(?:\S|(?<!\s)  (?!\s))*$', line)
            #print('Ok: ',)
            #if not line.strip():
                #continue
            #else:
                #new_lines.append(line)
        #for li in new_lines:
        #    print('Cac dong co khoang trong: ',li)
         
    