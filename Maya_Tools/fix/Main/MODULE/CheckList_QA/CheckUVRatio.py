import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel


def getShaderNonTilingFromSelectedMesh():
	out = list()
	cmds.hyperShade(smn = True)
	shaders = cmds.ls(sl = True, mat = True)
	for shader in shaders:
		if shader not in listShaderTiling:
			out.append(shader)
	return out
	
def findUVShellOnMesh(mesh, UVSet = 'map1'):
    UVShells = OpenMaya.MIntArray()
    ptr = OpenMaya.MScriptUtil()
    ptr.createFromInt(0)
    UVShellNumbers = ptr.asUintPtr()
    #print dagPath.fullPathName()
    mesh.getUvShellsIds(UVShells, UVShellNumbers, 'map1')
    #print str(ptr.getUint(UVShellNumbers))
    return UVShells
    
def selectFaceByShaderPerMesh(shader, mesh):
    out = list()
    cmds.hyperShade(objects = shader)
    selFaces = cmds.ls(sl = True, fl = True)
    print selFaces
    for face in selFaces:
        rootMesh = face.split('.')[0]
        if rootMesh == mesh:
            out.append(face)
    print out
    return out
    
def getIndexUVShellTilingOnMesh(mesh, meshName):
    UVShells = findUVShellOnMesh(mesh, UVSet = 'map1')
    out = set(UVShells)
    shadersNonTiling =  getShaderNonTilingFromSelectedMesh()
    for shader in shadersNonTiling:
        selectFaceByShaderPerMesh(shader, meshName)
        uvList = cmds.polyListComponentConversion(tuv = True)
        cmds.select(uvList)
        uvList = cmds.ls(sl = True, fl = True)
        firstUV = int(uvList[0].split('.')[1].rstrip(']').lstrip('map['))
        indexShell = UVShells[firstUV]
        out.remove(indexShell)
    return out
    
def getRatioFromUVShell(mesh, meshName, indexUVShell, UVSet = 'map1'):
    UVRatio = 0
    UVShells = findUVShellOnMesh(mesh, UVSet)
    exit = False
    index = 0
    while not exit:
        if UVShells[index] == indexUVShell:
            exit = True
        else:
            index += 1
    cmds.select(meshName + '.map[' + str(index) + ']')
    faceList = cmds.polyListComponentConversion(tf = True)
    print faceList
    cmds.select(faceList)
    mel.eval('ConvertSelectionToUVShell')
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)
    iter = OpenMaya.MItSelectionList(selection)
    while not iter.isDone():
        dagPath = OpenMaya.MDagPath()
        component = OpenMaya.MObject()
        iter.getDagPath(dagPath, component)
        piter = OpenMaya.MItMeshPolygon(dagPath, component)
        
        utilAreaUV = OpenMaya.MScriptUtil(0.0)
        utilAreaUV.createFromDouble(0.0)
        areaUV = utilAreaUV.asDoublePtr()
        utilAreaGeometry = OpenMaya.MScriptUtil(0.0)
        utilAreaGeometry.createFromDouble(0.0)
        areaGeometry = utilAreaGeometry.asDoublePtr()
        
        totalAreaUV = 0
        totalAreaGeometry = 0
        while not piter.isDone():
            
            piter.getArea(areaGeometry,OpenMaya.MSpace.kWorld)
            geometry = OpenMaya.MScriptUtil(areaGeometry).asDouble()
            totalAreaGeometry += OpenMaya.MScriptUtil(areaGeometry).asDouble()
            
            piter.getUVArea(areaUV,'map1')
            UV = OpenMaya.MScriptUtil(areaUV).asDouble()
            totalAreaUV += OpenMaya.MScriptUtil(areaUV).asDouble()
            
            piter.next()
        UVRatio = totalAreaGeometry / totalAreaUV
        iter.next()
        
    outFaces = cmds.ls(sl = True)
    return (UVRatio, outFaces)
    
def main(*args):
    wrongUVRatioFaces = list()
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection)
    iter = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kGeometric)
    while not iter.isDone():
        
        dag = OpenMaya.MDagPath()
        iter.getDagPath(dag)
        mesh = OpenMaya.MFnMesh(dag)
        meshName = dag.partialPathName().replace('Shape','')
        outIndex = getIndexUVShellTilingOnMesh(mesh, meshName)
        print outIndex
        for i in outIndex:
            (UVRatio, faces) = getRatioFromUVShell(mesh,dag.fullPathName(), i)
            if UVRatio <= 26 and UVRatio >= 24:
                wrongUVRatioFaces.append(faces)
        cmds.select(wrongUVRatioFaces)        
        iter.next()
	    
UI()
