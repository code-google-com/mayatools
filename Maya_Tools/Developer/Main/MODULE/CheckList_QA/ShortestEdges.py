import maya.OpenMaya as OpenMaya
import maya.mel as mel
import maya.cmds as cmds
import re

__name__ = 'Shortest Edges'

def getShortesEdgesOnMesh(lengthSample, mesh):
    cmds.select(mesh)
    cmds.polySelectConstraint(mode = 3, type = 0x8000, l = True, lb = [0, lengthSample])
    shortestEdges = cmds.ls(sl = True, fl = True)
    cmds.polySelectConstraint(l = False)
    cmds.polySelectConstraint(mode = 0)
    cmds.select(cl = True)
    return shortestEdges

def run(mesh):
    numShortestEdges = 0
    if re.search(r'(.*)_LOD6', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.1, mesh)
    elif re.search(r'(.*)_LOD5', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.05, mesh)
    elif re.search(r'(.*)_LOD4', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.025, mesh)
    elif re.search(r'(.*)_LOD3', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.012, mesh)
    elif re.search(r'(.*)_LOD2', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.006, mesh)
    elif re.search(r'(.*)_LOD1', mesh, re.I):
        numShortestEdges = getShortesEdgesOnMesh(0.003, mesh)
    else:
        numShortestEdges = getShortesEdgesOnMesh(0.001, mesh)
    
    result = (len(numShortestEdges) == 0) or False
    if result:
        message = 'No shortest was found. Keep moving.'
    else:
        message = 'Found ' + str(len(numShortestEdges)) + 'some shortest edges on ' + mesh + ' . That may cause bad performance in game. Need to be fixed but not compulsory'
    return (result, message, numShortestEdges)

def fix():
    pass