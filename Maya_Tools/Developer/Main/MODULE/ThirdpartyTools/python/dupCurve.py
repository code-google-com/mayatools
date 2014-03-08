'''
Chris Zukowski
Duplicate Along Curve Script

Copy and Paste this section of code to run

import dupCurve
reload(dupCurve)
dupCurve.gui()


INFO ON EACH FUNCTION

gui:
	The main GUI that starts the window.
	
layout:
	The main layout that.
	
fnRefreshGUI:
	Deletes the UI and restarts layout.
	
fnAutoUpdateOn:
	Selects CV's and creates individual script jobs for them based on 
	modifying its attributes
	
fnAutoUpdateOff:
	Kills all script jobs
	
fnRepSelected:
	If DupCurve has already been executed... this will use the same objects
	and run DupCurve again.
	
fnDupCurve:
	Takes a selected object on a motion path and duplicates it every frame.
	CURVE MODES
		1. Adjust Curve time
			- takes whatever frame value and makes that how many 
			  frames the curve is.
		2. Auto Distance Mode
			- Finds the objects largest height/width/length based 
			  off of which up axis is activated for that curve and 
			  equally distributes the object along the curve.
		3. Chain Mode
		        - Every other object gets rotated 90 degress after being
		          equally distributed along the curve.
		4. Equal Distance Mode
			- Use the field to tell the script how much distance
			  is between each object.
			 		
fnStarterCurve:
	Creates a curve that acts as a good starting point for people who just
	want to test the script out. You can use any other curve form.
	
fnAttach:
	Attach selected object to selected curve.

fnAvg:
	Find height/width/length of object.

fnError1:
	Tells user to select an object on a motion path first.
	
fnControlVertex:
	selects all control paths of curves that contain a motion path.
	
fnCreateMotionMenu:
	Generate the menu based on the number of motion paths and their values
	
fnSetMotionAttr:
	Apply all attributes to all motion paths.


'''



import maya.cmds as cmds
import random
#Kills EVERYTHING!!!
cmds.scriptJob(ka=True,f=True)
AutoUpdate=0


selected = "default"

global AutoUpdate
AutoUpdate=0

global window
window = "dupCurve"

global runOnce
runOnce=0
if( cmds.window("dupCurve", ex=True)):
	cmds.deleteUI("dupCurve")

	

RBSpecialModes="None"
Distance=4

def main():
    gui()


#_____________________________MAIN GUI_____________________________________#

def gui(*arg):
	global window
	window = "dupCurve"
			

	if( cmds.windowPref(window, ex=True)):
		cmds.windowPref(window, r=True)		
		
	cmds.window(window, title="Duplicate Along Curve", w=240, h=400)
	
	
	cmds.scrollLayout('sindex1',p="dupCurve")
	cmds.frameLayout('sindex',l="",w=215 )
	
	layout()
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	
	
	cmds.showWindow(window)
	
#_____________________________MAIN LAYOUT_____________________________________#

