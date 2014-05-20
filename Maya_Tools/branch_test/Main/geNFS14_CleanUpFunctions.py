import maya.cmds as mc
import maya.OpenMaya
import maya.mel as mel
import os

def DeleteIsolatedMeshes( selection=[] ):
	print('CLEAN : DeleteIsolatedMeshes\n')
	numDeleted = 0
	deletedMeshes = []
	
	meshes = mc.ls(l=1, fl=1, typ='mesh')
	if selection != [] and selection != ['']:
		meshes = nodesOfTypeFromList(selection, 'mesh')	
	
	if meshes is not None and meshes != []:
		# Progress Bar Window	
		numJobs = len(meshes)
		progressBarInit(title='Cleanup', status='Deleting Isolated Meshes', numJobs=numJobs)
		i=0
		
		for mesh in meshes:
			conn = mc.listConnections(mesh, d=1, s=1)
			if conn is None:
				try:
					# Ensure it's unlocked
					mc.lockNode(mesh, l=0)
					print "Deleting",mesh
					mc.delete(mesh)
					numDeleted+=1
					deletedMeshes.append(mesh)
				except:
					print "Couldn't delete",mesh
			i+=1
			mc.progressWindow(edit=True, progress=i)
					
		mc.progressWindow (endProgress=True)
				
	print(str(numDeleted) + ' nodes deleted.\n')
	return deletedMeshes

def DeleteEmptyMeshes( selection=[] ):
	print('CLEAN : DeleteEmptyMeshes\n')
	numDeleted = 0
	deletedMeshes = []
	
	meshes = mc.ls(l=1, fl=1, typ='mesh')
	if selection != [] and selection != ['']:
		meshes = nodesOfTypeFromList(selection, 'mesh')	
	
	if meshes is not None and meshes != []:
		# Progress Bar Window	
		numJobs = len(meshes)
		progressBarInit(title='Cleanup', status='Deleting Empty Meshes', numJobs=numJobs)
		i=0
		
		for mesh in meshes:
			numFaces = mc.polyEvaluate(mesh, f=1)
			if numFaces == 0:
				try:
					# Ensure it's unlocked
					mc.lockNode(mesh, l=0)
					print "Deleting",mesh
					mc.delete(mesh)
					numDeleted+=1
					deletedMeshes.append(mesh)
				except:
					print "Couldn't delete",mesh
			i+=1
			mc.progressWindow(edit=True, progress=i)
					
		mc.progressWindow (endProgress=True)
				
	print(str(numDeleted) + ' nodes deleted.\n')
	return deletedMeshes
	
def DeleteIsolatedIntermediateNodes( selection=[] ):
	print('CLEAN : DeleteIsolatedIntermediateNodes\n')
	numDeleted = 0
	deletedNodes = []	
	
	numxforms = 0
	rootxforms = []

	xforms = mc.ls(l=1, fl=1, typ='transform')
	if selection != [] and selection != ['']:
		xforms = mc.ls(selection, fl=1, l=1, typ='transform')
			
	if xforms is not None and xforms != []:
		# Progress Bar Window
		numJobs = len(xforms)
		progressBarInit(title='Cleanup', status='Deleting Isolated Intermediate Nodes', numJobs=numJobs)
		i=0
		
		for x in xforms:
			# Only interested in root nodes
			parents = mc.listRelatives (x, parent=1, fullPath=1)
			if parents is not None:
				continue
			rootxforms.append(x)
			numxforms+=1

		for x in rootxforms:
			found = 0
			meshFound = 0

			# find all descendents that are meshes.
			rels = mc.listRelatives (x, allDescendents=1, fullPath=1)
			if rels is not None:
				for r in rels:
					if mc.nodeType(r) == "mesh":
						intermediate = mc.getAttr( str(r+'.intermediateObject') )
						if intermediate == 0:
							found = 1
							break	
						meshFound = 1

			# If there are meshes as descendents and they are all intermediates, delete everthing.
			if found==0 and meshFound==1:
				try:
					mc.lockNode(x, l=0)
					mc.delete(x)
					numDeleted+=1
					deletedNodes.append(x)
				except:
					pass
			i+=1
			mc.progressWindow(edit=True, progress=i)
		mc.progressWindow (endProgress=True)

	print(str(numDeleted) + " nodes deleted.\n")	
				
	return deletedNodes

