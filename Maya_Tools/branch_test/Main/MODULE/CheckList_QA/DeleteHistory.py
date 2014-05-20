import maya.cmds as cmds
import maya.mel as mel

__name__ = 'Delete History'

def run(mesh):
    message = ''
    result = False
    nodeType = cmds.nodeType(mesh)
    if nodeType == 'transform':
        shapeNode = cmds.pickWalk(mesh,d='down')[0]
        if cmds.nodeType(shapeNode) == 'mesh':
            try:
                plug = ''.join([mesh,'.inMesh'])
                history = cmds.connectionInfo(plug, isDestination = True)
            except ValueError:
                result = 'Not Available'
                message = 'Please double check this node for sure!'
                return (result, message, '')
            if history:
                result = False
                message = 'Please delete History for ' + mesh + '. '
            else:
                result = True
                message = mesh + ' is deleted History. Good to go!'
        else:
            result = 'Not Available'
            message = mesh + ' is not Geometry. Please check again!'    
        return (result, message,'')
    
def fix(mesh):
    mel.eval('DeleteHistory')