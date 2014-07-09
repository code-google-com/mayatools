# Author: THO HOANG - GlassEgg Digtal Media
# Date: 1-1-2014

#from array import *

import maya.OpenMayaUI as OpenMayaUI
import inspect, os, sys
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as OpenMayaUI
import sip
import functools
import imp
from xml.dom import *
from xml.dom.minidom import *
import xml.etree.ElementTree as ET
# String
smtp= []
port = []
mail = []
password = []
 
#import MySQLdb
from MODULE.ShaderTools import ShaderTools as st
reload(st)

from MODULE.PolyTools import PolyTools as pt
reload(pt)

import CommonFunctions as cf
reload(cf)

import dockWidget as dW
reload(dW)

import Source.IconResource_rc
reload(Source.IconResource_rc)

import getShaderATG
reload(getShaderATG)

import CommonFunctions
reload(CommonFunctions)


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
fileDirCommmon1 = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
dirUI= fileDirCommmon +'/UI/ConfigureForm.ui'
# XML File
xmlDir = os.path.split(os.path.split(fileDirCommmon1)[0])[0] + '/Developer/Project/IronMonkey/XMLfiles/MailList.xml'
try:
   form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)
        
def writeXML(xmlFile,content,newPass):
    xmlDoc = xml.dom.minidom.parse(xmlFile)
    root = xmlDoc.firstChild
    datatree=''
    #tree = ET.parse(xmlFile)
    #root = tree.getroot()
    listNodes = root.getElementsByTagName(content)[0]
    for d in listNodes.childNodes:
        name = d.nodeName
        #print 'Ten Node: '
        #print name
        if name =='Pass':
            print 'Note Data'
            print d.childNodes[0].data
            d.firstChild.nodeValue  = newPass
            #datatree = d.childNodes[0].data
            #d.removeAttribute(name)
            #d.setAttribute('Pass',newPass)
            #d.writexml(f)
    xml_file = open(xmlFile,'w')
    xmlDoc.writexml(xml_file,encoding="utf-8")
    xml_file.close() 
    #return datatree
    #saveXML(self,None)
        
def saveXML(self,where =None):
    if not where:
        self.root.save()
    else:
        self.rote.save(where,self.node)

def loadXML(xmlFile, content, proper):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        #print 'XU LY FILE XLM '
        root = xmlDoc.firstChild
        listNodes = root.getElementsByTagName(content)[0]
        for d in listNodes.childNodes:
            name = d.nodeName
            if name == "Mail":
                kit.append(d.childNodes[0].data)
                
            elif name == "Smtp":
                kit.append(d.childNodes[0].data)
                
            elif name == "Port":
                kit.append(d.childNodes[0].data)
                
            elif name == 'Pass':
                kit.append(d.childNodes[0].data)
                
        return kit

class ConfigForm(form_class,base_class):
    def __init__(self,parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        
        self.btnOK.clicked.connect(functools.partial(self.updateXMLFile,xmlDir))
        # load xml
        
        
        print 'xlm Dir'
        print xmlDir
        #from_ad = loadXML(xmlDir,'Smtp_config','Smtp')
        #to_ad = loadXML(xmlDir,'Producer','mail')
        smtp = loadXML(xmlDir,'Smtp_config','Smtp')
        print 'SMTP: '
        print smtp
        self.txtSMTP.setText(smtp[0])
        self.txtPort.setText(smtp[1])
        
        mail = loadXML(xmlDir,'Configuration','Mail')
        print 'Configuration: '
        print mail
        self.txtMail.setText(mail[0])
        self.txtPassword.setText(mail[1])
        
        #newPass = self.txtPassword.text()
        #test = writeXML(xmlDir,'Configuration',newPass)
        #print 'gia tri test'
        #print test
        
    def updateXMLFile(self,xmlDir):
        # UPDATE XML FILE
        newPass = self.txtPassword.text()
        print 'Password moi: '
        print newPass
        writeXML(xmlDir,'Configuration',newPass)                    
