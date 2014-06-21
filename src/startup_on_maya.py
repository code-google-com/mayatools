import os, sys, imp

def loadProject(projName):
    if os.environ.get('PROJECT_DIR') + projName not in sys.path:
        sys.path.append(os.environ.get('PROJECT_DIR') + projName)
    file, pathname, description = imp.find_module(projName)
    try:
        print pathname
        return imp.load_module(projName, file, pathname, description)
    except:
        print 'cannot load project'
    finally:
        if file: file.close() 

proj = loadProject('template_proj')
proj.main()