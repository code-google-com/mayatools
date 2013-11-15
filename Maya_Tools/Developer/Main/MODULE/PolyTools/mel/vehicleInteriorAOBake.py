#--------------------------------------------------------------------------------------------------
#
# Description.
# evoVehicleInteriorAOBake  --  Script to bake AO for vehicle interiors based on placed light 
#								probe inside the car. It will then blend the interior AO with 
#								the exterior AO based on a volume with fall of value.
# 
# Author  --  Nigel Middleman (Evolution studios)
#  
#--------------------------------------------------------------------------------------------------

import maya.cmds as mc #Maya commands
import os
import maya.mel as mel #Mel only commands
import math as math

import maya.OpenMaya as OM #API
import evoMayaLib 

#--------------------------------------------------------------------------------------------------
# cleans color sets used for baking process
def cleanUpColorSets(meshes):
	
	for mesh in meshes:
	
		colorSets = mc.polyColorSet(mesh, q=1, acs=1)

		for item in colorSets:

			if item != 'colorSet1':
			
				mc.polyColorSet(mesh, cs=item, e=1, d=1)
	
#--------------------------------------------------------------------------------------------------
#converts vert colors from srgb to linear (mental ray creates srgb during bake)
def srgbToLinear(meshSource):

	vertCount= OM.MIntArray()
	linearVertCols= OM.MColorArray()
	
	# MESH
	sourceDagPath = evoMayaLib.nameToDagPath(meshSource)	
	sourceMesh = sourceDagPath.node()
	
	# Iterate through all the vertices
	vertIterator = OM.MItMeshVertex(sourceMesh)
	
	util = OM.MScriptUtil()
	mesh = OM.MFnMesh(sourceMesh)
	
	intCol = OM.MColor() #internal AO bake
	
	while vertIterator.isDone() == 0:

		vert = vertIterator.index()
		vertIterator.getColor(intCol, 'interiorBake')
		
	
		if intCol.r < 0.05:
		
			convertedCol = OM.MColor(intCol.r,intCol.g,intCol.b,intCol.a)
			
		if intCol.r > 0.05:
		
			redCol = intCol.r
			linCol = math.pow(redCol,2.2) #linear colour value
		
			convertedCol = OM.MColor(linCol,linCol,linCol,linCol)
		
		vertCount.append(vert)
		linearVertCols.append(convertedCol)

		vertIterator.next()
	vertIterator.reset()
	
	mesh.setCurrentColorSetName('interiorBake')
	mesh.setVertexColors(linearVertCols, vertCount)
	
#--------------------------------------------------------------------------------------------------
#Gets new vert colour for base color set based on the interior lighting and using a lerp value
#from the blend color set and adds it to the original base color set
#InteriorCol * BlendColor + BaseColor*(1-BlendColor)
def setNewVertCols(meshSource):

	vertCount= OM.MIntArray()
	extVertColors= OM.MColorArray()

	# MESH
	sourceDagPath = evoMayaLib.nameToDagPath(meshSource)	
	sourceMesh = sourceDagPath.node()
	
	# Iterate through all the vertices
	vertIterator = OM.MItMeshVertex(sourceMesh)
	
	util = OM.MScriptUtil()
	mesh = OM.MFnMesh(sourceMesh)
	
	intCol = OM.MColor() #internal AO bake
	extCol = OM.MColor() #external AO bake
	blendCol = OM.MColor() #blend values
	
	tempCol = OM.MColor(1,1,1,1) #default color

	while vertIterator.isDone() == 0:
	
		vert = vertIterator.index()
		vertIterator.getColor(extCol, 'colorSet1')
		vertIterator.getColor(blendCol, 'blendColor')
		vertIterator.getColor(intCol, 'interiorBake')
		
		tempInt = OM.MColor(intCol.r, intCol.r, intCol.r, intCol.r) # sets all channels to the same colour
		tempExt = OM.MColor(extCol.a, extCol.a, extCol.a, extCol.a) # sets all channels to the same colour
		tempBlend = OM.MColor(blendCol.r, blendCol.r, blendCol.r, blendCol.r) # sets all channels to the same colour
		
		finalCol = tempInt * tempBlend + tempExt * (tempCol - tempBlend)

		newCol = OM.MColor(extCol.r, extCol.g, extCol.b, finalCol.r)
		#newCol = OM.MColor(finalCol.r, finalCol.g, finalCol.b, 1) #use this to preview the new vert colours on the rgb verts rather than the alpha
		
		vertCount.append(vert)
		extVertColors.append(newCol)

		vertIterator.next()
	vertIterator.reset()

	mesh.setCurrentColorSetName('colorSet1')
	mesh.setVertexColors(extVertColors, vertCount)

