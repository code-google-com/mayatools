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
################################### IMPORT MAIL #####################
################################### IMPORT MAIL #####################
import smtplib
# Here are the email package modules we'll need

from optparse import OptionParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

################################## END IMPORT MAIL #################################
f1_dir =[]
f2_dir=[]
tempDir = []
published_dir = 'C:/development/marmoset/app/res/published/data/car_descriptions'
master_dir = 'C:/development/marmoset/app/res/master/data/car_descriptions'
#serverPath = '//glassegg.com/Scenes/RR_2014/To_Client/Today'
serverPath = 'T:/Scenes/RR_2014/To_Client/Today'
clientPath ='Z:/Project/RR_2014/Cars/'

    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def loadXML(xmlFile, content, proper):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        listNodes = root.getElementsByTagName(content)[0]
        for d in listNodes.childNodes:
            name = d.nodeName
            if name == "mail":
                kit.append(d.childNodes[0].data)
                
        #dir = ProjectNode.getElementsByTagName(kitNodes)[0]
        #kit = [x.getAttribute(proper) for x in kitNodes]
        #kit.append([x.getAttribute('shortname') for x in kitNodes])
        return kit
def sendMailHTML(from_ad,to_ad,car_folder):
    #xmlDir = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/MailList.xml'
    # THONG SO GUI MAIL
    smtpserver='gemail01.glassegg.com'
    #from_ad = 'thohoang@glassegg1.com'
    #to_ad ='duynguyen2@glassegg.com'
    #to_ad = loadXML(xmlDir,'Tech','mail')
    #print 'DANH SACH MAIL NE PA CON'
    #print to_ad
    
    #cc_ad = 'thohoang@glassegg.com'
    #subject = 'How are you?'
    #message = ' Di nhau de anh em :D'
    login = 'thohoang@glassegg1.com'
    password ='abc123'
    #password ='S#CpkG$TT'
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "GUI SAN SAN PHAM CHO KHACH HANG"
    msg['From'] = from_ad
    msg['To'] = ', '.join(to_ad)
    #smtpserver = 'secure.emailsrvr.com:465'
    
    
    # Create the body of the message (a plain-text and an HTML version).
    text = "Xin chao!\nSan pham da duoc kiem tra, Producer co the gui cho khach hang. Thanks!"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Xin chao!<br>
           San pham da duoc kiem tra va duoc luu tru theo duong dan ben duoi:<br>
           <h3>{car_folder}</h3>
           Producer co the gui cho khach hang. Thanks!
           <br>
           <br>
           Technical Group !
        </p>
      </body>
    </html>
    """.format(car_folder=car_folder)    
    #s = Template(html).safe_substitute(code="We Says Thanks!")
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    # Send the message via local SMTP server.
    server = smtplib.SMTP(smtpserver,25)
    server.login(login,password)
    #for m in to_ad:
    server.sendmail(from_ad, to_ad, msg.as_string())
    #server.quit()
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    server.quit()
def execute():
    
    ##################################################
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
    
    #--------------SEND MAIL TO PRODUCER
    xmlDir = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/MailList.xml'
    from_ad = 'thohoang@glassegg1.com'
    to_ad = loadXML(xmlDir,'Producer','mail')
    print 'SEND MAIL DI'
    print to_ad
    sendMail = sendMailHTML(from_ad,to_ad,car_folder)
    
