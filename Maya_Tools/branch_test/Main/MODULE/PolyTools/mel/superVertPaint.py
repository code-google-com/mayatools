import sys
import time #used to time code execution

import maya.cmds as mc
#import maya.OpenMaya as om
import maya.api.OpenMaya as om
import re
import maya.mel as mel

#from pymel.all import *
#import pymel.core.datatypes as dt #vector datatype

#import os
#os.putenv("KMP_DUPLICATE_LIB_OK", "TRUE") #allows us to import the intel optimised version of numpy
#import numpy as np


#does a reflection from the driver's eye to work out where to brighten the interior reflections
def brightenCockpitAO(mode):
	
	#get face selection of metal parts
	polysToTest = mc.ls(fl=True, sl=True)
	polysToTest = [p for p in polysToTest if re.search(r'\.f\[', p)]
	
	if len(polysToTest) == 0: mc.error("No polygons selected!")
	
	#work out driver's head position
	seatPos = mc.xform("SEAT_DRIVER", q=True, ws=True, translation=True)
	headPos = om.MFloatPoint([seatPos[0],(seatPos[1]+0.65),(seatPos[2]-0.15)])
		
	#create temprorary raycasting test object hemisphere

	#delete existing raycast lookup
	raycastLookups = mc.ls("RAYCAST_SPHERE*", transforms=1)
	if len(raycastLookups) > 0:
		for lookup in raycastLookups:
			mc.delete(lookup)

	mc.polySphere(ch=0, o=1, r=1.1, name="RAYCAST_SPHERE")
	mc.setAttr("RAYCAST_SPHERE.t", 0, 0.69, 0)
	mc.setAttr("RAYCAST_SPHERE.r", 3, 0, 0)
	mc.setAttr("RAYCAST_SPHERE.s", 1, 1, 1.3)
	mc.delete( ['RAYCAST_SPHERE.f[0:199]', 'RAYCAST_SPHERE.f[360:379]'] )

	raycastLookupMfn = getMeshFN("RAYCAST_SPHERE")
		
	#convert to a list of verts/vfs bepending if hard or soft normals
	
	vfsToTest = mc.polyListComponentConversion(polysToTest, toVertexFace=1)
	vfsToTest = mc.ls(vfsToTest, fl=1)
	vfsToBrighten = []
	
	#get position and normal of each vert / vf
	print "Testing verts..."
	for vf in vfsToTest:
		
		#calculate reflection vector
		vert = mc.polyListComponentConversion(vf, toVertex=1)
		pos = om.MFloatPoint(mc.pointPosition(vert[0], world=1))
		normal = getWorldSpaceNormal(vf) #om.MFloatVector(mc.polyNormalPerVertex(vf, q=1, xyz=1)[0:3])
		eye = (headPos-pos).normalize()
		
		dot = (eye*normal)
		if dot > 0: #don't bounce off backfaces
			ref = (2 * normal * dot) - eye
			raycastResult = raycastLookupMfn.anyIntersection(pos,ref,om.MSpace.kWorld,4,False,tolerance=0.001)
			if (raycastResult[1] != 0.0): vfsToBrighten.append(vf)

		#draw debug refs
		#refL = pos + (2*ref)
		#mc.curve(d=1, p=((pos.x,pos.y,pos.z),(refL.x,refL.y,refL.z)), k=(0,1), name="reflection_vector_");
		#eyeL = pos + eye
		#mc.curve(d=1, p=((pos.x,pos.y,pos.z),(headPos.x,headPos.y,headPos.z)), k=(0,1), name="reflection_eye_vector_");
		#print vf
		#print raycastResult
		
		
		
	
	#print vfsToBrighten
	
	mc.select(vfsToBrighten)
	if (mode==1): mc.polyColorPerVertex(a=0.9, cdo=0)
	
	#brighten all window reflecting verts
	
	#cleanup
	print "Cleanup..."
	raycastLookups = mc.ls("RAYCAST_SPHERE*", transforms=1)
	if len(raycastLookups) > 0:
		for lookup in raycastLookups:
			mc.delete(lookup)




#returns the normal of a vf in world space
def getWorldSpaceNormal(vf): 

	normal = om.MVector(mc.polyNormalPerVertex(vf, q=1, xyz=1)[0:3])
	obj = re.sub(r'\.vtxFace.*', '', vf)
	
	if mc.nodeType(obj) == "mesh":
		obj = mc.listRelatives(obj, parent=1)[0]
	#print normal
	
	transFN = getTransFN(obj)
	invMatrix = transFN.transformation().asMatrix() #.asMatrixInverse()
	normal *= invMatrix
	#print normal

 	return om.MFloatVector(normal)










#proc to fix AO gamma
def adjustAOLevels(black, white, gamma):
	objs = mc.ls(transforms=True, sl=True)
	print objs
	for obj in objs:
		print obj
		#convert sel to vert list
		verts = mc.polyListComponentConversion(obj, toVertex=True)
		verts = mc.ls(verts, fl=True)
		
		Mcols = om.MColorArray()
		Mverts = om.MIntArray()
		
		oldCols = getVertCols(verts, "RGBA")
		cols = 	getVertCols(verts, "A")
		print cols
		cols2 = calcLevels(cols, black, white, gamma)
		
		for i in range(0,len(verts)):
			Mcols.append(om.MColor( [oldCols[i*4], oldCols[i*4+1], oldCols[i*4+2], cols2[i]] )) # r,g,b,a
		for i in verts:
			Mverts.append( int(i.split('.vtx[')[-1:][0][:-1]) )
		
		# Create a function set for the mesh.
		meshFn = getMeshFN(obj)
	
		#set colours with API
		meshFn.setVertexColors(Mcols, Mverts)
	
		# Turn off the mesh's color display.
		meshFn.findPlug('displayColors').setBool(False)
			
			 
		

