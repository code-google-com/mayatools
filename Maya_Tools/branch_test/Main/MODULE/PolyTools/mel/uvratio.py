
# script hacked by AndyB to work as uv auto ratio pro replacement for Maya 2013.

#  varun.bondwal@yahoo.com. Please report any bugs or suggestions.
#  v1.0 . Modified script to work in Maya 2011


import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import string
import math


#used to set the GUI ratio, also for ratio measurement when setting
#set_active 0 returns UV ratio, 1 sets gui UV ratio, 2 special mode, returns correct default UV ratio of 25 for small shells. (<2x2cm)
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
	
	if set_active==2 and totalFaceArea<0.0004 :
		return 0.04 # if its a small face and mode 2 is specified, return the default correct UV ratio of 1/25
		
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
		cmds.floatField("boltUVRatioField", edit=True, v=(UV_ratio_inverted) ) ;
		for i in range(0,len(orig_sele)):
			mel.eval("select -add " + orig_sele[i])
	return UV_ratio


#set scale of selected UV shells
#mode 1 double checks the result, and moves shell closer to origin if necessary
def collect_shells_and_set_shells_UV_ratio(mode):
	
	active_ratio = 1.0 / cmds.floatField("boltUVRatioField", q=True, v=True)
	
	print "target ratio:"
	print active_ratio
	
	orig_sele=cmds.ls(sl=True, fl=True)

	mel.eval("ConvertSelectionToUVs")
	main_list=cmds.ls(sl=True,fl=True)
	UV=cmds.ls(sl=True, fl=True)
	new_list=[" "]
	
	orig_len=len(main_list)
	
	
	whileCount = len(main_list)
	while (len(main_list)>0):
		
		print "fixing uv shell:"
		print main_list[0]
		
		mel.eval("select "+ main_list[0])
		mel.eval("SelectUVShell")
		prog=((1.000*orig_len-1.000*len(main_list))/(1.000*orig_len))*20

		current_ratio=get_sel_faces_UV_ratio(0)
		
		print "current ratio:"
		print current_ratio
		
		if current_ratio==0:
			current_ratio=1
		scale_factor=active_ratio/current_ratio
		scale_factor=math.sqrt(scale_factor)
		mel.eval("PolySelectConvert 4;")   #to UVs
		UV_bounds=cmds.polyEvaluate(bc2=True)
		u_pivot = (UV_bounds[0][0]+UV_bounds[0][1])/2
		v_pivot = (UV_bounds[1][0]+UV_bounds[1][1])/2
		
		print "scale factor:"
		print scale_factor
		
		cmds.polyEditUV(pu=u_pivot, pv=v_pivot, su=scale_factor, sv=scale_factor)
		
		temp_shell=cmds.ls(sl=True,fl=True)
		for j in range(0,len(temp_shell)):
			if temp_shell[j] in main_list:
				main_list.remove(temp_shell[j])
		
		cmds.select(temp_shell)
		current_ratio=get_sel_faces_UV_ratio(0)
		print "fixed ratio:"
		print current_ratio
		
		if mode == 1 and current_ratio != 0:
			if abs((1/current_ratio)-(1/active_ratio)) >= 5: #large tolerance allowed
				print ("Could not scale this shell within tolerance - moving nearer to origin and rescaling:")
				
				cmds.polyEditUV(relative=1, u=(-1*u_pivot), v=((-1*v_pivot)-1) );
				
				scale_factor=active_ratio/current_ratio
				scale_factor=math.sqrt(scale_factor)
				mel.eval("PolySelectConvert 4;")   #to UVs
				UV_bounds=cmds.polyEvaluate(bc2=True)
				u_pivot = (UV_bounds[0][0]+UV_bounds[0][1])/2
				v_pivot = (UV_bounds[1][0]+UV_bounds[1][1])/2
				cmds.polyEditUV(pu=u_pivot, pv=v_pivot, su=scale_factor, sv=scale_factor)
				
				current_ratio=get_sel_faces_UV_ratio(0)
				print "fixed ratio after moving shell closer to origin:"
				print current_ratio
				
		whileCount-=1
		if whileCount < 0:
			print "While loop error!"
			break
		
	new_list.remove(" ")
	cmds.select(cl=True)
	for i in range(0,len(orig_sele)):
		mel.eval("select -add " + orig_sele[i])

	return new_list



