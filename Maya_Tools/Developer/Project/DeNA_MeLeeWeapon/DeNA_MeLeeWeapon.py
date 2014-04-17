import inspect,os
'load project'
try:
    reload(ProjectUI)
except:
    import ProjectUI
    
dirfile = os.path.split(inspect.getfile(inspect.currentframe()))[0]
ProjectName = os.path.splitext(os.path.split(inspect.getfile(inspect.currentframe()))[1])[0]
ProjectXML = dirfile + '/XMLfiles/' + ProjectName + '.xml'

def main():
    MainForm = ProjectUI.ProjectUI(ProjectXML)
    MainForm.show()