def test2(sel):
	
	#convert sel to vert list
	sel = mc.polyListComponentConversion(sel, toVertex=True)
	sel = mc.ls(sel, fl=True)
	
	colours1 = getVertCols(sel, "A")
	colours2 = calcLevels(colours1, 0.0, 1.0, 2.2)
	
	setVertCols(sel, "A", colours2)


def getVertCols(sel, channel):
	#t0 = time.clock()
	
	rgba = [0,0,0,0]
	if "R" in channel: rgba[0] = 1
	if "G" in channel: rgba[1] = 1 
	if "B" in channel: rgba[2] = 1
	if "A" in channel: rgba[3] = 1 
	
	numVerts = mc.polyEvaluate( vertex=True )
	
	#for i in range(0,numVerts):
	#colourList.append( mc.polyColorPerVertex( (obj + ".vtx[" + str(i) + "]"), query=True, rgb=True ) )
	
	colourList = mc.polyColorPerVertex( sel, query=True, r=rgba[0], g=rgba[1], b=rgba[2], a=rgba[3] )
	
	#t = time.clock() - t0
	#print "Time to read all colours %f" % t
	
	#print colourList
	
	return colourList
	
	





#sets all vertex cols using api
#sel is a list of verts, channel is R/G/B/A/RGB/RGBA, newCols is a list of colour values.
def setVertCols(sel, channel, newCols):

	oldCols = getVertCols(sel, "RGBA")
		
	t0 = time.clock()
	
	cols = om.MColorArray()
	verts = om.MIntArray()
	numVerts = mc.polyEvaluate( vertex=True )
	
	if channel=="R":
		for i in range(0,len(sel)):
			cols.append(newCols[i], oldCols[i*4+1], oldCols[i*4+2], oldCols[i*4+3]) # r,g,b,a
	elif channel=="G":
		for i in range(0,len(sel)):
			cols.append(oldCols[i*4], newCols[i], oldCols[i*4+2], oldCols[i*4+3]) # r,g,b,a
	elif channel=="B":
		for i in range(0,len(sel)):
			cols.append(oldCols[i*4], oldCols[i*4+1], newCols[i], oldCols[i*4+3]) # r,g,b,a
	elif channel=="A":
		for i in range(0,len(sel)):
			cols.append(oldCols[i*4], oldCols[i*4+1], oldCols[i*4+2], newCols[i]) # r,g,b,a
	elif channel=="RGB":
		for i in range(0,len(sel)):
			cols.append(newCols[i*4], newCols[i*4+1], newCols[i*4+2], oldCols[i*4+3]) # r,g,b,a
	elif channel=="RGBA":
		for i in range(0,len(sel)):
			cols.append(newCols[i], newCols[i*4+1], newCols[i*4+2], newCols[i*4+3]) # r,g,b,a
	for i in sel:
		verts.append( int(i.split('.vtx[')[-1:][0][:-1]) )
		
	# Get the mesh's dag path.
	msel = om.MSelectionList()
	msel.add(sel[0])
	meshPath = om.MDagPath()
	msel.getDagPath(0, meshPath)

	# Create a function set for the mesh.
	meshFn = om.MFnMesh(meshPath)
	
	#set all vert colours in mel (slow, but works on bigrig41 wheels)
	#for i in range(0,len(sel)):
	##	print "setting %s to %f" % (sel[i], newCols[i])
	#	mc.polyColorPerVertex( sel[i], b=newCols[i]) 
	
	#set colours with API - not working on bigrig41 wheels, unless you do a "resurrect corrupted shape nodes"
	meshFn.setVertexColors(cols, verts)
	
	# Turn off the mesh's color display.
	meshFn.findPlug('displayColors').setBool(False)
		
	t = time.clock() - t0
	print "Time to set all colours at once with array not using api %f" % t
	
#######################Getting a colour via API
#	col = cols[63]
#	util = om.MScriptUtil()
#	util.createFromDouble(0.0)
#	rF = util.asFloatPtr()
#	util2 = om.MScriptUtil()
#	util2.createFromDouble(0.0)
#	gF = util2.asFloatPtr()
#	util3 = om.MScriptUtil()
#	util3.createFromDouble(0.0)
#	bF = util3.asFloatPtr()
#	col.get(om.MColor.kRGB,rF,gF,bF)
#	print om.MScriptUtil.getFloat(rF)
	


#sets all vertex cols using mel
#slow, but more reliable on corrupt geometry...
#fixed to preserve per vertex face info.
def setVertColsMel(sel, channel, newCols):

	t0 = time.clock()
	
	if channel == "R":
		for i in range(0,len(sel)):
			mc.polyColorPerVertex( sel[i], nun=1, r=newCols[i]) 
	if channel == "G":
		for i in range(0,len(sel)):
			mc.polyColorPerVertex( sel[i], nun=1, g=newCols[i]) 
	if channel == "B":
		for i in range(0,len(sel)):
			mc.polyColorPerVertex( sel[i], nun=1, b=newCols[i]) 
	if channel == "A":
		for i in range(0,len(sel)):
			mc.polyColorPerVertex( sel[i], nun=1, a=newCols[i]) 
		
	t = time.clock() - t0
	print "Time to set all colours using mel %f" % t