#--------------------------------------------------------------------------------------------------
#Uses new area ligh and bakes the light velues on the interior mesh parts
def bakeInteriorAO(meshes):
	
	mc.setAttr ('defaultRenderGlobals.enableDefaultLight', 0)#turns of default light

	#----light set up----
	probeCP = mc.xform('INTERIOR_LIGHTPROBE', q=1, ws=1, t=1)

	interiorProbe = mc.shadingNode ('areaLight', n='BakeLight', asLight=True)
	mc.rename( interiorProbe, 'BakeAreaLight' )
	mc.xform('BakeAreaLight', ws=1, t=probeCP)

	mc.setAttr ('BakeLight.areaLight', 1)
	mc.setAttr ('BakeLight.areaType', 2)

	mc.setAttr ('BakeAreaLight.scaleX', 0.15)
	mc.setAttr ('BakeAreaLight.scaleY', 0.15)
	mc.setAttr ('BakeAreaLight.scaleZ', 0.15)

	mc.parent( 'BakeAreaLight', 'INTERIOR_LIGHTPROBE')  

	ProbeOsX = mc.getAttr('LocalLightProbeNode1.ProbeOffsetX')
	ProbeOsY = mc.getAttr('LocalLightProbeNode1.ProbeOffsetY')
	ProbeOsZ = mc.getAttr('LocalLightProbeNode1.ProbeOffsetZ')

	mc.xform('BakeAreaLight', r=1, t=[ProbeOsX,ProbeOsY,ProbeOsZ])

	#---create vert bake set---
	mc.createNode('vertexBakeSet',  n='InteriorVertexBakeSet')

	mc.setAttr ('InteriorVertexBakeSet.colorMode', 1)

	print 'interior bake setup - Adding attrs to bake set...'

	mc.addAttr ('InteriorVertexBakeSet', ln='filterSize', sn='fs', min=-1)
	mc.setAttr ('InteriorVertexBakeSet.filterSize', 0.03)
	mc.addAttr ('InteriorVertexBakeSet', ln='filterNormalTolerance', sn='fns', min=0, max=180)
	mc.setAttr ('InteriorVertexBakeSet.filterNormalTolerance', 1.0)
	mc.setAttr ('InteriorVertexBakeSet.occlusionRays', 1024)

	#---bake meshes---
	for mesh in meshes:

		shapeNode = mc.listRelatives(mesh, s=1)
		mc.polyColorSet(mesh, cs='interiorBake', cr=1)
	
		mc.sets(shapeNode[0], fe='InteriorVertexBakeSet')
		mc.select(shapeNode[0], add=1)

	mc.select('BakeAreaLight', add=1)
	mc.setAttr ('InteriorVertexBakeSet.colorSetName', 'interiorBake', typ='string')	
	mc.convertLightmapSetup ( bakeSetOverride='InteriorVertexBakeSet', camera='persp', sh=1, vm=1, showcpv=1)

	mc.select(clear=1)
	

#--------------------------------------------------------------------------------------------------
#creates final blend color values by merging the X bake and Y bake values together
def mergeColorSets(meshes):

	for mesh in meshes:
	
		mc.polyColorSet(mesh, cs='blendColor', cr=1)
	
		shapeNode = mc.listRelatives(mesh, c=1)
		
		if shapeNode[0] == 'STEERING_WHEELShape':
		
			mc.polyColorPerVertex(shapeNode[0], r=1, g=1, b=1, a=1)
			mc.polyColorSet(mesh, cs='BakeZ', d=1)
			mc.polyColorSet(mesh, cs='BakeX', d=1)
			
		else:
	
			mc.polyBlendColor(shapeNode[0], bcn='BakeX', src='BakeZ', dst='blendColor', bfn=1, bwa=0, bwb=0, bwc=0, bwd=0)
			
			mc.polyColorSet(mesh, cs='BakeX', d=1)
			mc.polyColorSet(mesh, cs='BakeZ', d=1)
				
