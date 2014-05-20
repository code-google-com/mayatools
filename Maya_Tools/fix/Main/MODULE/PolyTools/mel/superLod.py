import sys
import time #used to time code execution
import re
import os
import math
import maya.cmds as mc
os.putenv("KMP_DUPLICATE_LIB_OK", "TRUE") #allows us to import the intel optimised version of numpy
import numpy as np



def superLod (obj, minEdgeLength, loopRemovalAvgLimit, loopRemovalMaxLimit, smoothing, targetPolyPercentage, loopSize):
	
	#get target poly count
	startCount = mc.polyEvaluate(obj, triangle=1)
	currentCount = mc.polyEvaluate(obj, triangle=1)
	targetCount = int( currentCount * (targetPolyPercentage / 100.0) )
	reductionCount = currentCount - targetCount
	
	#guess how many edges are needed to achieve the polycount
	edgeReductionCount = int( reductionCount / 1.8)
	
	#get the indexes of all edges below minEdgeLength
	edgeLengths = getEdgeLengths(obj)
	shortEdgeIndexes = np.where(edgeLengths < minEdgeLength)[0]
	
	#handles the case of there being more short edges than needed to achieve target (avg 2 polys per vert collapsed)
	if (len(shortEdgeIndexes) > edgeReductionCount):
		# get the reduction count no of smallest edges
		shortEdgeIndexes = np.argsort(edgeLengths)[0:(edgeReductionCount)]
		
		print ("too many short edges found, deleting only shortest %i edges" % (len(shortEdgeIndexes)) )
		
		deleteEdges(obj, shortEdgeIndexes)
		
		collapseShortestEdges(obj, targetCount)
		
	else:
	
		deleteEdges(obj, shortEdgeIndexes)
		#delete edges
	
		currentCount = mc.polyEvaluate(obj, triangle=1)
		#loopSize = 6 #initial minimum loop size 
		count = 0
	
		#delete least significant loops
		while (currentCount > targetCount):
		
			count +=1
			if (count > 1000): break #emergency stop
			
			if (removeLeastSignificantEdgeLoop(obj, loopSize, loopRemovalAvgLimit, loopRemovalMaxLimit) == 0):
				#if no loops found, drop loop size
				loopSize-=1
				print ("Loopsize reduced to: %s" %(loopSize))
				if (loopSize == 2): 
					print "quiting due to min loop length being reached" 
					break
			currentCount = mc.polyEvaluate(obj, triangle=1)
	
		
	#if no loops available, start collapsing more edges
	collapseShortestEdges(obj, targetCount)
		
	if (smoothing > 0):
		print ("Setting smoothing angle to %i degrees." %(smoothing) )
		mc.polyNormalPerVertex(obj, ufn=1)
		mc.polySoftEdge(obj, angle=smoothing, ch=0)
	
	currentCount = mc.polyEvaluate(obj, triangle=1)
	
	print ("%s reduced from %i to %i polys" %(obj,startCount,currentCount) )



#keep deleting chunks of shortest edges until we are at required poly count
def collapseShortestEdges(obj, targetCount):

	if (targetCount < 20): targetCount = 20
	currentCount = mc.polyEvaluate(obj, triangle=1)
	
	#guess how many edges are needed to achieve the polycount
	reductionCount = currentCount - targetCount
	edgeReductionCount = int( reductionCount / 1.8)
	
	while (currentCount > targetCount):
		
		#guess how many edges are needed to achieve the polycount
		reductionCount = currentCount - targetCount
		edgeReductionCount = int( reductionCount / 1.8)
		if (edgeReductionCount < 1): edgeReductionCount = 1 
		
		edgeLengths = getEdgeLengths(obj)
		shortestEdgeIndexes = np.argsort(edgeLengths)[0:(edgeReductionCount)]
		deleteEdges(obj, shortestEdgeIndexes)
		currentCount = mc.polyEvaluate(obj, triangle=1)
		
		print ("%i edges collapsed" % (edgeReductionCount))


#deletes the edges specified in the supplied int list
def deleteEdges(obj, edges):
	
	edgeStrings = [ ("%s.e[%i]" %(obj, edge)) for edge in edges ] 
	
	if ( len(edgeStrings) > 0):
		mc.polyCollapseEdge(edgeStrings, ch=0)
			