def layout(*arg):
	
	cmds.columnLayout('dupIndex',w=215,adj=True, p="sindex")	
	
	global maxTime
	maxTime=cmds.playbackOptions(q=True, maxTime=True)

	cmds.rowColumnLayout('RCL1',nc=2,p="dupIndex",w=215)
	cmds.button('dupCurve', label="    Dup Curve   ", c=fnDupCurve)
	cmds.button('selObjectRep', label="Repeat Dup Curve", c=fnRepSelected)
	cmds.text(l="Num Frames")
	cmds.intField('iNumFrames',v=maxTime)
	cmds.setParent( '..' )
	
	#_____________________________SPECIAL MODES_____________________________________#
	
	cmds.frameLayout('FL1', label='Special Modes', cll=True, borderStyle='in',bgc=[0.150,0.232,0.333], p="dupIndex",w=196 )
	cmds.columnLayout('CL1',w=215)
	
	cmds.radioCollection("RBSpecialModes")
	cmds.radioButton('None', label='None' )
	cmds.radioButton('AdjustCurve', label='Adjust Curve Time' )
	cmds.radioButton('ChainMode', label='Chain Mode' )
	cmds.radioButton('EqualDistance', label='Equal Distance Mode' )
	cmds.radioCollection( "RBSpecialModes", edit=True, select=RBSpecialModes )
	cmds.floatField('iDistance',  v=Distance)
	
	cmds.setParent( '..' )
	cmds.setParent( '..' )

	#________________________STARTER BUTTONS________________________________________#

	cmds.frameLayout('FL2', label='Extra Helpers', cll=True, borderStyle='in',bgc=[0.150,0.232,0.333] )
	cmds.rowColumnLayout('RCL3',nc=2)
	
	cmds.button('StarterCrv', label="Starter Curve", c=fnStarterCurve)
	cmds.button('AttachCrv', label="Attach To Curve", c=fnAttach)
	if (AutoUpdate==0):
		cmds.button('AuOn', label="Auto Update is 'Off'", c=fnAutoUpdateOn)
	else:
		cmds.button('AuOff', label="Auto Update is 'On'", c=fnAutoUpdateOff)
	cmds.button('ControlVertex', label="Control Vertex", c=fnControlVertex)
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	
	#________________________MOTION CURVES___________________________________________#
	

	cmds.frameLayout('FL3', label='Motion Paths', cll=True,cl=False, borderStyle='in',bgc=[0.150,0.232,0.333] )
	cmds.columnLayout('CL',w=215)

	
	
	fnCreateMotionMenu()
	

#_______________________________REFRESH GUI___________________________________________#


def fnRefreshGUI(*arg):
	cmds.select(cl=True)

	cmds.deleteUI("dupIndex",lay=True)
	layout()	
	
#_______________________________AUTO UPDATE ON___________________________________________#

def fnAutoUpdateOn(*arg):
	selected2=cmds.ls(sl=True)
	print("AutoUpdate is On")
	global AutoUpdate
	AutoUpdate=1
	
	#start the curve process
	
	mPath=cmds.ls(typ="motionPath")
	crv=cmds.listConnections(mPath,type="nurbsCurve")
	numCrv=len(crv)
	CCrv=0
	for index in range(0,numCrv):
		
		crvName=crv[CCrv]
		slCCrv=crvName+".cv[0:1000]"
		cmds.select(slCCrv)
		cv=cmds.ls(sl=True)
		cv=cv[0]
		rtLencv=len(cv)
		lfLencv=len(crvName)
		rtcv=rtLencv-1
		lfcv=lfLencv+6
		FNumCv=cv[lfcv:rtcv]
		numCv=0                  
		for index2 in range(0,int(FNumCv)):
			cmds.scriptJob( ac=[crvName+".cv["+str(numCv)+"]", fnRepSelected])
			numCv=numCv+1 
		CCrv=CCrv+1
	fnRefreshGUI()
	cmds.select(selected2)
	
#_______________________________AUTO UPDATE OFF___________________________________________#

def fnAutoUpdateOff(*arg):
	print("AutoUpdate is off")
	global AutoUpdate
	AutoUpdate=0 
	cmds.scriptJob( ka=True, f=True)
	fnRefreshGUI()

#_______________________________REPEAT SELECTED___________________________________________#

def fnRepSelected(*arg):
	error=[]
	if(selected==error):
		fnError1()
	lastSelected=cmds.ls(sl=True)
	if(selected == "default"):
		fnError1()
	else:
		cmds.select(selected)
		fnDupCurve()

		
		cmds.select(selected)
		objType=cmds.objectType(lastSelected)
		if(objType=="nurbsCurve"):
			mPath=cmds.ls(typ="motionPath")
			crv=cmds.listConnections(mPath,type="nurbsCurve")
			cmds.hilite(crv)
			cmds.selectType(ocm=True,alc=False)
			cmds.selectType(ocm=True,cv=True)
			cmds.select(lastSelected)
		else:
			cmds.select(lastSelected)
			
#_______________________________DUPLICATE ALONG CURVE___________________________________________#

