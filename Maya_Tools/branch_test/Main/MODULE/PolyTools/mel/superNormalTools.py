import sys
import time #used to time code execution

import maya.cmds as mc
import maya.OpenMaya as om

import os
os.putenv("KMP_DUPLICATE_LIB_OK", "TRUE") #allows us to import the intel optimised version of numpy
import numpy as np


def getHardEdges(obj):
	t0 = time.clock()
	
	edgeList = mc.polyInfo(edge, ev=1)
	if (edgeInfo[0] "Hard\n"`) return 1;
	return 0;


	

	t = time.clock() - t0
	print "Time to read all edges %f" % t
	
	return edgeList



def toFaces(inComponents):
	output = mc.polyListComponentConversion(inComponents, toFace=1)
	output = mc.ls(output, fl=1)
	return output
def toVerts(inComponents):
	output = mc.polyListComponentConversion(inComponents, toVertex=1)
	output = mc.ls(output, fl=1)
	return output
def toEdges(inComponents):
	output = mc.polyListComponentConversion(inComponents, toEdge=1)
	output = mc.ls(output, fl=1)
	return output
def toVFs(inComponents):
	output = mc.polyListComponentConversion(inComponents, toVertexFace=1)
	output = mc.ls(output, fl=1)
	return output













#gets all normals using api
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
	#	print "setting %s to %f" % (sel[i], newCols[i])
	#	mc.polyColorPerVertex( sel[i], b=newCols[i]) 
	
	#set colours with API - not working on bigrig41 wheels, unless you do a "resurrect corrupted shape nodes"
	meshFn.setVertexColors(cols, verts)
	
	# Turn off the mesh's color display.
	meshFn.findPlug('displayColors').setBool(False)
		
	t = time.clock() - t0
	print "Time to set all colours at once with array using api %f" % t
	
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
	