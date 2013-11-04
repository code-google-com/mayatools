
# script hacked by AndyB to work as uv auto ratio pro replacement for Maya 2013.

#  varun.bondwal@yahoo.com. Please report any bugs or suggestions.
#  v1.0 . Modified script to work in Maya 2011


import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import string
import math


#used to set the GUI ratio, also for ratio measurement when setting
def get_sel_faces_UV_ratio(set_active):

	totalUVArea = 0
	totalFaceArea =0
	orig_sele=cmds.ls(sl=True, fl=True)
	areaParam = om.MScriptUtil()
	areaParam.createFromDouble(0.0)
	areaPtr = areaParam.asDoublePtr() 

	mel.eval("PolySelectConvert 1")      
	sele=om.MSelectionList()
	om.MGlobal.getActiveSelectionList(sele)
	it=om.MItSelectionList(sele)
	while not it.isDone():
		dagPath=om.MDagPath()
		component=om.MObject()
		it.getDagPath(dagPath,component)
		fn=om.MFnDependencyNode(dagPath.node())
		if not component.isNull():
			if component.apiType()==om.MFn.kMeshPolygonComponent:
				itPoly=om.MItMeshPolygon(dagPath,component)
				while not itPoly.isDone():

					itPoly.getUVArea(areaPtr)
					area = om.MScriptUtil(areaPtr).asDouble()
					totalUVArea += area

					itPoly.getArea(areaPtr,om.MSpace.kWorld)
					area = om.MScriptUtil(areaPtr).asDouble()
					totalFaceArea += area

					itPoly.next()
		it.next()
	
	#print " totalUVArea: "
	#print totalUVArea
	#print " totalFaceArea: "
	#print totalFaceArea
	
	#catch divide by zero errors
	UV_ratio = 0.0;
	if totalFaceArea != 0:
		UV_ratio=totalUVArea/totalFaceArea
	
	if set_active==1:
		active_ratio=UV_ratio
		print "UV area:"
		print totalUVArea
		print "total face area:"
		print totalFaceArea
		print "UV Ratio:"
		UV_ratio_inverted = 0.0;
		if UV_ratio != 0:
			UV_ratio_inverted = 1.0/UV_ratio
		print UV_ratio_inverted
		#cmds.floatField("boltUVRatioField", edit=True, v=(UV_ratio_inverted) ) ;
		for i in range(0,len(orig_sele)):
			mel.eval("select -add " + orig_sele[i])
	return UV_ratio


#set scale of selected UV shells
def collect_shells_and_set_shells_UV_ratio(ratio):
	
	active_ratio = 1.0 / ratio#cmds.floatField("boltUVRatioField", q=True, v=True)
	
	orig_sele=cmds.ls(sl=True, fl=True)

	mel.eval("ConvertSelectionToUVs")
	main_list=cmds.ls(sl=True,fl=True)
	UV=cmds.ls(sl=True, fl=True)
	new_list=[" "]
	
	orig_len=len(main_list)
	
	while (len(main_list)>0):
		
		print "fixing uv shell:"
		print main_list[0]
		
		mel.eval("select "+ main_list[0])
		mel.eval("SelectUVShell")
		prog=((1.000*orig_len-1.000*len(main_list))/(1.000*orig_len))*20

		current_ratio=get_sel_faces_UV_ratio(0)
		if current_ratio==0:
			current_ratio=1
		scale_factor=active_ratio/current_ratio
		scale_factor=math.sqrt(scale_factor)
		mel.eval("PolySelectConvert 4;")   #to UVs
		UV_bounds=cmds.polyEvaluate(bc2=True)
		u_pivot = (UV_bounds[0][0]+UV_bounds[0][1])/2
		v_pivot = (UV_bounds[1][0]+UV_bounds[1][1])/2

		cmds.polyEditUV(pu=u_pivot, pv=v_pivot, su=scale_factor, sv=scale_factor)

		temp_shell=cmds.ls(sl=True,fl=True)
		for j in range(0,len(temp_shell)):
			if temp_shell[j] in main_list:
				main_list.remove(temp_shell[j])
		
	new_list.remove(" ")
	cmds.select(cl=True)
	for i in range(0,len(orig_sele)):
		mel.eval("select -add " + orig_sele[i])

	return new_list
	





