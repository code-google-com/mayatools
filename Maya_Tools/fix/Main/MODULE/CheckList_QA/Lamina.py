import time
from maya import cmds as cmds

__name__ = 'Lamina Faces'

def run(mesh):
    result = False
    message = ''
    if cmds.nodeType(mesh) == 'transform':
        shapeNode = cmds.pickWalk(mesh,d = 'down')[0]
        if cmds.nodeType(shapeNode) == 'mesh':
            cmds.select(mesh)
            cmds.selectType( pf=True ) 
            cmds.polySelectConstraint(mode=3, type=0x0008, topology=2) # lamina)
            sel=cmds.ls(sl=True, fl=True)
            result = (len(sel) == 0) or False
            cmds.polySelectConstraint(disable=True)
            if result:
                message = 'No faces share all edges together in ' + mesh + '.'
            else:
                message = 'There are ' + str(len(sel)) +' polys are sharing all edges in ' + mesh + '. Please fix by \'CleanUp Option\'.'
            return (result, message, sel)
        else:
            return ('Not Available','No need to check this!' ,'')
        
def fix(mesh):
    print __name__, mesh