description = 'Clean up dead shapes.'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


def execute():
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
    
    