def fnDupCurve(*arg):
	
	numFrames=cmds.intField('iNumFrames', q=True, v=True)
	global RBSpecialModes
	RBSpecialModes=cmds.radioCollection("RBSpecialModes", q=True, sl=True)
	global Distance
	Distance=cmds.floatField('iDistance', q=True, v=True)


	
	
	global selected
	selected=cmds.ls(sl=True)
	error=[]
	if(selected==error):
		fnError1()
	

	if(selected == "default"):
		fnError1()
	else:	
		selected=cmds.ls(sl=True)
		print(selected)
		fnSetMotionAttr()
		mPath=[]
		for i in range(0,len(selected)):
			mPathUS=cmds.listConnections(selected[i], type="motionPath")
			mPathUS = (list(set(mPathUS)))
			mPathUS = str(mPathUS)
			mPathUS = mPathUS[3:-2]
			mPath.append(mPathUS)
		

		if(RBSpecialModes=="AdjustCurve"):
			mPathCount=0
			for index in range(0,len(mPath)):
				cmds.select(mPath[mPathCount])
				
				kFrm=cmds.keyframe( mPath[mPathCount]+".u", time=(0,50000), query=True, timeChange=True)
				kFrmFt=cmds.keyframe( mPath[mPathCount]+".frontTwist", time=(0,50000), query=True, timeChange=True)
				kFrmUt=cmds.keyframe( mPath[mPathCount]+".upTwist", time=(0,50000), query=True, timeChange=True)
				kFrmSt=cmds.keyframe( mPath[mPathCount]+".sideTwist", time=(0,50000), query=True, timeChange=True)
				
				print(kFrm[-1])
				print(numFrames)
				
				cmds.keyframe( mPath[mPathCount]+".u", time=(kFrm[-1],kFrm[-1]), timeChange=numFrames)
				cmds.keyframe( mPath[mPathCount]+".frontTwist", time=(kFrmFt[-1],kFrmFt[-1]), timeChange=numFrames)
				cmds.keyframe( mPath[mPathCount]+".upTwist", time=(kFrmUt[-1],kFrmUt[-1]), timeChange=numFrames)
				cmds.keyframe( mPath[mPathCount]+".sideTwist", time=(kFrmSt[-1],kFrmSt[-1]), timeChange=numFrames)
				mPathCount=mPathCount+1
				
			cmds.playbackOptions(maxTime=numFrames)
			global maxTime
			maxTime=numFrames
			cmds.select(selected)
			
		if RBSpecialModes in ["EqualDistance","ChainMode","AutoDistance"] :
			
			mPathCount=0
			numFrames2=[]
			for index in range(0,len(mPath)):
				crv=cmds.listConnections(mPath,type="nurbsCurve")
				crv=crv[mPathCount]
				crvLength=cmds.arclen(crv,ch=False)
				if(RBSpecialModes=="AutoDistance"):
					fnAvg()
					UpAxis=cmds.getAttr(mPath[index]+".upAxis")
					print("----")
					print(UpAxis)
					print("----")
					if(UpAxis==0):
						Distance=finX[mPathCount]
					elif(UpAxis==1):
						Distance=finY[mPathCount]
					elif(UpAxis==2):
						Distance=finZ[mPathCount]
				numFrames=int(crvLength/Distance)
				cmds.select(mPath[mPathCount])
				
				kFrm=cmds.keyframe( mPath[mPathCount]+".u", time=(0,500000), query=True, timeChange=True)
				if (RBSpecialModes=="ChainMode"):
					print("")
				else:
					kFrmFt=cmds.keyframe( mPath[mPathCount]+".frontTwist", time=(0,50000), query=True, timeChange=True)
					kFrmUt=cmds.keyframe( mPath[mPathCount]+".upTwist", time=(0,50000), query=True, timeChange=True)
					kFrmSt=cmds.keyframe( mPath[mPathCount]+".sideTwist", time=(0,50000), query=True, timeChange=True)
					
				cmds.keyframe( mPath[mPathCount]+".u", time=(kFrm[-1],kFrm[-1]), timeChange=numFrames)
				if (RBSpecialModes=="ChainMode"):
					print("")
				else:
					cmds.keyframe( mPath[mPathCount]+".frontTwist", time=(kFrmFt[-1],kFrmFt[-1]), timeChange=numFrames)
					cmds.keyframe( mPath[mPathCount]+".upTwist", time=(kFrmUt[-1],kFrmUt[-1]), timeChange=numFrames)
					cmds.keyframe( mPath[mPathCount]+".sideTwist", time=(kFrmSt[-1],kFrmSt[-1]), timeChange=numFrames)
				cmds.playbackOptions(maxTime=numFrames)
				mPathCount=mPathCount+1
				numFrames2.append(numFrames)
			global maxTime
			maxTime=numFrames
			cmds.select(selected)
				

	counter=1
	
	selLen=len(selected)
	selCounter=0
	
	for mp in range(0, len(mPath)):
		cmds.keyTangent( mPath[mp], inTangentType='linear',ott='linear', time=(0,500000) )
	
	for index2 in range(0,selLen):
		if cmds.objExists("DC_"+selected[selCounter]+"_1"):
			cmds.select( "DC_"+selected[selCounter]+"_*" )
			cmds.delete()
		if(RBSpecialModes=="ChainMode"):
			chVal=0

			for index in range(0,numFrames2[selCounter]):
				cmds.select(selected[selCounter])
				cmds.currentTime(counter, edit=True)
				cmds.duplicate(rr=True)
				cmds.rename("DC_"+selected[selCounter]+"_"+str(counter))
				
				cmds.select(mPath[selCounter])
				cmds.setAttr(mPath[selCounter]+".ft", chVal)
				cmds.setKeyframe(mPath[selCounter]+".ft")
				
				if(chVal==0):
					chVal=90
				else:
					chVal=0
				counter=counter+1
				
		elif RBSpecialModes in["EqualDistance","AutoDistance"]:
			
			for index in range(0,numFrames2[selCounter]):
				cmds.select(selected[selCounter])
				cmds.currentTime(counter, edit=True)
				cmds.duplicate(rr=True)
				cmds.rename("DC_"+selected[selCounter]+"_"+str(counter))
				counter=counter+1	
			
		
		else:
			for index in range(0,numFrames):
				cmds.select(selected[selCounter])
				cmds.currentTime(counter, edit=True)
				cmds.duplicate(rr=True)
				cmds.rename("DC_"+selected[selCounter]+"_"+str(counter))
				counter=counter+1
				
		counter=1
		if(RBSpecialModes=="ChainMode"):
			print("")
			if cmds.objExists('orientationMarker*'):
				cmds.select("orientationMarker*")
				cmds.delete()
		
		selCounter=selCounter+1
	
	
	fnRefreshGUI() 
	cmds.select(selected)
	
	
	
	