def getEdgeLengths(obj):
	
	#convert the edges to a string list, 
	noEdges = mc.polyEvaluate(obj, edge=1 )
	edges = [ ("%s.e[%i]" %(obj, edge)) for edge in range(noEdges) ]
	
	orderedVerts = np.array([])
	
	for edge in edges:
		verts = toVerts([edge])
		orderedVerts = np.append(orderedVerts , verts)

	noVerts = np.size(orderedVerts)
	vertPositions = np.zeros( (noVerts, 3) )

	for i in range(noVerts):
		vertPositions[i] = mc.pointPosition(orderedVerts[i], world=1)
	
	edgeVectors = vertPositions[0::2] - vertPositions[1::2]
	edgeLengths = np.array( [ np.sqrt(np.vdot(v,v)) for v in edgeVectors ] )
	
	return edgeLengths


#finds all edge loops on an object and removes the least significant one.
#returns 1 if edges removed, else returns 0
def removeLeastSignificantEdgeLoop(obj, loopSize, loopRemovalAvgLimit, loopRemovalMaxLimit):
	
	#t0 = time.clock()
	
	loops = getLoops(obj, loopSize)
	
	#t = time.clock() - t0
	#print "Time to get edge loops %f" % t
	#t0 = time.clock()
	
	if ( len(loops) == 0 ):
		return 0
	
	#get list of all poly normals
	normText = mc.polyInfo(obj, fn=1)
	polyNorms =  [ ([float(x) for x in y.split()[2:5] ]) for y in normText ]

	loopAngles = []
	for loop in loops:
		#measure loop angles, reject any avg angles where the max angle is above the limit.
		loopMeasurements = getAverageAngleOfLoop(obj, loop, polyNorms)
		if loopMeasurements[1] > loopRemovalMaxLimit:
			loopAngles.append(180.0)
		else:
			loopAngles.append(loopMeasurements[0])
	
	#t = time.clock() - t0
	#print "Time to measure loop angles %f" % t
	#t0 = time.clock()
	
	
	if ( len(loopAngles) == 0 ):
		print "No loop angles found... quitting"
		return 0
	
	#don't remove anything with an avg angle greater than the limit
	if ( min(loopAngles) > loopRemovalAvgLimit ):
		print "Loop angles all above limit... quitting"
		return 0
		
	loopToDelete = loopAngles.index(min(loopAngles))
	
	edgesToDelete = [ ("%s.e[%i]" %(obj, edge)) for edge in loops[loopToDelete] ]
	
	if ( len(edgesToDelete) > 0 ):	
		mc.polyDelEdge(edgesToDelete, ch=0, cv=1)
		return 1
	else:
		return 0
	
	
	
	
#given an int list of loop edges on an obj, returns tupple of the average angle of edges perpendicular to the loop, and the max angle
#now returns angles in degrees
def getAverageAngleOfLoop(obj, loop, polyNorms):
	
	#t0 = time.clock()
	
	edges = [ ("%s.e[%i]" %(obj, edge)) for edge in loop ]
	faces = [ toFaces(edge) for edge in edges ]
	faces = sum(faces, []) #make list 1d
	faceIDs = [ getComponentNumber(face) for face in faces ]
	loopFaceNorms = np.array( [polyNorms[x] for x in faceIDs] )
	angles = np.array( [np.dot(loopFaceNorms[k],loopFaceNorms[k+1]) for k in range(0, len(loopFaceNorms), 2) ])
	
	#prevent floating point induced crash
	np.clip(angles, -1, 1, out=angles)
	
	avgAngle = math.degrees(math.acos(np.mean(angles)))
	maxAngle = math.degrees(math.acos(np.min(angles)))
	
	#t = time.clock() - t0
	#print "Time to calculate average angle on loop %f" % t
	#t0 = time.clock()

	return (avgAngle, maxAngle)


