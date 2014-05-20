#Author: Tran Quoc Trung GlassEgg Digital Media
#Date: SEP-11-2012
#------------------------- Baking AO to vertex -----------------------------------------

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
        
class bakingNormalUI():
    def __init__(self, winName = "winAO"):
        self.winTitle = "Baking AO Tools"
        self.winName = winName
        self.valueAverage = 0

    def create(self):
        #selectedVertex = cmds.scriptJob()
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

        cmds.window(self.winName, title=self.winTitle, rtf = True)
        #----------------
        cmds.frameLayout( label = 'Baking AO tools', cll = True)
            #--------------
        cmds.rowLayout(nc = 2)
        self.btnAOVertex = cmds.button( label='Baking AO on vertex', c=partial(self.run, False) )
        self.btnAOVertexFace = cmds.button( label='Baking AO on vertexFace', c=partial(self.run, True) )
        cmds.setParent('..')
            #--------------
        cmds.setParent('..')
        #----------------
        #----------------
        cmds.frameLayout( label = 'Adjust vertex color tools', cll = True)
            #--------------
        self.rowLayout(nc = 3)
        self.btnRedChannel = cmds.button(label = 'Red', bgc = [255,0,0] )
        self.btnGreenChannel = cmds.button(label = 'Green', bgc = [0,255,0])
        self.btnBlueChannel = cmds.button(label = 'Blue', bgc = [0,0,255])
        cmds.setParent('..')
            #--------------
            #--------------
        cmds.rowLayout(nc = 2 )
        self.btnCopyVertexColorAverage = cmds.button(label = 'Copy Average Color' , c = partial(self.copyVertexColorAverage,'' ))
        self.btnPasteVertexColorAverage = cmds.button(label = 'Paste Buffer Color' , c = partial(self.copyVertexColorAverage, ''))
        cmds.setParent('..')
            #--------------
            #--------------
        cmds.rowLayout(nc = 2)
        cmds.text(label = 'Adjust color:')
        self.sldColor = cmds.floatSlider(min = 0, max = 1, step = 0.01, hr = True)
        cmds.setParent('..')
            #--------------
        cmds.setParent('..')
        #--------------
        cmds.showWindow( self.winName )
        cmds.window(self.winName, edit=True, widthHeight=[250,150])
        
    def createSurfaceNodeMentalRay(self, node):
        surfaceNode = cmds.shadingNode('surfaceShader', asShader = 1)# create surfaceShader node
        ambientNode = cmds.shadingNode('mib_amb_occlusion', asTexture = 1)# create ambient texture node
        cmds.setAttr(ambientNode + '.samples', 1024) # setup quality for AO
        cmds.connectAttr(ambientNode + '.outValue',surfaceNode + '.outColor')# connect mib_ambient_occ to surfaceShader
        shadingGroupAO = cmds.sets(renderable = True, noSurfaceShader = True, empty = True, n = 'shadingGroupAO')
        try:
            cmds.connectAttr(surfaceNode + '.outColor', 'shadingGroupAO.surfaceShader')
        except:
            print 'connection is ready'
        cmds.sets(node, edit = True, forceElement = 'shadingGroupAO')
        return (surfaceNode, ambientNode, shadingGroupAO)
    
    def bakingOcclusion(self,node):
        (surfaceNode, ambientNode, shadingGroupAO) = createSurfaceNodeMentalRay(node)
        # setup vertex color for node
        cmds.polyColorPerVertex(node, r = 0, g = 0, b = 0, a = 1, rel = True, cdo = True)
        # create vertex colorbakeset to bake AO from Mentalray
        if (cmds.objExists('vertexBakeSetAO')):
            cmds.delete('vertexBakeSetAO')
        cmds.createNode('vertexBakeSet', n = 'vertexBakeSetAO')
        cmds.setAttr('vertexBakeSetAO' + '.colorMode',0) # set color mode to bake Light and Color
        cmds.addAttr('vertexBakeSetAO', ln = 'filterSize', min = -1)
        cmds.setAttr('vertexBakeSetAO.filterSize', 0.001)
        cmds.addAttr('vertexBakeSetAO', ln = 'filterNormalTolerance', min = 0, max = 180)
        cmds.setAttr('vertexBakeSetAO.filterNormalTolerance', 0.001)
        cmds.select(node)
        cmds.convertLightmapSetup(shadingGroupAO, node, camera = 'persp', sh = True, bo = 'vertexBakeSetAO', vm = True)
        cmds.delete(surfaceNode)
        cmds.delete(ambientNode)
        cmds.delete('vertexBakeSetAO')
    
    def copyVertexAlpha(self,source, target, countNormal = True):
        cmds.polyColorPerVertex(source, r = 0, b = 0, g = 0, a = 0, rel = True, cdo = True)
        cmds.polyColorPerVertex(target, r = 0, b = 0, g = 0, a = 0, rel = True, cdo = True)
        numVertSource = cmds.polyEvaluate(source, v = True)
        numVertTarget = cmds.polyEvaluate(target, v = True)
        out = (numVertSource == numVertTarget) or False
        if out:
            if countNormal: # use to calculate normal and then copy to vertexFace
                selectList = cmds.select(source + '.vtx[0:' + str(numVertSource) + ']')
                vertexFacesSource = cmds.polyListComponentConversion(tvf = True)
                cmds.select(vertexFacesSource)
                vertexFacesSource = cmds.ls(sl = True, fl = True)
                for iSource in vertexFacesSource:
                    value = cmds.polyColorPerVertex(iSource , q = 1, r = 1)# get Vertex Color Red channel from Source
                    iTarget = iSource.replace(source, target)
                    cmds.polyColorPerVertex(iTarget, a = value[0]) # assign to Color Alpha to target
            else: # use to copy to vertex
                for i in range(numVertSource):
                    value = cmds.polyColorPerVertex(source + '.vtx[' + str(i) + ']' , q = 1, r = 1)[0]# get Vertex Color Red channel from Source
                    cmds.polyColorPerVertex(target + '.vtx[' + str(i) + ']', a = value) # assign to Color Alpha to target
        else:
            print 'Please using transfering method instead!'
        
    def run(self, para, a = 'Nothing'):
        targetNode = cmds.ls(sl = True)[0]
        sourceNode = cmds.duplicate(n = targetNode + '_bakingAONode')[0]
        cmds.setAttr(targetNode + '.visibility', False)
        bakingOcclusion(sourceNode)
        cmds.setAttr(targetNode + '.visibility', True)
        copyVertexAlpha(sourceNode, targetNode, para)
        cmds.delete(sourceNode)
        
    def copyVertexColorAverage(self, channel = 'a'): # copy alpha channel
        isVertexSelected = cmds.selectType(q = True, v = True)
        totalValue = 0
        if isVertexSelected:
            selectedVertexes = cmds.ls(sl = True, fl = True)
            for vertex in selectedVertexes:
                totalValue += cmds.polyColorPerVertex(vertex, q= True, channel = True)
        self.valueAverage = totalValue/len(selectedVertexes)
        
    def pasteBufferColor(self, channel):
        isVertexSelected = cmds.selectType(q = True, v = True)
        if isVertexSelected:
            selectedVertexes = cmds.ls(sl = True, fl = True)
            cmds.polyColorPerVertex(selectedVertexes, channel = self.valueAverage)
        
inst = bakingNormalUI()
inst.create()