import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *
import pyodbc
################################### IMPORT MAIL #####################
import smtplib
################################### IMPORT ZIP
import zipfile
# Here are the email package modules we'll need

from optparse import OptionParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

clientPath ='Z:/Project/RR_2014/Cars/TestCar'

COMMASPACE = ', '


description = 'Test Send Mail.'
name = 'senmailto'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def connetDatabase():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=GESVR05;DATABASE=Gem_Tools_Test;UID=geuser;PWD=Aa@123456')
    cursor = cnxn.cursor()
    cursor.execute("select Project_ID, Group_ID,Name from tbl_Asset")
    rows = cursor.fetchall()
    for row in rows:
        print "ID Project:"
        print row.Project_ID
        print "Group ID"
        print row.Group_ID
        print "Name"
        print row.Name
def toZip(directory):
    zippedHelp = zipfile.ZipFile(zip, "w", compression=zipfile.ZIP_DEFLATED )
    #print zippedHelp
 
    list = os.listdir(directory)
 
    for entity in list:
        print entity
        each = os.path.join(directory,entity)
 
        if os.path.isfile(each):
            print each
            zippedHelp.write(each,zipfile.ZIP_DEFLATED)
        else:
            addFolderToZip(zippedHelp,entity)
 
    zippedHelp.close()
 
def addFolderToZip(zippedHelp,folder):
 
    for file in folder:
            if os.path.isfile(file):
                zippedHelp.write(file, os.path.basename(file), zipfile.ZIP_DEFLATED)
            elif os.path.isdir(file):
                addFolderToZip(zippedHelp,file)

def zipfiles(dirCar,carName):
    print '..... ZIP ZIP ZIP .....'
    print dirCar
    zf = zipfile.ZipFile("ford_fiesta_b3.zip", "w")
    for dirname, subdirs, files in os.walk(dirCar):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
def loadXML(xmlFile, content, proper):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        listNodes = root.getElementsByTagName(content)[0]
        for d in listNodes.childNodes:
            name = d.nodeName
            if name == "mail":
                kit.append(d.childNodes[0].data)
            if name == "Smtp":
                kit.append(d.childNodes[0].data)
                
        #dir = ProjectNode.getElementsByTagName(kitNodes)[0]
        #kit = [x.getAttribute(proper) for x in kitNodes]
        #kit.append([x.getAttribute('shortname') for x in kitNodes])
        return kit
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              #smtpserver='smtp.gmail.com:587'):
              #smtpserver='gesvr01.glassegg.com:25'):
              smtpserver):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver,25)
    #server.ehlo()
    #server.starttls()
    #server.ehlo()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
def sendMailHTML(from_ad,to_ad):
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
    msg['Subject'] = "CHUONG TRINH NHAU NHET CUOI TUAN NHU THE NAO?"
    msg['From'] =','.join(from_ad) 
    msg['To'] = ', '.join(to_ad)
    #smtpserver = 'secure.emailsrvr.com:465'
    
    
    # Create the body of the message (a plain-text and an HTML version).
    text = "Xin chao!\nCuoi tuan nay ban co ranh khong?\nNeu ranh minh lam vai ly lai rai nhe. Thanks!"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Xin chao!<br>
           Cuoi tuan nay ban co ranh khong?<br>
          
           Neu ranh minh lam vai ly lai rai nhe. Thanks!
           <br>
           <br>
           Tho Hoang
        </p>
      </body>
    </html>
    """   
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
    #return problems
def execute():
      
    print '################## SEND MAIL ###########################'
    #--------------SEND MAIL TO PRODUCER
    #zipfiles(clientPath,'ford_fiesta_b3')
    #zip = "TestCar.zip"
    #print clientPath
    #toZip(clientPath)
    
    xmlDir = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/MailList.xml'
    print 'duong dan xml'
    print xmlDir
    from_ad = loadXML(xmlDir,'Smtp_config','Smtp')
    to_ad = loadXML(xmlDir,'Producer','mail')
    
    print 'NGUOI GUI MAIL:'
    print from_ad
    print 'SEND MAIL DI'
    print to_ad
    #sendMail = sendMailHTML(from_ad,to_ad)
    connetDatabase()