#get list of loops larger than the specified no of edges, on the specified object
#returns a list of int lists
def getLoops(obj, minNoEdges):
	
	#print "searching for long edge loops..."
	
	noEdges = mc.polyEvaluate(obj, edge=1 )
	
	longLoops = []
	processedEdges = []
	
	for edge in range(noEdges):
		if edge not in processedEdges:
			loopEdges = edgeToLoop(obj, edge)
			processedEdges.extend(loopEdges)
			if len(loopEdges) > minNoEdges:
				longLoops.append(loopEdges)
	
	#print ("%i loops longer than %i found.") %( len(longLoops), minNoEdges )
	return longLoops


	
##gets a simple edge loop, no fancy stuff, returns a list of ints
def edgeToLoop(obj, edge):
	loop = mc.polySelect(obj, noSelection=1, edgeLoop=edge)
	return loop




def superLoop():
	
	getSmallestLoop = True
	
	edgeSel = getSelectedEdges()
	
	#get selected object
	m = re.match("^[^\.]*", edgeSel[0])
	objectName = m.group(0)
	
	#if one edge, select full loop
	#if 2 edges select the longest / shortest connection (alternately?)
	
	loops = []
	
	for edge in edgeSel:
		#avoid calculating the same loop twice
		edgeFound = False
		for loop in loops:
			if edge in loop:
				edgeFound = True
		if not edgeFound:		
			loops.append(getLoop(edge))
	
	selectedLoops = []
	for loop in loops:
		
		selectedEdgesInLoop = listAnd(loop, edgeSel)
		
		if len(selectedEdgesInLoop) == 1:
			selectedLoops.append(loop)
		if len(selectedEdgesInLoop) > 2:
			selectedLoops.append(loop)
		if len(selectedEdgesInLoop) == 2:
			edge1 = loop.index(selectedEdgesInLoop[0])
			edge2 = loop.index(selectedEdgesInLoop[1])
			if edge1 > edge2:
				edge1, edge2 = edge2, edge1
			if isFullLoop(loop):
				if ((edge2-edge1) > len(loop)/2 and getSmallestLoop) or \
							((edge2-edge1) < len(loop)/2 and not getSmallestLoop):
					selectedLoops.append(loop[0:edge1])
					selectedLoops.append(loop[edge2:])
					continue
			selectedLoops.append(loop[edge1:edge2])
			
	for loop in selectedLoops:
		mc.select(loop, add=1)

#returns list of currently selected edges
def getSelectedEdges():
	sel = mc.ls(sl=1, fl=1)
	edgeSel = []
	for s in sel:
		if ".e[" in s:
			edgeSel.append(s)
	if len(edgeSel) == 0:
		raise Exception("No edges selected!")
	return edgeSel



def superLoopRemove():
	edges = getSelectedEdges()
	verts = toVerts(edges)
	vertsSet = mc.sets(verts, vertices=1)
	mc.polyDelEdge(edges, cleanVertices=True )
	#keep deleteing verts until the set is empty
	while mc.sets(vertsSet, q=1):
		#print "vertset to remove:", mc.sets(vertsSet, q=1)
		vertToRemove = mc.ls( mc.sets(vertsSet, q=1), fl=1)[0]
		smartVertRemove(vertToRemove)
	mc.select(cl=1)

#removes verts in a smarter way than maya
def smartVertRemove(vert):
	
	edges = toEdges(vert)
	polys = toFaces(vert)
	verts = listSubtract(toVerts(edges),[vert]) # list of all surrounding verts
	transform = getTransFromComponent(vert)
	
	polySet = mc.sets(polys, fc=1)
	
	if len(edges)>2:
		for poly in polys:
			#if poly is not a tri, then verts need connecting
			if len(toEdges(poly)) != 3:
				vertsToConnect = listAnd(toVerts(poly),verts)
				if len(vertsToConnect) != 2:
					raise Exception("Could not connect verts - wrong number found!")
				connectVerts(vertsToConnect[0],vertsToConnect[1])
	
	deleteVertFlag = False
	for e in edges[:0:-1]: #reverse order, doesn't delete the last edge as this disappears by itself
		if len(toFaces(e)) == 2:
			mc.delete(e)
		elif len(toFaces(e)) == 1:
			deleteVertFlag = True
		else:
			raise Exception("smartVertRemove does not work with non-manifold edges")
	
	if deleteVertFlag:
		print "deleting vert"
		mc.delete(vert)

	#quadrangulate any remaining polys with 5 or more edges
	
	polys = mc.ls(mc.sets(polySet, q=1), fl=1)
	bigPolys = []
	for p in polys:
		if len(toEdges(p)) >= 5:
			bigPolys.append(p)
	if bigPolys:
		bigPolySet = mc.sets(bigPolys, fc=1)
		mc.polyTriangulate(mc.sets(bigPolySet, q=1))
		mc.polyQuad(mc.sets(bigPolySet, q=1))
	

