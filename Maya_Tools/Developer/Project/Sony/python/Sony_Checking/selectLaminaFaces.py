description = 'Select lamina face.'
name = 'selectLaminaFaces'
import maya.cmds as cmds
import maya.mel as mel

def execute():
    edges = cmds.polyInfo(laminaFaces  = True)
    cmds.select(edges)
    
    