#sets all vertex face cols using mel
#very slow, but preserves hard edges in other colur channels...
#fixed to preserve per vertex face info.
def setVertColsMelPerVF(sel, channel, newCols):

	t0 = time.clock()
	
	mc.undoInfo(state=0);
	
	for i in range(0,len(sel)):
		
		vfs = mc.polyListComponentConversion(sel[i], toVertexFace = 1)
		vfs = mc.ls(vfs, fl=1)
		
		for vf in vfs:
			
			#if channel == "R":
			mc.polyColorPerVertex( vf, nun=1, r=newCols[i]) 
			#elif channel == "G":
			#	mc.polyColorPerVertex( vf, nun=1, g=newCols[i]) 
			#elif channel == "B":
			#	mc.polyColorPerVertex( vf, nun=1, b=newCols[i]) 
			#elif channel == "A":
			#	mc.polyColorPerVertex( vf, nun=1, a=newCols[i]) 
	
	mc.undoInfo(state=1, length=100);
	
	t = time.clock() - t0
	print "Time to set all colours to VFs using mel %f" % t









#######################Getting a colour via API
#	col = cols[63]
#	util = om.MScriptUtil()
#	util.createFromDouble(0.0)
#	rF = util.asFloatPtr()
#	util2 = om.MScriptUtil()
#	util2.createFromDouble(0.0)
#	gF = util2.asFloatPtr()
#	util3 = om.MScriptUtil()
#	util3.createFromDouble(0.0)
#	bF = util3.asFloatPtr()
#	col.get(om.MColor.kRGB,rF,gF,bF)
#	print om.MScriptUtil.getFloat(rF)


	
	


#does a photoshop style levels calculation
def calcLevels(inPixel, inBlack, inWhite, inGamma):
	print "calculating levels..."
	
	for i in range(0, len(inPixel)):
		inPixel[i] = clamp( ((inPixel[i]-inBlack)/(inWhite-inBlack)) , 0, 1) ** inGamma
	
	return inPixel



#old numpy version
#does a photoshop style levels calculation
#def calcLevels(inPixel, inBlack, inWhite, inGamma):
#	print "calculating levels..."
#	outPixel = (inPixel-inBlack)/(inWhite-inBlack)
#	np.clip(outPixel, 0, 1, out=outPixel) #req to prevent complex number fail
#	outPixel **= inGamma
#	#* (outWhite - outBlack)) + outBlack #### outWhite and black not required...
#	return outPixel

#normalizes a 2d array of vectors
def normalizeVectorArray(vectors):
	magnitudes = np.apply_along_axis(getMagnitude, 1, vectors)
	vectors /= magnitudes.reshape(-1,1) #gives the array a second dimension of 1 - needed for division to work

#returns the magnitude of the given 1d vector array
def getMagnitude(vector):
	return np.sqrt(np.dot(vector,vector.conj()))
	#3* faster than: np.sqrt(np.sum(np.abs(normals[0])**2))
	

#colour channel levels sliders, histograms?
	#per obj, selection, change colour channel

#colour chanel layers - mixing, combining copying.
	#see superDecalEditor

"""MAYA GUI - GRAPH TOO SLOW
class vertexColourLevels:
	def __init__(self, sel):
		
		vcLevelsWindow = "vcLevelsWindow"
		if (mc.window(vcLevelsWindow, ex=1)): mc.deleteUI (vcLevelsWindow)
	
		mc.window(vcLevelsWindow, title="Normal Toolbox", menuBar=1, toolbox=1)
		mc.menu (label="Help", tearOff=1, allowOptionBoxes=1);
		mc.menuItem (label="SHIP Help Page", command='showHelp -a "http://wiki.ship.scea.com/confluence/display/NWSTUDIOWIKI/BPT_PolyCutter"');

		mc.columnLayout()
		mc.frameLayout(width=276, collapsable=1, label="Selection", mw=10, mh=10, labelAlign="center", borderStyle="etchedOut")
		mc.columnLayout()
		
		histogramRowLayout = mc.rowLayout(numberOfColumns=128)
		for i in range(1,128):
			mc.rowLayout(histogramRowLayout, edit=1, columnWidth=[i, 2], rowAttach=[i,"bottom",0])
			mc.separator(height=(i/5+1), width=2, horizontal=0, style="double")
		mc.setParent("..")
		
		mc.button (height=20, width=200, label="Test", command="boltNorms.EdgeToVF(1)", ann="Blah blah")
		mc.setParent("..")
		mc.setParent("..")
		
		mc.showWindow(vcLevelsWindow)
		#window -e -height 550 -width 240 boltNormalsWindow;
		
"""

