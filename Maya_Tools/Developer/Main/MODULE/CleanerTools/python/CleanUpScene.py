description = 'Clean up redundant nodes in scene.'
name = 'CleanUpScene'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py

def execute():
    print '--------------- CLEAN UP SCENE-------------------------'
    
    print '--------------- Optimize scene ------------------------'
    mel.eval('OptimizeScene;')
    
    print '--------------- Convert Instance mesh to object-------------------'
    shapeNodes = cmds.ls(type = 'mesh')
    for shape in shapeNodes:
        parents = cmds.listRelatives(shape, allParents = True)
        if len(parents) > 1:
            print shape + ' is instances of mesh'
            py.select(parents)
            mel.eval('ConvertInstanceToObject;')

    print '--------------- Clean up dead shape node-----------------'
    shapeNodes = py.ls(shapes = True, long = True)
    liveShapes = list()
    #print shapeNodes
    sgs = py.ls(typ = 'shadingEngine')
    for shape in shapeNodes:
        for sg in sgs:
            member = [mem.split('.f')[0] for mem in sg.members()]
            if shape in member:
                liveShapes.append(shape)# = [shape for shape in shapeNodes for sg in sgs if py.sets(shape, im = sg)]
    deadShapes = [shape for shape in shapeNodes if shape not in liveShapes]
    for node in deadShapes:
        if node.nodeType() == 'camera':
            deadShapes.remove(node)
    for node in deadShapes:
        if len(node.listConnections(c = True)):
            deadShapes.remove(node)
    for dead in deadShapes:
        try:
            cmds.delete(dead)
            print '-- delete dead shape: ' + dead
        except:
            pass
        
    print '--------------- Export Selected for cleaning up-----------------'
    mel.eval('SelectAll;')
    namefile= cmds.file(q= True, sn = True)
    cmds.file(namefile, f= True, es = True, type = 'mayaBinary')
    cmds.file(namefile, f= True, o = True)
    cmds.viewFit(all = True)

    
    