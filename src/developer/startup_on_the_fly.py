import os, sys, imp

def loadProject(projName):

    file, pathname, description = imp.find_module(projName)
    try:
        print pathname
        return imp.load_module(projName, file, pathname, description)
    except:
        print 'cannot load project'
    finally:
        if file: file.close() 

proj = loadProject('geProject')
proj.main()