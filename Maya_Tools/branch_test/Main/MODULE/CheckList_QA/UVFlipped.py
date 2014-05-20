import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import pymel.core.datatypes as dt

__name__ = 'Flipped UV'

def run(mesh):
    message = ''
    if cmds.nodeType(mesh) == 'transform':
        shapeNode = cmds.pickWalk(mesh,d = 'down')[0]
        if cmds.nodeType(shapeNode) == 'mesh':
            flippedUVList = []
            cmds.select(mesh)
            faces = cmds.ls((cmds.polyListComponentConversion((cmds.ls(fl=1,sl=1)), tf=1)), fl=1)
            for face in faces:
                uvs = []
                vtxFaces = cmds.ls(cmds.polyListComponentConversion(face,toVertexFace=True),flatten=True)
                try:
                    for vtxFace in vtxFaces:
                        uv = cmds.polyListComponentConversion(vtxFace,fromVertexFace=True,toUV=True)
                        uvs.append(uv[0])
                except IndexError:
                        continue
                #get edge vectors and cross them to get the uv face normal
                uvAPos = cmds.polyEditUV(uvs[0], q=1)
                uvBPos = cmds.polyEditUV(uvs[1], q=1)
                uvCPos = cmds.polyEditUV(uvs[2], q=1)
                uvAB = dt.Vector([uvBPos[0]-uvAPos[0], uvBPos[1]-uvAPos[1]])
                uvBC = dt.Vector([uvCPos[0]-uvBPos[0], uvCPos[1]-uvBPos[1]])
                crossproduct = uvAB.cross(uvBC) 
                if crossproduct.z < 0:
                    flippedUVList.append(face)
            result = (len(flippedUVList) == 0) or False
            if result:
                message = 'No flippedUV face was found on ' + mesh
            else:
                message = 'There are ' + str(len(flippedUVList)) + '  flipped UV faces in ' + mesh + '.'
            return (result, message,flippedUVList)
        else: 
            return ('Not Available','No need to check this!' ,'')
        
def fix(mesh):
    print __name__, mesh