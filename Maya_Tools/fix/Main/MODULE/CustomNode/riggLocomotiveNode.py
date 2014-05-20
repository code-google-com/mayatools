import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.mel as mel
import math

kPluginNodeName = "rigLocomotiveNode"
kPluginNodeID = OpenMaya.MTypeId(0x12899)

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT =glRenderer.glFunctionTable()

kLength = 10
kWidth = 10
kHeight = 10

class rigLocomotiveNode(OpenMayaMPx.MLocatorNode):
	aLength = OpenMaya.MObject()
	
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
	def draw(self, view, path, style, status):
		if status == OpenMayaUI.M3dView.kLead:
			glFT.glColor4f()
		#draw
		glFT.glEnable(OpenMayaRender.MGL_BLEND)
		for i in range(4):
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)
			glFT.glVertex3f(0, 0,kHeight/2)
			glFT.glVertex3f(kLength/2 * math.cos(i * math.PI), 0,0)
			glFT.glVertex3f(0, 0,-kHeight/2)
			glFT.glVertex3f(0, kWidth/2 * math.cos(i * math.PI), 0)
			glFT.glEnd()
		glFT.glDisable(OpenMayaRender.MGL_BLEND)
		
	def compute(self, data, plug):
		return OpenMaya.kUnknownParameter
		
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(rigLocomotiveNode())
    
    
def nodeInitializer():
    #return OpenMaya.MStatus.kSuccess
    pass
    
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    #plugin.registerNode(kPluginNodeName, kPluginNodeID, nodeCreator,nodeInitializer,OpenMayaMPx.MPxNode.kLocatorNode)
    try:
        plugin.registerNode(kPluginNodeName, kPluginNodeID, nodeCreator,nodeInitializer,OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        sys.stderr.write('Failed to initilize plugin')
    
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(kPluginNodeID)
    except:
        sys.stderr.write('Failed to uninitialize plugin')