#sets all vertex cols using api
#sel is a list of verts, channel is R/G/B/A/RGB/RGBA, newCols is a list of colour values.
def setVertRGBs(verts, colours, mesh):

	t0 = time.clock()
	
	verts = eval(verts)
	colours = eval(colours)
	
	mColours = om.MColorArray()
	mVerts = om.MIntArray()
	numVerts = mc.polyEvaluate( vertex=True )
	
	for i in range(0,len(verts)):
		mColours.append(om.MColor( [float(colours[i*3]), float(colours[i*3+1]), float(colours[i*3+2]), 0.0] ) ) # r,g,b,a
	for i in verts:
		mVerts.append( int(i) )
		
	# Get the mesh's dag path.
	
	#returns a MFnMesh object for the specified obj
	meshFn = getMeshFN(mesh)
		
	#set all vert colours in mel (slow, but works on bigrig41 wheels)
	#for i in range(0,len(sel)):
	#	print "setting %s to %f" % (sel[i], newCols[i])
	#	mc.polyColorPerVertex( sel[i], b=newCols[i]) 
	
	#set colours with API - not working on bigrig41 wheels, unless you do a "resurrect corrupted shape nodes"
	meshFn.setVertexColors(mColours, mVerts)
	
	# Turn off the mesh's color display.
	#meshFn.findPlug('displayColors').setBool(False)
		
	t = time.clock() - t0
	print "\nTime to set all colours at once using api %f" % t






######################################################################################################


#returns a MFnMesh object for the specified obj
def getMeshFN(obj):
	
	#shape prevents errors on objs with interior only nodes if transform is used
	shape = mc.listRelatives(obj, fullPath=1, children=1, type="mesh")[0]
	
	# Get the mesh's dag path.
	msel = om.MSelectionList()
	msel.add(shape)
	meshPath = om.MDagPath()
	meshPath = msel.getDagPath(0)
	# Create a function set for the mesh.
	return om.MFnMesh(meshPath)

#returns a MFnTransform object for the specified obj
def getTransFN(obj):
	# Get the transform's dag path.
	msel = om.MSelectionList()
	msel.add(obj)
	transformPath = om.MDagPath()
	transformPath = msel.getDagPath(0)
	# Create a function set for the mesh.
	return om.MFnTransform(transformPath)




#returns a tupple of vertexColours, faceIDs, vertIDs for current object, default colorSet	
def getVertColsApi(obj):
	
	t0 = time.clock()
	
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	
	#get vf colours
	vertexColours = om.MColorArray()
	vertexColours = meshFn.getFaceVertexColors()

	#get sequence of face ids & corresponding vertex id list
	faceIDs = []
	vertIDs = []
	for i in range(0,meshFn.numPolygons):
		verts = meshFn.getPolygonVertices(i)
		for v in verts:
			faceIDs.append(i)
			vertIDs.append(v)
			
	t = time.clock() - t0

	return (vertexColours,faceIDs,vertIDs)


#sets the red colour channel with a list of per vertex values
#edits ver vertex face to avoid breaking other colour channels.
def setRedVertCols(obj, newCols):

	t0 = time.clock()
	
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)

	getColours = getVertColsApi(obj)
	colours = getColours[0]
	faceIDs = getColours[1]
	vertIDs = getColours[2]

	#process the list of colours
	for i in range(0, len(colours)):
		colours[i].r = newCols[vertIDs[i]]

	#re-apply colours to mesh
	meshFn.setFaceVertexColors(colours, faceIDs, vertIDs) 
	
	t = time.clock() - t0
	print "Time to set red vertex colours with api: %f" % t

#sets the green colour channel with a list of per vertex values
#edits ver vertex face to avoid breaking other colour channels.
def setGreenVertCols(obj, newCols):

	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)

	getColours = getVertColsApi(obj)
	colours = getColours[0]
	faceIDs = getColours[1]
	vertIDs = getColours[2]

	#process the list of colours
	for i in range(0, len(colours)):
		colours[i].g = newCols[vertIDs[i]]

	#re-apply colours to mesh
	meshFn.setFaceVertexColors(colours, faceIDs, vertIDs) 
	

#sets the red colour channel to black (no scratches)
def setRedVertColsToBlack(obj):

	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	try:
		getColours = getVertColsApi(obj)
	except:
		print ("ERROR - No vertex colours found on object: " + obj)
		return
		
	colours = getColours[0]
	faceIDs = getColours[1]
	vertIDs = getColours[2]

	#process the list of colours
	for i in range(0, len(colours)):
		colours[i].r = 0

	#re-apply colours to mesh
	meshFn.setFaceVertexColors(colours, faceIDs, vertIDs) 

#sets the green colour channel to black (no mud)
def setGreenVertColsToBlack(obj):
	
	#test for valid object
	isMesh = mc.listRelatives(obj, type="mesh")
	if not isMesh:
		print ("Could not paint mud for non mesh object: " + obj) 
		return
	
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	try:
		getColours = getVertColsApi(obj)
	except:
		print ("ERROR - No vertex colours found on object: " + obj)
		return
		
	colours = getColours[0]
	faceIDs = getColours[1]
	vertIDs = getColours[2]

	#process the list of colours
	for i in range(0, len(colours)):
		colours[i].g = 0

	#re-apply colours to mesh
	meshFn.setFaceVertexColors(colours, faceIDs, vertIDs) 

#returns the integer component index
def getComponentIndex(component):
	m_obj = re.search(r"(\[)([0-9]+)(\])", component)
	return int(m_obj.group(2))
	
	
#returns the short name of an object, without path
def getShortNameOf(obj):
	return obj.split("|")[-1]
	
