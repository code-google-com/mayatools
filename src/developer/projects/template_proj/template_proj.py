'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: project main entry

'''
import inspect,os
import pymel.core as py

try:
    reload(ui)
except:
    from developer.main import projectUI as ui
    
dirfile = os.path.split(inspect.getfile(inspect.currentframe()))[0]
ProjectName = os.path.splitext(os.path.split(inspect.getfile(inspect.currentframe()))[1])[0]
ProjectXML = dirfile + '/xml/' + ProjectName + '.xml'

if py.window('ProjectUIWindow', q = True, ex= True):
    py.deleteUI('ProjectUIWindow')    
form = ui.projectUI(ProjectXML)
form.show()