def RemoveNamespaces( selection=[] ):
	print('CLEAN : RemoveNamespaces\n')

	numRenamed = 0
	renamedNodes = []
	nameSpacesToRemove = []
	nameSpacesRemoved = []

	nodes = mc.ls(l=1, fl=1)
	if selection != [] and selection != ['']:
		nodes = selection
	
	# Set the current namespace to the global namespace
	mc.namespace(set=":")

	depNodes = mc.ls(nodes, dep=1, fl=1)
		
	for node in depNodes:

		# Get 'leaf' name from full namespace qualified path.
		newName = node.split(':')[-1:][0]
				
		# Rename node without the namespace (if possible).
		if newName != node:
		
			nameSpaceToRemove = node.split(':')[:-1][0]
			nameSpacesToRemove.append(nameSpaceToRemove)		
		
			try:
				# Ensure it's unlocked
				mc.lockNode(node, l=0)
				mc.rename(node, newName)
			except:
				pass	# This will still rename the node it'll just be given a unique name automatically by Maya
			renamedNodes.append(node)
			numRenamed+=1
			
	# Remove redundant namespaces from the Scene
	nameSpacesToRemove = list(set(nameSpacesToRemove))
	
	# Progress Bar Window
	numJobs = len(nameSpacesToRemove)
	progressBarInit(title='Cleanup', status='Removing Namespaces', numJobs=numJobs)
	i=0	
	for nameSpace in nameSpacesToRemove:
		try:
			mc.namespace(f=1, rm=nameSpace)
			nameSpacesRemoved.append(nameSpace)
		except:
			pass
		i+=1
		mc.progressWindow(edit=True, progress=i)
	mc.progressWindow (endProgress=True)
	
	print "Namespaces removed:"
	print nameSpacesRemoved,"\n"	
	print(str(numRenamed) + " nodes renamed.\n")
	
	return renamedNodes

def DeleteReferenceNodes( selection=[] ):
	print('CLEAN : DeleteReferenceNodes\n')
	deletedNodes = deleteNodesOfType('reference', selection)
	
	numDeleted = len(deletedNodes)
	print(str(numDeleted) + " nodes deleted.\n")	
	
	return deletedNodes

def progressBarInit(title='Cleanup', status='Cleaning', numJobs=100):
	if numJobs == 0:
		numJobs = 1
	mc.progressWindow (title=title, st=status, progress=0, min=0, max=numJobs, isInterruptable=False)
	
def nodesOfTypeFromList(nodeList, type):
	returnList = []
		
	for node in nodeList:
		try:	# Try in case the node type doesn't exist which would cause maya ERRORs
			typeTest = mc.ls(node, st=1)[1]
			if typeTest == type:
				returnList.append(node)
		except:
			pass
				
	return returnList
	
def deleteNodesOfType(nodeType, selection=[]):
	numDeleted = 0
	deletedNodes = []
	
	print selection
	
	nodes = mc.ls(l=1, fl=1, typ=nodeType)
	if selection != [] and selection != ['']:
		nodes = nodesOfTypeFromList(selection, nodeType)	
	
	if nodes is not None and nodes != []:	
		# Progress Bar Window	
		numJobs = len(nodes)
		progressBarInit(title='Cleanup', status=('Deleting '+nodeType+' Nodes'), numJobs=numJobs)
		i=0
		
		for node in nodes:
			try:
				# Ensure it's unlocked
				mc.lockNode(node, l=0)
				print "Deleting",node
				mc.delete(node)
				numDeleted+=1
				deletedNodes.append(node)
			except:
				print "Couldn't delete",node
			i+=1
			mc.progressWindow(edit=True, progress=i)
					
		mc.progressWindow (endProgress=True)
				
	print(str(numDeleted) + ' nodes deleted.\n')
	return deletedNodes	