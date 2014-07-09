import maya.cmds as cmds
import maya.mel as mel

def createSurfaceNodeMentalRay(node):
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
    
def bakingOcclusion(node):
    (surfaceNode, ambientNode, shadingGroupAO) = createSurfaceNodeMentalRay(node)
    # setup vertex color for node
    cmds.polyColorPerVertex(node, r = 0, g = 0, b = 0, a = 1, rel = True, cdo = True)
    # create vertex colorbakeset to bake AO from Mentalray
    if (cmds.objExists('vertexBakeSetAO')):
        cmds.delete('vertexBakeSetAO')
    cmds.createNode('vertexBakeSet', n = 'vertexBakeSetAO')
    cmds.setAttr('vertexBakeSetAO' + '.colorMode',0) # set color mode to bake Occlusion
    cmds.addAttr('vertexBakeSetAO', ln = 'filterSize', min = -1)
    cmds.setAttr('vertexBakeSetAO.filterSize', 0.001)
    cmds.select(node)
    #cmds.convertLightmapSetup(vm = True, bo = 'vertexBakeSetAO')
    cmds.convertLightmapSetup(shadingGroupAO, node, camera = 'persp', sh = True, bo = 'vertexBakeSetAO', vm = True)
    cmds.delete(surfaceNode)
    cmds.delete(ambientNode)
    
def copyVertexAlpha(source, target):
    cmds.polyColorPerVertex(source, r = 0, b = 0, g = 0, a = 0, rel = True, cdo = True)
    numVertSource = cmds.polyEvaluate(source, v = True)
    numVertTarget = cmds.polyEvaluate(target, v = True)
    out = (numVertSource == numVertTarget) or False
    if out:
        for i in range(numVertSource):
            #print source + '.vtx[' + str(i) + ']'
            value = cmds.polyColorPerVertex(source + '.vtx[' + str(i) + ']' , q = 1, r = 1)[0]# get Vertex Color Red channel from Source
            cmds.polyColorPerVertex(target + '.vtx[' + str(i) + ']', a = value) # assign to Color Alpha to target
    else:
        print 'Please using transfering method instead!'
            
def run():
    targetNode = cmds.ls(sl = True)[0]
    sourceNode = cmds.duplicate(n = targetNode + '_bakingAONode')[0]
    cmds.setAttr(targetNode + '.visibility', False)
    #(shader, texture) = createSurfaceNodeMentalRay(sourceNode)
    bakingOcclusion(sourceNode)
    cmds.setAttr(targetNode + '.visibility', True)
    copyVertexAlpha(sourceNode, targetNode)
    cmds.delete(sourceNode)
    
    
run()