#--------------------------------------------------------------------------------------------------
#Transfers vert colors from temp bake planes onto interior parts
def transferVertCols(meshes):

	for mesh in meshes:

		shapeNode = mc.listRelatives(mesh, c=1)
		
		mc.transferAttributes('BakePlaneVertColZ', shapeNode[0], col=1, scs='colorSet1', tcs='BakeZ', sus='map1', tus='map1')
		mc.transferAttributes('BakePlaneVertColX', shapeNode[0], col=1, scs='colorSet1', tcs='BakeX', sus='map1', tus='map1')
		
		mc.delete(mesh, ch=1)
	
#--------------------------------------------------------------------------------------------------
#Builds list for parts to bake and parts to exclude
def getInteriorObjectsToBake():

	carInteriorParts =[] #all interior parts
	
	partsToBake = [] #all parts to bake
	partsNotToBake = [] #all parts not to bake

	objects = mel.eval('listTransforms -geometry') #lists all geometry
	interiorParts = mc.listRelatives('INTERIOR_SHELL', ad=1) #lists all interior parts

	for obj in interiorParts:
	
		type = mc.objectType(obj)

		if type == 'mesh':
		
			parent = mc.listRelatives(obj, p=1)
		
			carInteriorParts.append(parent[0])
	

	for obj in carInteriorParts:
	
		if obj.find('LOD')>=0 or obj.find('lod') >=0 or obj.find('REFLECTION') >=0:
		
			partsNotToBake.append(obj)
			
		else:
			
			partsToBake.append(obj)
	

	list1 = set(partsToBake)
	list2 = set(partsNotToBake)
	
	partsToReturn = [list1,list2]

	return partsToReturn 
		
#--------------------------------------------------------------------------------------------------
#Gets RGB value from texture and puts the colour onto the corresponding vert
def setVertColors():

	meshes = ['BakePlaneVertColZ' , 'BakePlaneVertColX']
	
	for mesh in meshes:
	
		#mc.polyColorSet(mesh, cs='colorSet1', cr=1)
		
		vertCount = (mc.polyEvaluate( mesh, v=1 )-1)
		
		for i in range(0, (vertCount+1)):
		
			uv = mc.polyEditUV (mesh + '.map[' + str(i) + ']', q=1)
			
			color = mc.colorAtPoint('BakeVert', o='RGB', u=uv[0], v=uv[1])
			
			mc.polyColorPerVertex(mesh + '.vtx[' + str(i) + ']', rgb=color)

#--------------------------------------------------------------------------------------------------
#Creates new blend texture to be used as fall off values
def bakePlanes():

	mc.surfaceSampler( mo='diffuseRGB', fn='M:/art/artTech/VehicleVertBake/gradbake', ff='tga', s='BakePlaneTexColXShape', t='BakePlaneVertColXShape', uv='map1', mh=256, mw=256, sp='tangent')
	