#_______________________________STARTER CURVE___________________________________________#
	
def fnStarterCurve(*arg):
	cmds.curve( d=3, p=[(-30,0,0),(-26.5, 0,0),(-19.5, 0, 0), (0, 0, 0), (19.5, 0, 0), (30.5, 0, 0), (36, 0, 0)])

			
#_______________________________ATTACH TO CURVE__________________________________________#

def fnAttach(*arg):	
	cmds.AttachToPath()
			
#_______________________________FIND AVG L/W/H___________________________________________#

def fnAvg(*arg):
	tx=[]
	ty=[]
	tz=[]
	global finX
	global finY
	global finZ
	finX=[]
	finY=[]
	finZ=[]
	tCount=0
	if(selected == "default"):
		fnError1()
	else:
		objectName=selected
		for i in range(0,len(objectName)):
			cmds.select(objectName[i]+".vtx[0:500000]")
			tranVert=cmds.xform(q=True,t=True)
			
			for i2 in range(0,len(tranVert)/3):
				
				tx.append(tranVert[tCount])
				ty.append(tranVert[tCount+1])
				tz.append(tranVert[tCount+2])
				tCount=tCount+3
			finX.append(max(tx)-min(tx))
			finY.append(max(ty)-min(ty))
			finZ.append(max(tz)-min(tz))
			tCount=0
		
		


	cmds.select(objectName)

			
#_______________________________ERROR: 1___________________________________________#
	
