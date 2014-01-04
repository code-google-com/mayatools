description = 'Correct all node name.'
name = 'CorrectNodeName'
tooltip = 'Correct node name:\n\t Correct shape node.\n\t Correct shadingGroup node.\n\t Correct texture name.'

import maya.cmds as cmds
import pymel.core as py

def execute():
    print '--------------- RENAME SHAPENODE-------------------------'
    meshes = cmds.ls(type= 'mesh')
    for mesh in meshes:
        transformNode = cmds.listRelatives(mesh, parent = True, type = 'transform')[0]
        if mesh != transformNode + 'Shape':
            cmds.rename(mesh, transformNode + 'Shape')
            print '-- Renamed shape node on mesh:' + mesh
            
    print '--------------- RENAME SHADINGNODE-------------------------'
    shaders = py.ls(materials = True)
    for s in shaders:
        try:
            sg = str(s.listConnections(s= True, t= 'shadingEngine')[0])
            py.rename(sg, s+'SG')
            print '-- Renamed shading node: ' + sg + ' to: ' + s + 'SG'
        except:
            pass
    
    print '--------------- RENAME TEXTURENODE-------------------------' 
    textures = py.ls(tex = True)
    for t in textures:
        try:
            name = t.getAttr('fileTextureName').split('/')[-1].split('.')[0]
            py.rename(t, name)   
            print '-- Renamed texture node: ' + t + ' to: ' + name
        except:
            pass
    