description = 'Select lamina face.'
tooltip = ''

import maya.cmds as cmds
import maya.mel as mel


def executeAll():
    transformNodes = cmds.ls(type = 'transform') # neu khong chon object nao het tool se kiem tra tat ca object
    print '-------------------------------------CHECK LAMINA FACES ON ENTIRE SCENE----------------------------------\n'
    for node in transformNodes:
        executeSelected(node)
    print '-------------------------------------CHECK LAMINA FACES COMPLETE----------------------------------\n'
       
def executeSelected(transformNode):
    childMeshes = cmds.listRelatives(transformNode, fullPath = True, c = True, type = 'mesh')
    meshes = cmds.ls(childMeshes,long = True, noIntermediate = True)
    try:
        mesh = meshes[0]
    except IndexError:
        #print transformNode + ' khong phai geometry.'
        return 0
    if mel.eval('attributeExists "nonManifoldException" {var}'.format(var = mesh)) == 0:
        edges = cmds.polyInfo(transformNode, laminaFaces = True)
        if edges == None:
            #print transformNode + ' khong co non manifold edges.'
            return 0
            #print transformNode + ' co ' + str(len(edges)) + ' non manifold edges. Can duoc fix\n'
        else:
            print transformNode + ' co ' + str(len(edges)) + ' lamina faces. Can duoc fix\n\n'
            return edges
            #laminaFaces = cmds.polyInfo(laminaFaces  = True)
            #print transformNode + ' co ' + str(len(laminaFaces)) + ' laminda faces. Can duoc fix\n'

def execute():
    if len(cmds.ls(sl = True)) == 0: # khong chon object nao het
        executeAll()
    else:
        errorItems = []
        print '-------------------------------------CHECK LAMINA FACES ON ENTIRE SCENE----------------------------------\n'
        for node in cmds.ls(sl = True):
            result = executeSelected(node)
            if result != 0:
                errorItems += result
        if len(errorItems) != 0:
            cmds.select(errorItems) 
        print '-------------------------------------CHECK LAMINA FACES COMPLETE----------------------------------\n'
            
        

    