import sys
import time #used to time code execution

import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel

#from pymel.all import *
#import pymel.core.datatypes as dt #vector datatype




#deletes all shading groups in scene, applies initial shading group, reaplies previous materials
#atempt to fix corrupt shading groups in maya
def reapplyAllMaterials():
	materialDict = getPolyListForEachMaterial()
	
	if checkMaterialDictionaryForErrors(materialDict) == 0:
		print "Error - mulitple shaders per polygon found - see script window for details"
		return

	setAllToInitialSG()
	reassignMaterialsFromDictionary(materialDict)


#sets everything in the scene to initialSG and delete all sgs in scene
def setAllToInitialSG():
	meshes = mc.ls(type="mesh")
	for mesh in meshes:
		mc.sets(mesh, e=1, forceElement="initialShadingGroup")
	
	sgs = mc.ls(type="shadingEngine")
	protectedSGs = ["initialParticleSE", "initialShadingGroup"]
	for sg in sgs:
		if sg not in protectedSGs:
			mc.delete(sg)

def reassignMaterialsFromDictionary(materialDict):
	for key in materialDict:
		print ("Reassigning material: " + key)
		
		#add a new shading group
		sg = mc.sets(renderable=1, noSurfaceShader=1, empty=1, name=(key+"SG"))
		mc.connectAttr( (key+".outColor"), (sg+".surfaceShader"), force=1);
		
		if len(materialDict[key]) == 0:
			print ("No polygons assigned to shader: " + key)
		else:
			mc.sets(list(materialDict[key]), e=1, forceElement=sg)
		
		#slow due to selections	
		#mc.select(list(materialDict[key]), r=1)
		#mc.hyperShade(assign=key) #automatically creates new sgs for us


#returns a dictionary of each material, with a list of polys using it
def getPolyListForEachMaterial():
	materialDict = {}
	materials = mc.ls(materials=1)
	for material in materials:
		print("Storing polygon assignments for: " + material)
		sgs = getSGsFromMaterial(material)
		polys = []
		for sg in sgs:
			sgPolys = mc.sets(sg, q=1)
			if sgPolys != None:
				sgPolys2 = []
				for i in sgPolys:
					if ".f[" in i:
						sgPolys2.append(i)
					else:
						sgPolys2 = sgPolys2 + mc.polyListComponentConversion(i,toFace=1)
				polys = polys + ( mc.ls(sgPolys2, flatten=1) )
				#print "polys = "; print polys
		materialDict[material] = set(polys)
	return materialDict


#checks dictionary for overlapping polys. Returns 0 if errors found
def checkMaterialDictionaryForErrors(materialDict):
	returnValue = 1
	dictKeys = materialDict.keys()
	for i in range(0, len(dictKeys)):
		for j in range(i+1, len(dictKeys)):
			multipleShadersPerPoly = materialDict[dictKeys[i]].intersection(materialDict[dictKeys[j]])
			if len(multipleShadersPerPoly) > 0:
				print ("Multiple shaders per polgon found (" + materialDict[dictKeys[i]] + " and " + materialDict[dictKeys[j]] + ") on:")
				print multipleShadersPerPoly
				returnValue = 0
	print "Dictionary checked for errors"
	return returnValue




#returns a list of shading groups for the given material
def getSGsFromMaterial(material):
	SGs = []
	if (material == ""): return SGs
	
	outColor = "outColor"
	if outColor not in mc.listAttr(material):
		outColor = "oc"
		if outColor not in mc.listAttr(material):
			print "no .oc or .outcolor found!"
			return SGs
	outColor = "." + outColor
	if mc.connectionInfo((material + outColor), isSource=1 ):
		dests = mc.connectionInfo((material + outColor), destinationFromSource=1 )
		for dest in dests:
			if mc.nodeType(dest) == "shadingEngine":
				SGs.append(rootNode(dest))

	if len(SGs) == 0 and material == "lambert1": 
		SGs[0] = "initialShadingGroup";

	return SGs

# Description: Strips the dot-suffix of the specified string.
def rootNode(object):
	tokens = object.split(".")
	return tokens[0]