#paints scratches
#added type flag to specify new maths that works better with new darker AO
def paintDamageColours(obj, scale, bias, occlusionAmount, aoType):
	
	#convert obj to vert list
	verts = mc.polyListComponentConversion(obj, toVertex=True)
	verts = mc.ls(verts, fl=True)
	
	#get peaks and dips infor for all vert
	peakDips = peaksAndDips(obj, scale, bias)
	
	occlusion = getVertCols(verts, "A")
	newCols = []
	if aoType == 0:
		newCols = [pd* (1-((1-ao)*occlusionAmount)) for pd,ao in zip(peakDips,occlusion)]
	if aoType == 1:
		newCols = [pd * clamp( (ao*4),0,1 ) for pd,ao in zip(peakDips,occlusion)]

	setRedVertCols(obj, newCols)
		
		
#return peaks and dips info for vert list
def peaksAndDips(obj, scale, bias):
	
	t0 = time.clock()
	
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	
	peakDips = []
	
	for v in range(0,meshFn.numVertices):
	
		#get avg vertex normal
		vNormal = meshFn.getVertexNormal(v, 0, space=om.MSpace.kWorld)
		
		#get list of edge indexes on this vert
		edgeNames = mc.polyListComponentConversion( (obj+".vtx[" + str(v) + "]"), toEdge=True)
		edgeNames = mc.ls(edgeNames, fl=True)
		edges = [getComponentIndex(e) for e in edgeNames] 
		
		#get position of first point
		vertPos = meshFn.getPoint(v, space=om.MSpace.kWorld)
				
		#get normalized edge vectors
		edgeVectors = om.MVectorArray()
		for edge in edges:
			edgeVerts = list(meshFn.getEdgeVertices(edge))
			edgeVerts.remove(v)
			vertPos2 = meshFn.getPoint(edgeVerts[0], space=om.MSpace.kWorld)
			
			#edgeVector = om.MVector()
			edgeVector = (vertPos2-vertPos).normalize()
			#edgeVector.normalize()
						
			edgeVectors.append(edgeVector)
		
		#find angles between edges and vert normal
		angles = [ e.angle(vNormal) for e in edgeVectors ]

		peakDips.append( float(sum(angles))/len(angles) )  #store average angle
		
	#scale, bias and clamp values
	for i in range(0,len(peakDips)):
		peakDips[i] = max(min( (((peakDips[i] -1.57) * scale) + bias),1 ) ,0)
	
	t = time.clock() - t0
	print "Time to calculate peaks and dips: %f" % t
	
	return peakDips
	
	


#converts a list of shapes to transforms
def shapesToTransforms(shapes):
	transforms = []
	for shape in shapes:
		if mc.objExists(shape):
			newTransforms = mc.listRelatives(shape, fullPath=1, parent=1)
			transforms.append(newTransforms[0])
	transforms = list(set(transforms)) #remove duplicates
	return transforms;

#returns the bounding box for the car including wheels, not including cols, shadows, or reflections.
def getDamageBounds():
	cols = mc.ls("*_COL", long=1, type="transform")
   	shad = mc.ls("*_SHADOW", long=1, type="transform")
	refl = mc.ls("REFLECTION_*", long=1, type="transform")
	boos = mc.ls("BOOST_*", long=1, type="transform")
	objList = shapesToTransforms(mc.ls(long=1, type="mesh"))
	
	rejects = cols + shad + refl + boos
	objList = [obj for obj in objList if obj not in rejects]
	
	bb = mc.polyEvaluate(objList, boundingBox=1)	
	#((xmin,xmax),(ymin,ymax),(zmin,zmax))
	
	return bb

#clamps x between min and max
def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