#connects 2 verts providing they are on the same poly
def connectVerts(v1,v2):
	transform = getTransFromComponent(v1)
	polys1 = toFaces(v1)
	polys2 = toFaces(v2)
	polys3 = listAnd(polys1,polys2)
	
	if polys3:
		edges = toEdges(polys3[0])
		edges1 = listAnd(edges, toEdges(v1))
		edges2 = listAnd(edges, toEdges(v2))
		e1 = edges1[0]
		e2 = edges2[0]
		
		end1 = getEdgeEnd(e1,v1)
		end2 = getEdgeEnd(e2,v2)
		
		#print "attempting toConnect: ", transform, v1, e1, end1, v2, e2, end2
		
		mc.polySplit(transform, sma=90, ip=[ (getComponentNumber(e1), end1), (getComponentNumber(e2), end2) ] )
		
	else:
		raise Exception("Could not connectVerts - and not on same poly!")

#returns 0. or 1. depending if vert is at start or end of edge.
def getEdgeEnd(edge,vert):
	
	#print "getting edge end for", edge, vert, 
	#print mc.polyInfo(edge, ev=1)[0].split()
	
	lastVert = int( mc.polyInfo(edge, ev=1)[0].split()[3] )
	if getComponentNumber(vert) == lastVert:
		return 1.
	else:
		return 0.
						
#returns the transform node of a given component name
def getTransFromComponent(component):
	m = re.match("^[^\.]*", component)
	return m.group(0)
	#add more code to ensure that we have transform not shape!

#returns the component number as an int
def getComponentNumber(component):
	cType = ""
	if ".vtx[" in component: cType = ".vtx["
	elif ".e[" in component: cType = ".e["
	elif ".f[" in component: cType = ".f["
	else: raise Exception("Component type not detected by getComponentNumber")
		
	num = component.split(cType)[-1:][0][:-1]
	if ":" in num:
		raise Exception("Component ranges not handled by getComponentNumber")
	return int(num)

#converts a string list into an int list of component IDs
def getComponentNumbers(componentStrings):
	
	componentIDs = [ getComponentNumber(component) for component in componentStrings ]
	return componentIDs

#returns the polygons common to two edges
def getSharedPoly(edge1,edge2):
	edge1Polys = toFaces(edge1)
	edge2Polys = toFaces(edge2)
	return listAnd(edge1Polys, edge2Polys)

#returns the opposite edge on a vert with 4 edges
def getOppositeEdge(edge, vert):
	edges = toEdges(vert)
	polys = toFaces(edge)
	polyEdges = toEdges(polys)
	oppositeEdge = listSubtract(edges, polyEdges)
	return oppositeEdge[0]
		
		
	
	

#returns true if the loop start and end meet up
def isFullLoop(loop):
	
	print "len loop ", len(loop)
	print "len loop verts ", len(toVerts(loop))
	
	if len(toVerts(loop)) == len(loop):
		return True
	else:
		return False

def getLoop(edge):
	
	loopEdges = [edge]
	lastEdge1 = edge
	lastEdge2 = edge
	loopVerts = toVerts(edge)
	lastVert1 = loopVerts[0]
	lastVert2 = loopVerts[1]
	
		
	while lastEdge1 or lastEdge2: #keep going until these are both empty
		if lastEdge1 and lastVert1:
			newEdge = findNextEdge(lastEdge1, lastVert1)
			lastEdge1 = newEdge
			if newEdge in loopEdges: break 
			if newEdge:
				loopEdges.append(newEdge)
				newVerts = toVerts(newEdge)
				for v in newVerts:
					if v not in loopVerts:	
						loopVerts.append(v)
						lastVert1 = v
		if lastEdge2 and lastVert2:
			newEdge = findNextEdge(lastEdge2, lastVert2)
			lastEdge2 = newEdge
			if newEdge in loopEdges: break 
			if newEdge:
				loopEdges.insert(0,newEdge)
				newVerts = toVerts(newEdge)
				for v in newVerts:
					if v not in loopVerts:	
						loopVerts.insert(0,v)
						lastVert2 = v
	
	return loopEdges
			
		

	
	


