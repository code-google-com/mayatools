import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaRender as OpenMayaRender
import maya.cmds as cmds
import maya.mel as mel
import math

# initialize plugin ID
kPluginNodeName = "rigLocomotiveMasterNode" # double quoted mark
kPluginNodeID = OpenMaya.MTypeId(0x81199)

glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT =glRenderer.glFunctionTable()

# Default Parameters
kCylRadius = 1.0
kConRadius = 2.5
kCylLength = 15
kConLength = 6
kSquLength= 15
kThickness = 5
kBevelRadius = 1
kSegment = 20

def getLengthOfCurvePath(inputNode):
    curveInfo = cmds.arclen(inputNode,ch = True)
    return cmds.getAttr(curveInfo + '.arcLength')

class rigLocomotiveMasterNode(OpenMayaMPx.MPxLocatorNode):
    #aLength = 0.0
    #aCargos = list()
    childNodes = list()
    
    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)
            
    def draw(self, view, path, style , status):
        if status == OpenMayaUI.M3dView.kLead:
        	glFT.glColor4f(0, 0, 1, 0.5)
        if status == OpenMayaUI.M3dView.kActive:
            glFT.glColor4f(1, 0, 0, 0.4)
        if status == OpenMayaUI.M3dView.kDormant:
            glFT.glColor4f(0, 1, 0, 0.5)	
        # draw arrow head    
            # draw cap off
        glFT.glEnable(OpenMayaRender.MGL_BLEND)
        #glFT.glColor4f(1,0,0,0.75)
        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        for i in range(kSegment):
            rad = (i * 360/kSegment * 2 * math.pi)/360
            glFT.glVertex3f( kConRadius * math.cos(rad), kConRadius * math.sin(rad), kCylLength/2)
        glFT.glEnd()
            # draw body
        for i in range(kSegment):
            glFT.glBegin(OpenMayaRender.MGL_TRIANGLES)
            glFT.glVertex3f(kConRadius * math.cos((i * 360/kSegment * 2 * math.pi)/360), kConRadius * math.sin((i * 360/kSegment * 2 * math.pi)/360), kCylLength/2)
            glFT.glVertex3f(kConRadius * math.cos(((i+1) * 360/kSegment * 2 * math.pi)/360), kConRadius * math.sin(((i+1) * 360/kSegment * 2 * math.pi)/360), kCylLength/2)
            glFT.glVertex3f(0, 0, kCylLength/2 + kConLength)
            glFT.glEnd()
        # draw arrow body
            # draw cap off
        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        for i in range(kSegment):
            rad = (i * 360/kSegment * 2 * math.pi)/360
            glFT.glVertex3f( kCylRadius * math.cos(rad), kCylRadius * math.sin(rad), -kCylLength/2)
        glFT.glEnd()
            # draw cylinder body
        for i in range(kSegment):
            glFT.glBegin(OpenMayaRender.MGL_QUADS)
            glFT.glVertex3f(kCylRadius * math.cos((i * 360/kSegment * 2 * math.pi)/360), kCylRadius * math.sin((i * 360/kSegment * 2 * math.pi)/360), -kCylLength/2)
            glFT.glVertex3f(kCylRadius * math.cos(((i+1) * 360/kSegment * 2 * math.pi)/360), kCylRadius * math.sin(((i+1) * 360/kSegment * 2 * math.pi)/360), -kCylLength/2)
            glFT.glVertex3f(kCylRadius * math.cos(((i+1) * 360/kSegment * 2 * math.pi)/360), kCylRadius * math.sin(((i+1) * 360/kSegment * 2 * math.pi)/360), kCylLength/2)
            glFT.glVertex3f(kCylRadius * math.cos((i * 360/kSegment * 2 * math.pi)/360), kCylRadius * math.sin((i * 360/kSegment * 2 * math.pi)/360), kCylLength/2)
            glFT.glEnd()
        
        glFT.glDisable(OpenMayaRender.MGL_BLEND)
        
        # draw rounded rectangle
        #glFT.beginGL()
        
        #glFT.endGL()
        
        
    def compute( self, plug, data ):
        return OpenMaya.kUnknownParameter
            
    def isAttachable(cargoShip):
        l = self._cargoShipsLength + cargoShip.length
        if l > self._curveLength:
            return False
        else:
            return True
        
    def attachToCurvePath(newCurvePath):
        pass
        
    def attachCargo(cargoShip):
        result = selt.isAttachable(cargoShip)
        if result:
            self._cargoShips.append(cargoShip.name)
            motionName = 'motionPath_' + cargoShip.name
            cmds.pathAnimation(cargoShip.bbox, c = self._curve, startU = 0, name = motionName )
            self.updateParameters()
        else:
            print 'Cannot append more cargo. Please lengthen the curve or find another proper curve!'
     
    def updateParameters(self):
        for index in range(len(self._cargoShips)):
            if index == 0 or index == len(self._cargoShips) - 1:
                pass

    def compute(self, plug, datahandle):						
		return OpenMaya.kUnknownParameter

                
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(rigLocomotiveMasterNode())
    
    
def nodeInitializer():
    return OpenMaya.MStatus.kSuccess
    #pass
    
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
                