def fnError1(*arg):
	cmds.confirmDialog( title='OMG', message='1. You need to select an object on a motion curve and click on the "Dup Curve" button.', button=['Ok'], defaultButton='Ok', cancelButton='No', dismissString='No' )	


			
#_______________________________SELECT CONTROL VERTEX IN SCENE______________________#

def fnControlVertex(*arg):
	mPath=cmds.ls(typ="motionPath")
	crv=cmds.listConnections(mPath,type="nurbsCurve")
	cmds.hilite(crv)
	cmds.selectType(ocm=True,alc=False)
	cmds.selectType(ocm=True,cv=True)
		
#_______________________________CREATE MOTION MENU_________________________________#		

def fnCreateMotionMenu(*arg):	
	mPath=cmds.ls(typ="motionPath")
	mPathList=[               
		"worldUpType",   	#0
		"worldUpVectorX",	#1
		"worldUpVectorY",	#2
		"worldUpVectorZ",	#3
		"inverseUp",	 	#4
		"inverseFront",  	#5
		"frontAxis",     	#6
		"upAxis",        	#7
		"frontTwist",    	#8
		"upTwist",       	#9
		"sideTwist",     	#10
		"bank",          	#11
		"bankScale",     	#12
		"bankLimit"]     	#13
	mAttr=[]
	global mAttrFull
	mAttrFull=[]
	global mPathUI
	mPathUI=[]	
	Add=0
	global AF
	AF=len(mPathList)
		

	for i in range(0,len(mPath)):
		
		for i2 in range(0,len(mPathList)):
			mAttr.append(cmds.getAttr(mPath[i]+"."+mPathList[i2]))
			mAttrFull.append(mPath[i]+"."+mPathList[i2])
			mPathUI.append(mPath[i]+mPathList[i2])
			
		cmds.frameLayout( label=mPath[i], cll=True, cl=True, borderStyle='in', bgc=[0.092,0.175,0.278],p="CL",w=215)
		cmds.columnLayout(w=186)

		
		cmds.optionMenuGrp(mPathUI[0+Add])
		cmds.menuItem('0', label='Scene Up' )
		cmds.menuItem('1', label='Object Up' )
		cmds.menuItem('2', label='Object Rotation Up' )
		cmds.menuItem('3', label='Vector' )
		cmds.menuItem('4', label='Normal' )
		cmds.optionMenuGrp(mPathUI[0+Add], edit=True, select=mAttr[0+Add]+1)
		
		cmds.text(l="World Up Vector")
		
		cmds.rowColumnLayout(nc=3, cw=[(1,70),(2,70),(3,70)])
		cmds.floatField(mPathUI[1+Add],  v=mAttr[1+Add],w=70)
		cmds.floatField(mPathUI[2+Add],  v=mAttr[2+Add],w=70)
		cmds.floatField(mPathUI[3+Add],  v=mAttr[3+Add],w=70)
		cmds.setParent( '..' )
		
		cmds.checkBox(mPathUI[4+Add], l="Inverse Up", v=mAttr[4+Add])
		cmds.checkBox(mPathUI[5+Add], l="Inverse Front", v=mAttr[5+Add])
		
		cmds.rowColumnLayout(nc=2, cw=[(1,105),(2,105)])
		cmds.text(l="Front Axis")
		cmds.optionMenuGrp(mPathUI[6+Add])
		cmds.menuItem('1', label='X' )
		cmds.menuItem('2', label='Y' )
		cmds.menuItem('3', label='Z' )
		cmds.optionMenuGrp(mPathUI[6+Add], edit=True, select=mAttr[6+Add]+1)
		
		cmds.text(l="Up Axis")
		cmds.optionMenuGrp(mPathUI[7+Add])
		cmds.menuItem('1', label='X' )
		cmds.menuItem('2', label='Y' )
		cmds.menuItem('3', label='Z' )
		cmds.optionMenuGrp(mPathUI[7+Add], edit=True, select=mAttr[7+Add]+1)
		cmds.setParent( '..' )

		cmds.rowColumnLayout(nc=3, cw=[(1,70),(2,70),(3,70)])
		cmds.text( l="Front Twist")
		cmds.text( l="Up Twist")
		cmds.text( l="Side Twist")
		cmds.floatField(mPathUI[8+Add], v=mAttr[8+Add])
		cmds.floatField(mPathUI[9+Add], v=mAttr[9+Add])
		cmds.floatField(mPathUI[10+Add],v=mAttr[10+Add])
		cmds.setParent( '..' )

		cmds.rowColumnLayout(nc=3, cw=[(1,70),(2,70),(3,70)])
		cmds.checkBox(mPathUI[11+Add], label="Bank",v=mAttr[11+Add])
		cmds.text(l="")
		cmds.text(l="")
		cmds.text( l="Bank Scale")
		cmds.text(l="")
		cmds.floatField(mPathUI[12+Add],v=mAttr[12+Add])
		cmds.text( l="Bank Limit")
		cmds.text(l="")
		cmds.floatField(mPathUI[13+Add],v=mAttr[13+Add])	
		
		
		
		
		cmds.setParent( '..' )
		cmds.setParent( '..' )
		cmds.setParent( '..' )
		Add=Add+AF
		