#avg is a flag to paint a single average colour to the verts (used for window shattering)
def paintDamageLookup(obj, avg):
	
	#create newcolour set if needed
	colourSets = mc.polyColorSet(obj, q=1, allColorSets=1)
	if ("damageLookup_colorSet" not in colourSets):
		mc.polyColorSet(obj, create=1, colorSet="damageLookup_colorSet", representation="RGB")
	mc.polyColorSet(obj, currentColorSet=1, colorSet="damageLookup_colorSet")
	
	bb = getDamageBounds()	
	#((xmin,xmax),(ymin,ymax),(zmin,zmax))
	
	print ""
	print bb
	
	xRange = bb[0][1] - bb[0][0]
	yRange = bb[1][1] - bb[1][0]
	zRange = bb[2][1] - bb[2][0]
	
	print "Geting meshfn"
	
	#get obj meshfn
	meshFn = getMeshFN(obj)
	
	colourList = om.MColorArray()
	numVerts = meshFn.numVertices
	
	print "if avg:"
	
	if avg:
		
		print "avg found"
		
		pAvg = [0.,0.,0.]
		for v in range(0,numVerts):
			pos = meshFn.getPoint(v, space=om.MSpace.kWorld)
			pAvg[0] += pos.x
			pAvg[1] += pos.y
			pAvg[2] += pos.z
		pAvg[0] /= numVerts
		pAvg[1] /= numVerts
		pAvg[2] /= numVerts
		pos = om.MPoint([pAvg[0],pAvg[1],pAvg[2]])
		
		print "average pos = "; print pos
		
		for v in range(0,numVerts):
			r = clamp ( ( (pos.x - bb[0][0]) / xRange),0,1 ) #** 2.2
			g = clamp ( ( (pos.y - bb[1][0]) / yRange),0,1 ) #** 2.2
			b = clamp ( ( (pos.z - bb[2][0]) / zRange),0,1 ) #** 2.2
			colourList.append(om.MColor( (r,g,b) ))
	else:
		
		print "non avg found"
		
		for v in range(0,numVerts):
			pos = meshFn.getPoint(v, space=om.MSpace.kWorld) 
			r = clamp ( ( (pos.x - bb[0][0]) / xRange),0,1 ) #** 2.2
			g = clamp ( ( (pos.y - bb[1][0]) / yRange),0,1 ) #** 2.2
			b = clamp ( ( (pos.z - bb[2][0]) / zRange),0,1 ) #** 2.2
			colourList.append(om.MColor( (r,g,b) ))
	
	meshFn.setVertexColors(colourList, range(0,numVerts))
	
	#switch back to colorSet1
	if ("colorSet1" in colourSets):
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		

	
#paint damage vectors from _DAM objects to colour set	
def paintDamageVector(obj):
	
	#create newcolour set if needed
	colourSets = mc.polyColorSet(obj, q=1, allColorSets=1)
	if ("damageVector_colorSet" not in colourSets):
		mc.polyColorSet(obj, create=1, colorSet="damageVector_colorSet", representation="RGB")
	mc.polyColorSet(obj, currentColorSet=1, colorSet="damageVector_colorSet")
	
	#get damage object
	damObj = getShortNameOf(obj) + "_DAM"
	
	if mc.objExists(damObj):
		
		#get obj meshfn
		meshFn = getMeshFN(obj)
		meshFnDam = getMeshFN(damObj)
		colourList = om.MColorArray()
		numVerts = meshFn.numVertices
		numDamVerts = meshFnDam.numVertices
		
		if numVerts == numDamVerts:
			for v in range(0,numVerts):
				pos = meshFn.getPoint(v, space=om.MSpace.kWorld) 
				damPos = meshFnDam.getPoint(v, space=om.MSpace.kWorld) 

				#store damage offsets
				damageVector = pos - damPos
				damageVector *= 2
				halfVector = om.MVector(0.5,0.5,0.5)
				damageVector += halfVector
			
				colourList.append(om.MColor(damageVector)) # (damageVector.x,damageVector.y,damageVector.z) ))

			meshFn.setVertexColors(colourList, range(0,numVerts))
		else:
			print ("WARNING: Could not set damage vectors for " + obj + " - damage object has a different vertex count")
			
	else:
		print ("Damage object: " + damObj + " not found. Setting vertex colours to zero deformation.");
		mc.polyColorPerVertex(obj, rgb=(0.5,0.5,0.5))
		
	#switch back to colorSet1
	if ("colorSet1" in colourSets):
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")


#sets the rgb vertex colours 0.5 (no damage vectors)
def setVertColsToNoDamageVector(obj):
	
	#create newcolour set if needed
	colourSets = mc.polyColorSet(obj, q=1, allColorSets=1)
	if ("damageVector_colorSet" not in colourSets):
		mc.polyColorSet(obj, create=1, colorSet="damageVector_colorSet", representation="RGB")
	mc.polyColorSet(obj, currentColorSet=1, colorSet="damageVector_colorSet")
	
	meshFn = getMeshFN(obj)
	colours = om.MColorArray()
	for i in range(0, meshFn.numVertices):
		colours.append(om.MColor((0.5,0.5,0.5)))
	meshFn.setVertexColors(colours, range(0,meshFn.numVertices))
	
	#switch back to colorSet1
	if ("colorSet1" in colourSets):
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		
		
		
		
def movePivot(nodeToAlign, target):
# moves the object's pivot to the same position as the target object
# must remove hierarchy before using
# no locked normals preservation code, so doesn't work with rotation & locked normals 

	#zero pivot offsets if needed
	zeroPivotOffsetVertCheck(target)
	zeroPivotOffsetVertCheck(nodeToAlign)
	
	meshFN = getMeshFN(nodeToAlign)
	targetTransFN = getTransFN(target)
	nodeToAlignTransFN = getTransFN(nodeToAlign)
	 
	#get the target transform matrix
	targetMatrix = targetTransFN.transformation()
		
	#store vertex positions
	vertPositions = meshFN.getPoints(space=om.MSpace.kWorld)
		
	#apply transform matrix to node
	nodeToAlignTransFN.setTransformation(targetMatrix)
	
	#move verts back into place
	meshFN.setPoints(vertPositions, space=om.MSpace.kWorld)
	
	





def zeroPivotOffsetVertCheck(obj):
#added check to ensure verts don't move - needed for parts with constraints
#also works on a given object rather than a selection
	
	locked = mc.listAttr((obj + ".translate"), locked=1)
	if locked: return
	
	#save vert positions
	mesh=1
	try:
		meshFn = getMeshFN(obj)
		vertPositions = meshFn.getPoints(space=om.MSpace.kWorld);
	except:
		mesh=0
		
	
	#freeze transform
	mc.makeIdentity(obj, apply=1, t=1, r=0, s=0)
	#move to the origin
	mc.move( 0, 0, 0, obj, rpr=1)

	objX = mc.getAttr( (obj + ".translateX") ) * (-1)
	objY = mc.getAttr( (obj + ".translateY") ) * (-1)
	objZ = mc.getAttr( (obj + ".translateZ") ) * (-1)

	#freeze transform again
	mc.makeIdentity(obj, apply=1, t=1, r=0, s=0)

 	mc.setAttr ( (obj + ".translateX"), objX)
 	mc.setAttr ( (obj + ".translateY"), objY)
 	mc.setAttr ( (obj + ".translateZ"), objZ)
	
	#restore vert positions
	if mesh: meshFn.setPoints(vertPositions, space=om.MSpace.kWorld)
	 

