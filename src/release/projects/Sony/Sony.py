'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: project main entry

'''
import inspect,os

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
