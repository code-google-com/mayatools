import sys
import time #used to time code execution
import os
import maya.cmds as mc
#import maya.OpenMaya as om
import maya.api.OpenMaya as om
import re
import maya.mel as mel
from pymel.core import *
import copy


#from pymel.all import *
#import pymel.core.datatypes as dt #vector datatype

#import os
#os.putenv("KMP_DUPLICATE_LIB_OK", "TRUE") #allows us to import the intel optimised version of numpy
#import numpy as np

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic
import sip


class colourEditor:
	def __init__(self):

		self.win = "colourEditorWindow"
		self.paintsCfgPath = "M:/assets/Vehicles/liveryEditor/paints.cfg"
		self.paints = [] 
		self.readColours()
		self.paintShader = "body_paint_setup"
		self.paintGUISwatches = []
		self.albedoGUISwatches = []
		self.metallicGUISwatches = []
		self.selectedPaint = None
		self.validPaintTypes = ["Factory"]
		self.defaultFinishes = ("Gloss","Matte","Metallic","Candy","MMetallic","MCandy")
				
		win = "colourEditorWindow"
		if (mc.window(win, ex=1)): mc.deleteUI (win)
	
		mc.window(win, title="Super Colour Editor", menuBar=1, toolbox=1)
		
		mainColumn = mc.columnLayout()
		mc.frameLayout(width=600, collapsable=1, label="Setup", mw=10, mh=10, labelAlign="center", borderStyle="etchedOut")
		mc.columnLayout()
		
		mc.rowLayout(numberOfColumns=2)
		mc.button (height=20, width=290, label="Load Paint Setup Shader + Assign to Bodypaint", ann="Must run this first for the swatch editing system to work", c=self.loadPaintSetupShader)
		mc.button (height=20, width=290, label="Save all shader edits back to paints.cfg", ann="", c=Callback(self.savePaintCfg) )
		mc.setParent("..")
		
		mc.rowLayout(numberOfColumns=2)
		mc.button (height=20, width=150, label="Render Swatches", ann="", c=Callback(self.renderSwatches) )
		mc.button (height=20, width=150, label="Build Swatches", ann="", c=Callback(self.buildSwatchImages) )

		
		
		mc.setParent("..")
		
		
		#mc.button (height=20, width=400, label="Print Cols", ann="", c=self.printColours)
		
		mc.setParent("..")
		mc.setParent("..")
		

		
		mc.setParent(mainColumn)
		mc.frameLayout(width=600, collapsable=1, label="Edit", mw=10, mh=10, labelAlign="center", borderStyle="etchedOut")
		mc.columnLayout()
				
		mc.rowLayout(numberOfColumns=2)
		mc.button(height=20, width=290, label="Edit Selected Preset", ann="Assigns the selected colour from the list to the paint setup shader for editing (or double click shader in list)", c=Callback(self.editSelected))    
		mc.button(height=20, width=290, label="Show Shader Attributes", ann="Reopens the shader attribute editor for paint editing", c=Callback(self.showMaterialAttributes))    
		mc.setParent("..")
		
		mc.rowLayout(numberOfColumns=2)
		mc.button(height=20, width=290, label="Copy Shader Attributes back to Selected Preset", ann="Writes the current shader settings into the selected paint", c=Callback(self.writePaintToSelected))    
		mc.button(height=20, width=290, label="Create new preset (below selected)", ann="Writes the current shader settings into the selected paint", c=Callback(self.writePaintBelowSelected))    
		mc.setParent("..")
		
		mc.rowLayout(numberOfColumns=4)
		mc.button(height=20, width=142, label="Move Up ^^^", ann="Moves the selected shader down in the list", c=Callback(self.moveSelectedUp))    
		mc.button(height=20, width=142, label="Move Down vvv", ann="Moves the selected shader up in the list", c=Callback(self.moveSelectedDown))    
		mc.button(height=20, width=142, label="Sort Paints", ann="Sorts all paints by brightness", c=Callback(self.sortPaints)) 
		mc.button(height=20, width=142, label="Delete Selected Preset", ann="Writes the current shader settings into the selected paint", c=Callback(self.deleteSelected))    
		mc.setParent("..")
		
		
		
		mc.rowLayout(numberOfColumns=3, columnWidth3=[250,100,250])
		mc.text(label = "Paint Vehicle:")
		mc.text(label = "Paint Type:")
		mc.text(label = "Paint Name:")
		mc.setParent("..")
		mc.rowLayout(numberOfColumns=3, columnWidth3=[250,100,250])
		self.PaintVehicleEditor = mc.textField(w=250, text="", changeCommand=Callback(self.paintVehicleEdited))
		self.PaintTypeEditor = mc.textField(w=100, text="", changeCommand=Callback(self.paintTypeEdited))
		self.PaintNameEditor = mc.textField(w=250, text="", changeCommand=Callback(self.paintNameEdited))
		mc.setParent("..")
		
		mc.setParent(mainColumn)
		mc.scrollLayout(width=600, height=800)
		self.PaintsColumn = mc.columnLayout(rowSpacing=2)
		self.updatePaintsColumn()

		mc.showWindow(win)
		mc.window(win, e=1, w=100, h=100)
		
		
		
		
	def renderSwatches(self):
		swatchFile = "M:/art/vehicles/GENERIC_MAYA/vehicle_paint_swatch.mb"
		destPath = "M:/assets/gui/images/paints/temp"
		
		#load swatch scene and lose changes?
		if  mc.file(q=1, sn=1) != swatchFile:
			result = mc.confirmDialog( 
				message="Load Swatch Scene?",
				button=("Load", "Cancel"), 
				defaultButton="Cancel", cancelButton="Cancel", dismissString="Cancel")
			if result == "Cancel": return
			if result == "Load":
				mc.file(swatchFile, open=1, force=1)
			
		#render each paint
		
		i=0
		for paint in self.paints:
		
			mc.setAttr( (self.paintShader + ".Mat_float_PaintColour"), paint.albedo[0], paint.albedo[1], paint.albedo[2] ,type='float3')
			mc.setAttr( (self.paintShader + ".Mat_float_MetallicColour"), paint.metallic[0], paint.metallic[1], paint.metallic[2], type='float3')
			mc.setAttr( (self.paintShader + ".Mat_float_Smoothness"), paint.albedo[3])
			mc.setAttr( (self.paintShader + ".Mat_float_MetallicPower"), paint.metallic[3])
			
			fileName=""
			if paint.who == "all": 
				fileName = ( paint.finish + "_" + str(i) + ".bmp").lower()
			else:
				fileName = ( paint.who + "_" + str(i) + ".bmp").lower()
		
			dest = (destPath + "/" + fileName)
			print ("Rendering: " + dest)
			imageFile = mc.hwRender(height=64, width=64, camera="persp")
			mc.sysFile(imageFile, copy=dest)
			
			i+=1
		
		#assemble final images
	
	def buildSwatchImages(self):
		
		swatchPath = "M:/assets/gui/images/paints/temp"
		destPath = "M:/assets/gui/images/paints"
		
		swatchDict = {}
		i=0
		for paint in self.paints:
			
			sourceName=""
			destName=""
			if paint.who == "all": 
				sourceName = ( paint.finish + "_" + str(i) + ".bmp")
				destName = ( paint.finish + ".png").lower()
			else:
				sourceName = ( paint.who + "_" + str(i) + ".bmp")
				destName = ( paint.who + ".png").lower()
			
			if destName not in swatchDict.keys():
				swatchDict[destName] = []
			
			swatchDict[destName].append(sourceName)
			i+=1
		
		for k in swatchDict.keys():
			print ("Updating swatch file: " + k)                                
			
			destFile = (destPath + "/" + k)
			
			destImage = QtGui.QImage(512,512, QtGui.QImage.Format_RGB32)
			
			
			p=0
			for image in swatchDict[k]:
				sourceFile = (swatchPath + "/" + image)
				sourceImage = QtGui.QImage(sourceFile) #.mirrored(horizontal=True, vertical=False)
				
				print ("source image: " + sourceFile)
								
				destPosX = (p%8) * 64
				destPosY = (p/8) * 64
				#destPos = QtCore.QPoint(50,50) 
				destPos = QtCore.QPoint(destPosX,destPosY)
				painter = QtGui.QPainter(destImage)
				painter.drawImage(destPos, sourceImage)
				painter.end()
				
				p+=1
				
			destImage.save(destFile) 