#turns off mud for selected objs
def paintMudOff():
   	cols = mc.ls("*_COL", long=1, type="transform")
   	shad = mc.ls("*_SHADOW", long=1, type="transform")
	objList = shapesToTransforms(mc.ls(long=1, type="mesh"))

	selected = mc.ls(sl=1, long=1)
	if len(selected)>0: 
		objList = selected
	#if objs are selected, use those instead
	else:
		confirm = mc.confirmDialog( title="WARNING", 
			message="No objects selected! Do you want to apply zero mud to all objects in scene?", 
			button=("Yes","No"), 
			defaultButton="No", cancelButton="No", dismissString="No")
		if confirm == "No": objList = []
	#warn user before un-mudding everything

	objList = list(set(objList))
	objList = [n for n in objList if n not in cols]
	objList = [n for n in objList if n not in shad]
	
	for obj in objList:
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		setGreenVertColsToBlack(obj)

def paintMud():
#paints mud onto selected objects with settings provided from gui
	mel.eval("boltRestoreHierarchy;")
	
	allInterior = []
	if mc.objExists("INTERIOR_SHELL"):
		children = mc.listRelatives("INTERIOR_SHELL", allDescendents=1, type="transform")
		if children: allInterior += children
		allInterior.append("INTERIOR_SHELL")
	
	innerDoors = mc.ls("DOOR_PANEL_*", type="transform")
	if innerDoors: allInterior += innerDoors
	
	doorHandles = mc.ls("DOOR_OPEN_*", type="transform")
	if doorHandles: allInterior += doorHandles
	
	mel.eval("boltRemoveHierarchy;") #hack needed otherwise normal directions are wrong on bike forks
	
	allInterior = [mc.ls(n, long=1)[0] for n in allInterior]
	
	#print allInterior
	
	locs = shapesToTransforms(mc.ls(long=1, exactType="locator")) 
	shad = shapesToTransforms(mc.ls(long=1, type="evoamboccvollocator"))
	lods = mc.ls("*_LOD*", long=1, type="transform")
	cols = mc.ls("*_COL", long=1, type="transform")
	#get misc lists
		
	wheels = mc.ls( ("WHEEL_FL","WHEEL_FR","WHEEL_BL","WHEEL_BR"), long=1)
	if len(wheels) != 4: 
		raise Error("Mud painting failed! Wheel(s) missing from scene - needed to calculate mud spray")
	
	allWheels = mc.ls("WHEEL_*", long=1, type="transform")
	allDiscs = mc.ls("DISC_*", long=1, type="transform")
	boost = mc.ls("BOOST_*", long=1, type="transform")
	
	objList = shapesToTransforms(mc.ls(long=1, geometry=1))
	
	selected = mc.ls(sl=1, long=1)
	if len(selected)>0: 
		objList = selected
	#if objs are selected, use those instead
	else:
		confirm = mc.confirmDialog( title="WARNING", 
			message="No objects selected! Do you want to redo mud on all objects in scene?", 
			button=("Yes","No"), 
			defaultButton="No", cancelButton="No", dismissString="No")
		if confirm == "No": objList = []
	#warn user before mudding everything
	
	objList = list(set(objList))
	objList = [n for n in objList if n not in cols]
	objList = [n for n in objList if n not in locs]
	objList = [n for n in objList if n not in shad]
	objList = [n for n in objList if n not in boost]
	#work out objlist of standard muddable shapes
	
	for obj in objList:
		mc.delete(obj, constructionHistory=1)
	#delete history - 4x speed up in some cases
	
	#seperate out selected wheels, disks and interior into seperate list	
	selWheels   = [n for n in allWheels if n in objList]
	objList     = [n for n in objList if n not in selWheels]
	selDiscs    = [n for n in allDiscs if n in objList]
	objList     = [n for n in objList if n not in selDiscs]
	selInterior = [n for n in allInterior if n in objList]
	objList     = [n for n in objList if n not in selInterior]
		
	#print objList
	#print selInterior
	#print selWheels
	#print selDiscs
	
	mc.undoInfo(state=0)
	#turn off otherwise maya runs out of memory.
		
	t0 = time.clock()
	
	print "Calculating Exterior Mud:"
	for obj in objList:
		print ("Calculating Mud for " + obj)
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		mudCols = getMud(obj)
		if mudCols: setGreenVertCols(obj, mudCols)
	
	print "Calculating Interior Mud:"
	for obj in selInterior:
		print ("Calculating Mud for " + obj)
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		setGreenVertColsToBlack(obj)
	
	print "Calculating Disk Mud:"
	for obj in selDiscs:
		print ("Calculating Mud for " + obj)
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		setGreenVertColsToBlack(obj)
	
	print "Calculating Wheel Mud:"
	for obj in selWheels:
		print ("Calculating Mud for " + obj)
		mc.polyColorSet(obj, currentColorSet=1, colorSet="colorSet1")
		mudCols = getWheelMud(obj)
		if mudCols: setGreenVertCols(obj, mudCols)
	
	mel.eval("boltRestoreHierarchy")
	mc.undoInfo(state=1)
	
	t = time.clock() - t0
	print "Time to paint all mud: %f" % t
	
	print "MUD COLOURS DONE!"
		
		
