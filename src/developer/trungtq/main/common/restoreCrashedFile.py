import os
import os.path
import sys
import time
import maya.cmds as cmds
 
print '[checkRestored]Triggered!'
 
tmps=[]
 
borderMin = 1 # Ask if tmp file is newer than this
 
# Get environments #
if sys.platform.startswith('win'):
    if os.environ.has_key('TMP'):# windows 1
        tmps += os.environ['TMP'].split(';')
    if os.environ.has_key('TEMP'):# windows 2
        tmps += os.environ['TEMP'].split(';')
else:
    if os.environ.has_key('TMPDIR'):# Linux
        tmps += os.environ['TMPDIR'].split(':')
 
res = {}
for tmp in tmps: # Parse all tmp direcotrys
    for file in os.listdir(tmp): # Parse all files in there
        if file.endswith('.ma'): # Only ma files
            # Store into res dic.
            # Key is unix time stamp, value is filePath
            difSec = time.time() - os.path.getmtime(tmp+os.sep+file)
            res[str(difSec).split('.')[0].zfill(16)]=tmp+os.sep+file
 
latestKey = sorted(res.iterkeys())[0]
 
if int(latestKey)&lt;borderMin*60:
    yesno = cmds.confirmDialog(
        title='Confirm',
        message='Tmp file detected. Do you want to open this?\n'+res[latestKey],
        button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if yesno=='Yes':
        print res[latestKey]
        cmds.file( res[latestKey], o=True, f=True )
 
print '[checkRestored] Done.'