#_______________________________CREATE MOTION MENU_________________________________#		

def fnSetMotionAttr(*arg):
	numFrames=cmds.intField('iNumFrames', q=True, v=True)
	error=[]
	if(selected==error):
		fnError2()
	else:
		mPath=cmds.ls(typ="motionPath")
			

		global mPathAttrNew
		mPathAttrNew=[]
		Add=0
		if(mPathUI==mPathAttrNew):
			fnCreateMotionMenu()
			
		for i in range(0,len(mPath)):
			mPathAttrNew.append(cmds.optionMenuGrp(mPathUI[0+Add], q=True, sl=True)-1)
			mPathAttrNew.append(cmds.floatField(mPathUI[1+Add], q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[2+Add], q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[3+Add], q=True, v=True))
			mPathAttrNew.append(cmds.checkBox(mPathUI[4+Add],q=True, v=True))
			mPathAttrNew.append(cmds.checkBox(mPathUI[5+Add],q=True, v=True))
			mPathAttrNew.append(cmds.optionMenuGrp(mPathUI[6+Add], q=True, sl=True)-1)
			mPathAttrNew.append(cmds.optionMenuGrp(mPathUI[7+Add], q=True, sl=True)-1)
			mPathAttrNew.append(cmds.floatField(mPathUI[8+Add], q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[9+Add], q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[10+Add], q=True, v=True))
			mPathAttrNew.append(cmds.checkBox(mPathUI[11+Add],q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[12+Add], q=True, v=True))
			mPathAttrNew.append(cmds.floatField(mPathUI[13+Add], q=True, v=True))
		
			Add=Add+AF
		
		Add=0	
		
		for i2 in range(0,len(mPathAttrNew)):
			cmds.setAttr(mAttrFull[i2], mPathAttrNew[i2])
		
		for i3 in range(0,len(mPath)):
			kFrm=cmds.keyframe( mPath[i3]+".u", time=(0,50000), query=True, timeChange=True)
			cmds.currentTime(kFrm[-1])
			cmds.setAttr(mAttrFull[8+Add], mPathAttrNew[8+Add])
			cmds.setAttr(mAttrFull[9+Add], mPathAttrNew[9+Add])
			cmds.setAttr(mAttrFull[10+Add], mPathAttrNew[10+Add])
			cmds.setKeyframe(mPath[i3]+".frontTwist")
			cmds.setKeyframe(mPath[i3]+".upTwist")
			cmds.setKeyframe(mPath[i3]+".sideTwist")
			cmds.currentTime(0)
			cmds.setAttr(mAttrFull[8+Add], 0)
			cmds.setAttr(mAttrFull[9+Add], 0)
			cmds.setAttr(mAttrFull[10+Add], 0)
			cmds.setKeyframe(mPath[i3]+".frontTwist")
			cmds.setKeyframe(mPath[i3]+".upTwist")
			cmds.setKeyframe(mPath[i3]+".sideTwist")
				
			Add=Add+AF
			