#--------------------------------------------------------------------------------------------------
#Creates new temp bake planes based on size of interior light probe
def setUpBakePlanes():

	mc.file('M:/art/artTech/VehicleVertBake/VehicleGradBake.mb', i=1, type='mayaBinary', options='v=0')
	probeCP = mc.xform('INTERIOR_LIGHTPROBE', q=1, ws=1, t=1)
	fadeVal = mc.getAttr('LocalLightProbeNode1.Fade')
	
	mc.scaleComponents(fadeVal,fadeVal,1,'BakePlaneTexColZ.f[2]', pivot=(0,0,0), rotation=(0,0,0))
	mc.scaleComponents(1,fadeVal,fadeVal,'BakePlaneTexColX.f[2]', pivot=(0,0,0), rotation=(0,0,0))

	scaleX = mc.getAttr('INTERIOR_LIGHTPROBE.scaleX')
	scaleY = mc.getAttr('INTERIOR_LIGHTPROBE.scaleY')
	scaleZ = mc.getAttr('INTERIOR_LIGHTPROBE.scaleZ')

	transX = (2*scaleX) + 0.5
	transZ = (2*scaleZ) + 0.5

	# bake x plane set up
	mc.xform('BakePlaneTexColX', ws=1, t=probeCP)
	mc.xform('BakePlaneVertColX', ws=1, t=probeCP)
	mc.setAttr('BakePlaneTexColX.translateX', (transX+probeCP[0]))
	mc.setAttr('BakePlaneVertColX.translateX', ((transX+probeCP[0])-0.5))
	mc.xform('BakePlaneTexColX', ws=1, s=[1, scaleY, scaleZ])
	mc.xform('BakePlaneVertColX', ws=1, s=[1, scaleY, scaleZ])
	
	# bake z plane set up
	mc.xform('BakePlaneTexColZ', ws=1, t=probeCP)
	mc.xform('BakePlaneVertColZ', ws=1, t=probeCP)
	mc.setAttr('BakePlaneTexColZ.translateZ', (transZ+probeCP[2]))
	mc.setAttr('BakePlaneVertColZ.translateZ', ((transZ+probeCP[2])-0.5))
	mc.xform('BakePlaneTexColZ', ws=1, s=[scaleX, scaleY, 1])
	mc.xform('BakePlaneVertColZ', ws=1, s=[scaleX, scaleY, 1])
	
	#sets sub divisons on plane that will have vertex colour info on that will be transfered onto car interior
	bbx = mc.xform ("BakePlaneVertColX", q=1, bb=1);
	bbz = mc.xform ("BakePlaneVertColZ", q=1, bb=1);
	
	#resolution scaler fro grid, 10=10cm/face, 20=5cm/face, 40=2.5cm/face
	res = 20

	pXh = (bbx[4]-bbx[1])
	pXw = (bbx[5]-bbx[2])
	pXhdiv = round((pXh * res), 0)
	pXwdiv = round((pXw * res),0)

	mc.setAttr ('BakePlaneVertColPlaneX.subdivisionsHeight', pXhdiv)
	mc.setAttr ('BakePlaneVertColPlaneX.subdivisionsWidth', pXwdiv)	
	
	pZh = (bbz[4]-bbz[1]);
	pZw = (bbz[3]-bbz[0]);
	pZhdiv = round((pZh * res), 0)
	pZwdiv = round((pZw * res), 0)
	
	mc.setAttr ('BakePlaneVertColPlaneZ.subdivisionsHeight', pZhdiv)
	mc.setAttr ('BakePlaneVertColPlaneZ.subdivisionsWidth', pZwdiv)

#--------------------------------------------------------------------------------------------------
#starts interior bake process
def vehicleInteriorAOBake():

	if mc.objExists('INTERIOR_LIGHTPROBE'):
	
		fadeVal = mc.getAttr('LocalLightProbeNode1.Fade')
		
		if fadeVal != 1:
		
			lightShapes =  mc.ls(lt=1, fl=1)
			
			for lightShape in lightShapes:#hides any lights in scene
			
				light = mc.listRelatives(lightShape, p=1)
				mc.setAttr((light[0] + '.visibility'), 0)
			
			setUpBakePlanes()
			bakePlanes()
			setVertColors()
			
			mc.delete('BakePlaneTexColX', 'BakePlaneTexColZ', 'BakeTexMat', 'BakeTex', 'BakeMatUV', 'BakeTexMatSG' )

			interiorParts = getInteriorObjectsToBake()

			partsToBake = interiorParts[0]
			partsNotToBake = interiorParts[1] 
		
			transferVertCols(partsToBake)
			
			mergeColorSets(partsToBake)
			
			bakeInteriorAO(partsToBake)
			
			for mesh in partsToBake:

				shapeNode = mc.listRelatives(mesh, s=1)
		
				if fadeVal != 0:# if fade is not 0 perform blend set up
				
					srgbToLinear(shapeNode[0])
					setNewVertCols(shapeNode[0])
					
				if fadeVal == 0: #if fade is 0 then only set up interior colors
				
					srgbToLinear(shapeNode[0])
			
			cleanUpColorSets(partsToBake)
			
			mc.delete('BakeLight', 'BakeAreaLight', 'InteriorVertexBakeSet', 'BakePlaneVertColX', 'BakePlaneVertColZ')	
			
		if fadeVal == 1:
		
			
			warning = mel.eval('warning("INTERIOR_LIGHTPROBE fade value is set to 1 and will use only exterior lighting values")')	
	else:
	
		warning = mel.eval('warning("There is no valid interior light probe in the scene")')
