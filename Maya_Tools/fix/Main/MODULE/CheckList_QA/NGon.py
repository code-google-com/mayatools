import maya.cmds as cmds

__name__ = 'N-Gon'

def run(mesh):
    result = False
    message = ''
    if cmds.nodeType(mesh) == 'transform':
        shapeNode = cmds.pickWalk(mesh,d = 'down')[0]
        if cmds.nodeType(shapeNode) == 'mesh':
            cmds.select(mesh)
            cmds.selectType(pf = True)
            cmds.polySelectConstraint(mode = 3,type = 0x0008, size = 3)
            sel = cmds.ls(sl = True , flatten = True)
            result = (len(sel) == 0 ) or False
            if result:
                message = 'No face is more than 4 sides was found in ' + mesh
            else:
                message = 'There are ' + str(len(sel)) +' faces which have more than 4 sides in '+ mesh + '. Please fix by cleaning up in \'CleanUp Options\'.'
            return (result, message,sel)
        else:
            return ('Not Available','No need to check this!')
        
def fix(mesh):
    print __name__, mesh