#return mud colours for vert list
def getMud(obj):
	
	#test for valid object
	isMesh = mc.listRelatives(obj, type="mesh")
	if not isMesh:
		print ("Could not paint mud for non mesh object: " + obj) 
		return []
	
	baseColour = 0.
	op_groundProximity = 0.2
	op_normalBias = 0.3
	op_crevice = 0.2
	op_edges = 0.1
	op_wheelEmitter = 0.2
	
	t0 = time.clock()
	
	#convert obj to vert list
	verts = mc.polyListComponentConversion(obj, toVertex=True)
	verts = mc.ls(verts, fl=True)
				
	occlusionCols = getVertCols(verts, "A")
	scrapeCols = getVertCols(verts, "R")
		
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	
	mudCols = []
	
	for v in range(0,meshFn.numVertices):
	
		vNormal = meshFn.getVertexNormal(v, 0, space=om.MSpace.kWorld)
		vertPos = meshFn.getPoint(v, space=om.MSpace.kWorld)
		scrape = scrapeCols[v]
		
		#GROUND PROXIMITY - Fall off depending on distance from ground
		groundProximity = 1 - (vertPos.y / 1.2);
		groundProximity = clamp(groundProximity, 0, 1)
		
		#NORMAL BIAS - More Mud on underneath and rear faces
		normalBiasX = (1 - abs(vNormal.x))
		normalBiasY = 1+(-1 * vNormal.y)
		if normalBiasY < 0: normalBiasY = 0
		normalBiasZ = 1+(-1 * vNormal.z)
		if normalBiasZ < 0: normalBiasZ = 0
		normalBias = normalBiasX * normalBiasY * normalBiasZ
		
		#CREVICE MUD - Takes info from the ambient occlusion data
		crevice = (1 - occlusionCols[v])
		
		#EDGE MUD - use info from red colour channel
		edges = scrapeCols[v]
		
		#WHEEL EMITTERS
		wheelEmitter = getWheelEmitter(vertPos)
		
		mud = baseColour + (op_groundProximity * groundProximity) + (op_normalBias * normalBias) + (op_crevice * crevice) + (op_edges * edges) + (op_wheelEmitter * wheelEmitter)
		mud = clamp(mud, 0, 1)
		mudCols.append(mud)  #store mud
		
	t = time.clock() - t0
	print "Time to calculate mud: %f" % t
	
	return mudCols



#returns the mud value sprayed up from wheels
def getWheelEmitter(vertPos):
	wheelEmit = 0;
	wheelDiam = 0.65;
	wheelBase = 2.7;
	
	wheels = mc.ls( ("WHEEL_FL","WHEEL_FR","WHEEL_BL","WHEEL_BR"), long=1) 
	
	for wheel in wheels:

		wheelPos = mc.xform(wheel, q=1, ws=1, rp=1)

		#calculate z fadeoff
		zDist = vertPos.z - wheelPos[2]
		zCol = 1
		if zDist > 0:
			zCol = (1 - zDist/(0.5*wheelDiam))
		else:
			zCol = 2*(1 - (zDist/(-1.3*wheelBase)));  
		zCol = clamp(zCol,0,1)
				
		coneSize = 0.5 * wheelDiam
		if zDist < 0:
			coneSize = coneSize+(-1.1*(zDist/wheelBase))
		coneSize = pow(coneSize, 2) 
		#calculate cone diameter squared based on z distance 
		
		xyDist = pow( (vertPos.x-wheelPos[0]), 2) + pow( (vertPos.y-wheelPos[1]), 2)
		xyCol = 1-(xyDist/coneSize)
		xyCol = clamp(xyCol,0,1)
	
		wheelEmit += zCol * xyCol
	
	return wheelEmit
	

#returns mud values for wheels
def getWheelMud(obj):
	
	baseColour = 0.2
	op_crevice = 0.2
	op_edges = 0.1
	op_radial = 0.5
	
	t0 = time.clock()
	
	#convert obj to vert list
	verts = mc.polyListComponentConversion(obj, toVertex=True)
	verts = mc.ls(verts, fl=True)
				
	occlusionCols = getVertCols(verts, "A")
	scrapeCols = getVertCols(verts, "R")
	
	wheelPos = mc.xform(obj, q=1, ws=1, rp=1)
	bb = mc.polyEvaluate(obj, boundingBox=1)	
	wheelDiam = bb[1][1] - bb[1][0]
	radius = wheelDiam/2
	
	# Create a function set for the mesh.
	meshFn = getMeshFN(obj)
	
	mudCols = []
	
	for v in range(0,meshFn.numVertices):
	
		vertPos = meshFn.getPoint(v, space=om.MSpace.kWorld)
		
		#RADIAL DISTANCE - Fall off depending on distance from center of wheel
		radial = pow ( pow((vertPos.y-wheelPos[1]) , 2) + pow((vertPos.z-wheelPos[2]) , 2) ,0.5)
		radial = pow( (radial / radius), 10)
		
		#CREVICE MUD - Takes info from the ambient occlusion data
		crevice = (1 - occlusionCols[v])
		
		#EDGE MUD - use info from red colour channel
		edges = scrapeCols[v]
		
		
		mud = baseColour + (op_radial * radial) + (op_crevice * crevice) + (op_edges * edges)
		mud = clamp(mud, 0, 1)
		mudCols.append(mud)  #store mud
		
	t = time.clock() - t0
	print "Time to calculate mud: %f" % t
	
	return mudCols