#given an edge and a vert (to define direction) returns the next edge on the loop
def findNextEdge(edge, vert):
	
	#print "finding next edge from: ", edge, "vert: ", vert
	
	polysOnVert = toFaces(vert)
	polysOnEdge = toFaces(edge)
	edgesOnVert = toEdges(vert)
	
	#does this vert have any open edges? Makes loop more difficult if so.
	openEdges = False
	for e in edgesOnVert:
		if len(toFaces(e)) != 2:
			openEdges = True
			break

	#if 2 edges, choose the other edge (loop round corners?)
	"""
	if len(polysOnVert)==1 and len(polysOnEdge)==1:
		
		print "corner edge found"
		
		if edge in edgesOnVert:
			nextEdge = listSubtract(edgesOnVert, [edge])
			return nextEdge[0]
		else:
			print "Error: 2 edged vert failed"
			return ""
	"""

	#if no polys other than those on current edge, then assume end of loop
	if isListSubset(polysOnVert, polysOnEdge):
		print vert, " is on end of edge"	
		return ""
		
	#if even number of edges, choose the middle one
	if len(edgesOnVert) % 2 == 0 and not openEdges:
		nextEdges = edgesOnVert
		notTheseEdges = [edge]
		while len(nextEdges) > 1:
			notTheseEdges = toEdges(toFaces(notTheseEdges))
			notTheseEdges = listAnd(notTheseEdges, edgesOnVert)
			nextEdges = listSubtract(edgesOnVert, notTheseEdges)
		if nextEdges[0]:
			return nextEdges[0]

	#if odd no of edges, or open edges, pick the straightest edge
	nextEdges = listSubtract(edgesOnVert, [edge])
	edgeVector = getEdgeVector(edge, vert)
	
	edgeVectors = np.empty( (len(nextEdges),3) )
	c=0
	for e in nextEdges:
		edgeVectors[c] = getEdgeVector(e, vert)
		c+=1
				
	#find angles between edges and vert normal (cosT=a.b)
	angles = np.arccos( np.apply_along_axis(np.vdot, 1, edgeVectors, edgeVector) )
	
	largestAngle = 0
	largestAngleIndex = 0
	for i in range(0,len(nextEdges)):
		if angles[i] > largestAngle:
			largestAngle = angles[i]
			largestAngleIndex = i
	
	return nextEdges[largestAngleIndex]


#returns a numpy vector for a maya edge, starting from the given vert, normalizes result by default
def getEdgeVector(edge, vert, normalized=1):
	verts = toVerts(edge)
	verts = listSubtract(verts, [vert])
	v1 = np.array(mc.pointPosition(vert, world=1))
	v2 = np.array(mc.pointPosition(verts[0], world=1))
	v3 = v2-v1
	if normalized:
		normalizeVector(v3)
	return v3	
	
#normalizes a 3d numpy vector
def normalizeVector(vector):
	magnitude = getMagnitude(vector)
	vector /= magnitude
	
#normalizes a 2d array of vectors
def normalizeVectorArray(vectors):
	magnitudes = np.apply_along_axis(getMagnitude, 1, vectors)
	vectors /= magnitudes.reshape(-1,1) #gives the array a second dimension of 1 - needed for division to work

#returns the magnitude of the given 1d vector array
def getMagnitude(vector):
	return np.sqrt(np.dot(vector,vector.conj()))
	#3* faster than: np.sqrt(np.sum(np.abs(normals[0])**2))



#returns true if all elements of a are also in b
def isListSubset(a,b):
	for i in a:
		if i not in b:
			return False
	return True
	
#subtracts items in list b from list a
def listSubtract(a,b):
	c = [i for i in a if i not in b]
	return c
	
#returns items that are in list a AND list b
def listAnd(a,b):
	c = [i for i in a if i in b]
	return c
	
	
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

