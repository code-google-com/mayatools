import inspect,os
import maya.cmds as cmds
'load project'
try:
    reload(ProjectUI)
except:
    import ProjectUI
    
dirfile = os.path.split(inspect.getfile(inspect.currentframe()))[0]
ProjectName = os.path.splitext(os.path.split(inspect.getfile(inspect.currentframe()))[1])[0]
ProjectXML = dirfile + '/XMLfiles/' + ProjectName + '.xml'

def main():
    #if cmds.window(MainForm, e = True):
    #    print 'delete Window'
    #    cmds.deleteUI(MainForm, window = True)
    MainForm = ProjectUI.ProjectUI(ProjectXML)
    MainForm.show()