#im = PyQt4.QtGui.QImage("D:/games/branches/evo11dx11/MS3/assets/gui/images/paints/matte.png")
#im.width()
#im2 = im.mirrored()
#im2.save("D:/games/branches/evo11dx11/MS3/assets/gui/images/paints/matte2.png")

#convert image to QPixmap
#QGraphicsPixmapItem & put in QGraphicsScene

#QImage srcImage = QImage(100, 100);
#QImage destImage = QImage(200, 200);
#QPoint destPos = QPoint(25, 25);  // The location to draw the source image within the dest

#srcImage.fill(Qt::red);
#destImage.fill(Qt::white);

#QPainter painter(&destImage);
#painter.drawImage(destPos, srcImage);
#painter.end();



	#saves all the modified paints back to disk
	def sortPaints(self):
		
		reorderedPaints = []
		
		lastPaintWho = self.paints[0].who
		lastPaintFinish = self.paints[0].finish
		
		paintsByType = []
		thisType = []

		#sort paints into catagories
		for paint in self.paints:
			if lastPaintWho != paint.who or lastPaintFinish != paint.finish:
				paintsByType.append(thisType)
				thisType = []
			thisType.append(paint)
		 	lastPaintWho = paint.who
			lastPaintFinish = paint.finish
		paintsByType.append(thisType)

		#order each type
		for paintType in paintsByType:
									
			brightnessList = []
			for paint in paintType:
				brightness = paint.getBrightness()
				if paint.getMetallicSRGB() == [0,0,0]: brightness -= 100 #place non metallics first
				brightnessList.append(brightness)
			
			sortedPaints = sorted(zip(brightnessList,paintType), reverse=True)
			
			#don't sort manufacturer colours!
			if paintType[0].finish in ("Gloss","Matte","Metallic","Candy","MMetallic","MCandy","Factory"):
				sortedPaints = zip(brightnessList,paintType)
						
			for x in sortedPaints:
				reorderedPaints.append(x[1])
		
		self.paints = reorderedPaints
		self.updatePaintsColumn()




	
	#saves all the modified paints back to disk
	def savePaintCfg(self):
		
		warn = mc.confirmDialog( title='Warning', message="Paints.cfg will be overwritten - are you sure?", button=["OK","CANCEL"], defaultButton='CANCEL', cancelButton='CANCEL', dismissString='CANCEL')
		if warn == "CANCEL": return
				
		paintFile = """-- Auto Generated by Maya Super Colour Editor Tool 
--
-- Lines with -- are comments!
--
-- If you add / alter a colour here you must..
-- Checkout all .png in assets/gui/images/paints
-- run assets/Vehicles/LiveryEditor/Assets/colours/MakeGuiPaintSwatches
-- Check back in the *.png in assets/gui/images/paints
--
--Who	,Finish			,R			,G			,B		,Smooth			,R			,G			,B		,Shine  --Paint Name
-- Who => for which vehicle or all
-- Finish => "Gloss","Matte","Metallic","Candy" where who=="all"
-- or 		"Factory" where who=<name of car>
-- See PF if you need help.
--\n"""
		lastPaintWho = ""
		lastPaintFinish = ""
		
		for paint in self.paints:
			if lastPaintWho != paint.who or lastPaintFinish != paint.finish:
				paintFile += "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
			paintFile += (paint.getString() + "\n")
			lastPaintWho = paint.who
			lastPaintFinish = paint.finish
		 
		paintFile += "--"
		
		
		try:
			f = open(self.paintsCfgPath, 'w')
		except IOError, e:
			if e.errno == 13:
				checkout = mc.confirmDialog( title='Perforce Error', message="Paints.cfg is write protected - Get latest and check out?", button=["OK","CANCEL"], defaultButton='CANCEL', cancelButton='CANCEL', dismissString='CANCEL')
				if checkout == "CANCEL": return
				
				path = os.environ.get('BRANCH_ROOT')
				path += r"\assets\Vehicles\liveryEditor\paints.cfg"

				os.system( ("p4 sync " + path) );
				os.system( ("p4 edit " + path) );
			else:
				raise
				
		f = open(self.paintsCfgPath, 'w')
		f.write(paintFile)
		f.close()
		
	
	#moves selected paint swatch up
	def moveSelectedUp(self):
		a, b = self.selectedPaint, (self.selectedPaint-1)
		if b >= 0:
			self.paints[b], self.paints[a] = self.paints[a], self.paints[b]
			self.updatePaintsColumn()
			self.paintButtonClicked(b)
	
	#moves selected paint swatch up
	def moveSelectedDown(self):
		a, b = self.selectedPaint, (self.selectedPaint+1)
		if b < len(self.paints):
			self.paints[b], self.paints[a] = self.paints[a], self.paints[b]
			self.updatePaintsColumn()	
			self.paintButtonClicked(b)
	
	#deletes selected paint swatch below selected - prevents deleting standard paints
	def deleteSelected(self):
		
		if len(mc.ls(self.paintShader, type="ATGMaterial")) == 0:
			mc.confirmDialog( title='Warning', message="No body_paint_setup shader found in scene - can't write paint", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
			return
		
		newPaint = copy.copy(self.paints[self.selectedPaint])
		
		if self.paints[self.selectedPaint].finish in self.defaultFinishes:
			mc.confirmDialog( title='Warning', message="Can't delete generic presets - there must be exactly 64 of each type", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
			return
				
		sure = mc.confirmDialog( title='Delete Selected paint preset', message="Are you sure you want to delete the selected preset? (not undoable)", button=["OK","CANCEL"], defaultButton='CANCEL', cancelButton='CANCEL', dismissString='CANCEL')
		if sure == "CANCEL": return
		
		self.paints.pop(self.selectedPaint)
		self.updatePaintsColumn()	
	
	#adds a new paint swatch below selected - prevent adding to standard paints
	def writePaintBelowSelected(self):
		
		if len(mc.ls(self.paintShader, type="ATGMaterial")) == 0:
			mc.confirmDialog( title='Warning', message="No body_paint_setup shader found in scene - can't write paint", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
			return
		
		newPaint = copy.copy(self.paints[self.selectedPaint])
		
		if newPaint.finish in self.defaultFinishes:
			mc.confirmDialog( title='Warning', message="Can't add to generic presets - there must be exactly 64 of each type", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
			return
				
		alb = mc.getAttr( (self.paintShader + ".Mat_float_PaintColour") )[0]
		met = mc.getAttr( (self.paintShader + ".Mat_float_MetallicColour") )[0]
		smo = mc.getAttr( (self.paintShader + ".Mat_float_Smoothness") )
		pwr = mc.getAttr( (self.paintShader + ".Mat_float_MetallicPower") )
		
		newPaint.albedo = [ alb[0], alb[1], alb[2], smo ]
		newPaint.metallic = [ met[0], met[1], met[2], pwr ]
		
		warn = newPaint.isValid()
		if warn == None:
			self.paints.insert( (self.selectedPaint+1), newPaint)
			self.updatePaintsColumn()			
		else:
			mc.confirmDialog( title='Warning', message=warn, button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')



	#writes the current shader settings over the selected paint swatch
	def writePaintToSelected(self):
		
		if len(mc.ls(self.paintShader, type="ATGMaterial")) == 0:
			mc.confirmDialog( title='Warning', message="No body_paint_setup shader found in scene - can't write paint", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
			return		
		
		newPaint = copy.copy(self.paints[self.selectedPaint])
		
		alb = mc.getAttr( (self.paintShader + ".Mat_float_PaintColour") )[0]
		met = mc.getAttr( (self.paintShader + ".Mat_float_MetallicColour") )[0]
		smo = mc.getAttr( (self.paintShader + ".Mat_float_Smoothness") )
		pwr = mc.getAttr( (self.paintShader + ".Mat_float_MetallicPower") )
		
		newPaint.albedo = [ alb[0], alb[1], alb[2], smo ]
		newPaint.metallic = [ met[0], met[1], met[2], pwr ]
		
		warn = newPaint.isValid()
		if warn == None:
			self.paints[self.selectedPaint] = newPaint
			
			mc.text(self.albedoGUISwatches[self.selectedPaint], e=1, bgc=self.paints[self.selectedPaint].getAlbedoSRGB())
			mc.text(self.metallicGUISwatches[self.selectedPaint], e=1, bgc=self.paints[self.selectedPaint].getMetallicSRGB())
			
		else:
			mc.confirmDialog( title='Warning', message=warn, button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
  			


		
		
		
		
	
		
	def paintNameEdited(self):
		paint = self.paints[self.selectedPaint]
		paint.name = mc.textField(self.PaintNameEditor, q=1, text=1)
		mc.iconTextButton(self.paintGUISwatches[self.selectedPaint], e=1, label=paint.getGUIString())
		
	def paintVehicleEdited(self):
		paint = self.paints[self.selectedPaint]
		paint.who = mc.textField(self.PaintVehicleEditor, q=1, text=1)
		mc.iconTextButton(self.paintGUISwatches[self.selectedPaint], e=1, label=paint.getGUIString())
		
	def paintTypeEdited(self):
		paint = self.paints[self.selectedPaint]
		
		newType = mc.textField(self.PaintTypeEditor, q=1, text=1)
		
		if newType in self.validPaintTypes:
			paint.finish = newType
		
		mc.iconTextButton(self.paintGUISwatches[self.selectedPaint], e=1, label=paint.getGUIString())
		
		
	def updatePaintsColumn(self):
		
		for iconButton in self.paintGUISwatches:
			mc.deleteUI(mc.iconTextButton(iconButton, q=1, parent=1)) 
		
		self.paintGUISwatches = []
		self.albedoGUISwatches = []
		self.metallicGUISwatches = []
	
		i=0
		for paint in self.paints:
			mc.setParent(self.PaintsColumn)
			mc.rowLayout(numberOfColumns=3, columnWidth3=[30,30,505])
			aSwatch = mc.text(w=30, h=20, bgc=paint.getAlbedoSRGB(), label="")
			mSwatch = mc.text(w=30, h=20, bgc=paint.getMetallicSRGB(), label="")
			
			#highlight broken presets in red
			bgCol = [0.9,0.9,0.9]
			if paint.isValid() != None: bgCol = [0.9,0.7,0.7]
			
			iconButton = mc.iconTextButton(style="iconAndTextHorizontal", label=paint.getGUIString(), bgc=bgCol, w=505, h=20, c=Callback(self.paintButtonClicked, i), dcc=Callback(self.paintButtonDoubleClicked, i) )    
			self.paintGUISwatches.append(iconButton)
			self.albedoGUISwatches.append(aSwatch)
			self.metallicGUISwatches.append(mSwatch)
			
			i+=1
			
	def paintButtonClicked(self,i):
		if self.selectedPaint != None:
			bgCol = [0.9,0.9,0.9]
			if self.paints[self.selectedPaint].isValid() != None: bgCol = [0.9,0.7,0.7]
			mc.iconTextButton(self.paintGUISwatches[self.selectedPaint], e=1, bgc=bgCol)
		self.selectedPaint = i
		mc.iconTextButton(self.paintGUISwatches[i], e=1, bgc=[0.776, 0.835, 0.992])
		
		paint = self.paints[self.selectedPaint]
		mc.textField(self.PaintNameEditor, e=1, text=paint.name, enable=1)
		mc.textField(self.PaintVehicleEditor, e=1, text=paint.who, enable=1)
		mc.textField(self.PaintTypeEditor, e=1, text=paint.finish, enable=1)
		
		#protect fixed gui swatches
		if paint.who in ("all"): mc.textField(self.PaintVehicleEditor, e=1, enable=0)
		if paint.finish in self.defaultFinishes:
			mc.textField(self.PaintTypeEditor, e=1, enable=0)
		
	def paintButtonDoubleClicked(self,i):
		self.paintButtonClicked(i)
		self.editSelected()

	def editSelected(self):
		if len(mc.ls(self.paintShader, type="ATGMaterial")) == 0:
			mc.confirmDialog( title='Warning', message="No body_paint_setup shader found in scene - can't edit paint", button=["OK"], defaultButton='OK', cancelButton='OK', dismissString='OK')
  			return		
		
		paint = self.paints[self.selectedPaint]
		mc.setAttr( (self.paintShader + ".Mat_float_PaintColour"), paint.albedo[0], paint.albedo[1], paint.albedo[2] ,type='float3')
		mc.setAttr( (self.paintShader + ".Mat_float_MetallicColour"), paint.metallic[0], paint.metallic[1], paint.metallic[2], type='float3')
		mc.setAttr( (self.paintShader + ".Mat_float_Smoothness"), paint.albedo[3])
		mc.setAttr( (self.paintShader + ".Mat_float_MetallicPower"), paint.metallic[3])
				
		self.showMaterialAttributes()
		
		
	def showMaterialAttributes(self):
		mel.eval( ('showEditor("' + self.paintShader + '")') )
	
	#reads in colours from config file, translates into list of paintColour objs
	def readColours(self):
		f = open(self.paintsCfgPath, 'r')
		lines = f.readlines()
		f.close()
		
		self.paints = []
		for line in lines:
			if line[0:2] != "--" and len(line.split(",")) == 10:
				#should be a valid colour
				newColour = paintColour()
				newColour.setFromString(line)
				self.paints.append( newColour )
	
	#prints the strings of all paintColour objs
	def printColours(self, *args):
		for i in self.paints: print i
			
	#loads and applies paint setup shader to any bodypaints in scene
	def loadPaintSetupShader(self, *args):
		
		paintSetupPath = "m:/assets/noodle/materials/library/vehicles_dc/body_paint/body_paint_setup.xml"
		bodyPaintXMLs = ("body_livery_carbon_damage.xml","body_livery_metal_damage.xml") 
		
		shaders = mc.ls(materials=1)
		if self.paintShader not in shaders:
			mc.shadingNode("ATGMaterial", asShader=1, name=self.paintShader)
			mc.setAttr ( (self.paintShader + ".SelectMode"), 0)
			mc.setAttr ( (self.paintShader + ".RawPath"), paintSetupPath, type="string")
		
			bodyPaints=[]
			for shader in shaders:
				if mc.nodeType(shader) == "ATGMaterial":
					xmlpath = mc.getAttr((shader + ".RawPath"))
					if xmlpath.endswith(bodyPaintXMLs):
						bodyPaints.append(shader)
			
			for shader in bodyPaints:
				mc.hyperShade(objects=shader)
				mc.hyperShade(assign=self.paintShader)
		
	
	



class paintColour:
	def __init__(self):
		self.who = ""
		self.finish = ""
		self.albedo = [0.,0.,0.,0.]
		self.metallic = [0.,0.,0.,0.]
		self.name = ""
	
	def __str__(self):
		return self.getString()
		
	def getString(self):
		formatTuple = (self.who, self.finish, self.albedo[0], self.albedo[1], self.albedo[2], self.albedo[3], self.metallic[0], self.metallic[1], self.metallic[2], self.metallic[3], self.name)
		colourString = "%s   ,%s   ,%.4f   ,%.4f   ,%.4f   ,%.4f   ,%.4f   ,%.4f   ,%.4f   ,%.4f   --%s" % formatTuple
		return colourString
	
	def getGUIString(self):
		formatTuple = (self.who, self.finish, self.name)
		guiString = "%s - %s - %s" % formatTuple
		return guiString
	
	def getAlbedoSRGB(self):
		return [x**(1.0/2.2) for x in self.albedo[0:3]]
	
	def getMetallicSRGB(self):
		return [x**(1.0/2.2) for x in self.metallic[0:3]]
	
	#returns a brightness value for ordering
	def getBrightness(self):
		metPowerB = 1.5 - self.metallic[3]
		g = (1.0/2.2)
		albedoB = (self.albedo[0]**(g)) + (self.albedo[1]**(g)) + (self.albedo[2]**(g))
		metallicB = (self.metallic[0]**(g)) + (self.metallic[1]**(g)) + (self.metallic[2]**(g))
		b =  albedoB + (metPowerB * metallicB)
		return b
		
	def setFromString(self, inString):
		commentSplit = re.sub(r'\s', '', inString).split("--")
		if len(commentSplit) == 2:
			self.name = commentSplit[1]
		else:
			self.name = ""
		paintSplit = commentSplit[0].split(",")
		self.who = paintSplit[0]
		self.finish = paintSplit[1]
		self.albedo = [float(paintSplit[2]),float(paintSplit[3]),float(paintSplit[4]),float(paintSplit[5])]
		self.metallic = [float(paintSplit[6]),float(paintSplit[7]),float(paintSplit[8]),float(paintSplit[9])]
	
	#returns None if colour settings are ok, else returns a warning msg
	def isValid(self):
		
		aMax = max(self.albedo[0:3]) ** (1/2.2)
		mMax = max(self.metallic[0:3]) ** (1/2.2)
		warn = None
		if aMax > 0.8:
			warn = "Invalid paint setting - Albedo value is brighter than 0.8"
			mc.warning(warn)
			return warn
		if (aMax + mMax) > 1.0:
			warn = "Invalid paint setting - Albedo + Metalic value is brighter than 1"
			mc.warning(warn)
			return warn
		if self.albedo[3] < 0.8:
			warn = "Invalid paint setting - Shininess should not go below 0.8"
			mc.warning(warn)
			return warn
		if self.metallic[3] < 0.5 and mMax > 0:
			warn = "Invalid paint setting - Metallic Power should not go below 0.5 (unless Metallic Colour is black)"
			mc.warning(warn)
			return warn
		
		return warn