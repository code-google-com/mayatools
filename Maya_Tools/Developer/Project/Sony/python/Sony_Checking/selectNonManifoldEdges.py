description = 'Select non_manifold face.'
name = 'selectNonManifoldEdges'
import maya.cmds as cmds
import maya.mel as mel

def execute():
    edges = cmds.polyInfo(nonManifoldEdges = True)
    cmds.select(edges)
    
    
