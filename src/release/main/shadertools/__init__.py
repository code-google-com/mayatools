from random import *

import boltUvRatio
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py


shadersValidatedList ={'chrome_1':'DaS', 'diffuse_black_plastic':'D', 'diffuse_holes':'D', 'diffuse_light':'N', 'diffusebumped_tire':'DM','lightglass_1':'DTaSI','paint_white':'DaS','transparent_grill':'D','windowglass_1':'DTaSI','windowglass_black':'DTaSI'}

def unParentAllScene():
    meshes = cmds.ls(type = 'mesh')
    groupTemp = cmds.group(em = True)
    for m in meshes:
        cmds.parent(m, groupTemp)
    transformLoc = [cmds.listRelatives(loc,p = True)[0] for loc in cmds.ls(type = 'locator')]
    cmds.delete(transformLoc)

def createLocatorGroup(*arg):
    errorMesh = []
    meshes = py.ls(type = 'mesh')
    for m in meshes:
        transformNode = m.listRelatives(p = True)[0]
        nodes = transformNode.split('_')
        if len(nodes) == 4: 
            gName = nodes[0] + '_' + nodes[1] + '_' + nodes[2]
        elif len(nodes) == 3:
            gName = transformNode
        if cmds.objExists(str(gName)): # check if locator exists
            gName = py.ls(gName)[0]
            if not gName.listRelatives(c = True)[0].nodeType() == 'locator':
                loc = py.spaceLocator()
                try:
                    py.parent(transformNode, loc)
                except:
                    pass
                py.rename(loc, gName)
            else:
                try:
                    py.parent(transformNode, gName)
                except:
                    pass
        else:
            loc = py.spaceLocator()
            try:
                py.parent(transformNode, loc)
            except:
                pass
            py.rename(loc, gName)
            
def naming(*arg):
    mel.eval('showHidden -all;')
    errorMeshes = list()
    meshes = cmds.ls(type = 'mesh')
    for m in meshes:
        #shape = cmds.listRelatives(node, s = True)[0]
        sgs = cmds.listConnections(m, type =  'shadingEngine')
        shaders = list(set([cmds.connectionInfo(x + '.surfaceShader', sfd = True).split('.')[0] for x in sgs]))
        if len(shaders) > 1:
            errorMeshes.append(m.replace('Shape',''))
            print m + ' khong co sp luong material dung.'
        else:
            if shaders[0] not in shadersValidatedList:
                errorMeshes.append(m.replace('Shape',''))
                print m + ' khong co material dung.'
            else:
                if shadersValidatedList[shaders[0]] not in m:
                    transformNode = cmds.listRelatives(m,p = True)[0]
                    newname = transformNode + '_' + shadersValidatedList[shaders[0]]
                    try:
                        cmds.rename(transformNode, newname)
                    except:
                        cmds.rename(transformNode + '|' + transformNode, newname)
    cmds.select(errorMeshes)
    mel.eval('showHidden -a;')
                
def checkNumsMaterial():
    mel.eval('showHidden -all;')
    result = ''
    mats = cmds.ls(materials = True)
    if mats > 10:
        result =  "Shader Report  ------  So luong Material nhieu hon can thiet.\n\n"
    elif mats < 10:
        result =  "Shader Report  ------  So luong Material it hon can thiet.\n\n"
    else:
        result =  "Shader Report  ------  Check Material hoan tat.\n\n"
    return result
    
        
def checkWrongMaterial():
    mel.eval('showHidden -all;')
    result = ''
    mats = cmds.ls(materials = True)
    for m in mats:
        if (m not in shadersValidatedList.keys()) and (m not in ['lambert1','particleCloud1']):
            result += "Shader Report  ------  " + m + ' khong co trong danh sach nhung material cua du an.\n\n'
    return result
    
def checkMaterial(*arg):
    result = '---------------------------MATERIAL CHECKS----------------------------------\n\n'
    result += checkNumsMaterial()
    result += checkWrongMaterial()
    print result
    
def checkIsParentingCorrect():
    mel.eval('showHidden -all;')
    errorMeshesOutput = list()
    result = ''
    locators = py.ls(type = 'locator')
    if len(locators) == 0:
        result += 'Locator Warning  ------  Scene chua duoc setup dung. Can chay Setup Locators.\n\n'
        return result
    #parentLoc = [m.listRelatives(p = True) for m in locators]
    else:
        errorMeshes = list()
        for locShape in locators:
            src = locShape.listRelatives(p = True)[0]
            errorMeshes = [mesh for mesh in src.listRelatives(ad = True, type = 'mesh') if str(src).lstrip('|') not in str(mesh).split('|')[-1]]
            if len(errorMeshes) != 0:
                print src
                print errorMeshes
                for err in errorMeshes:
                    result += 'Locator Warning  ------  ' + err + ' chua duoc parent dung cho.\n\n'
                mel.eval('showHidden -a;')
            errorMeshesOutput += errorMeshes
        py.select(errorMeshesOutput)
        if len(errorMeshesOutput) == 0:
            result += 'Locator Warning  ------  Check mesh hierachy hoan tat.\n\n'
    return result
                
def checkMeshes(*arg):
    result = '---------------------------MESHES CHECKS----------------------------------\n\n'
    result += checkIsParentingCorrect()
    print result
    
def setUVRatio(*arg):
    ratio = 157873.72303
    boltUvRatio.collect_shells_and_set_shells_UV_ratio(ratio)
    
def setShaderToSelectedFaces(shader):
    # get shadingGroup from shader
    selIns = cmds.ls(sl = True)
    cmds.select(cl = True)
    sg = cmds.connectionInfo(shader + '.outColor', dfs = True)
    if len(sg) == 0:#.split('.')[0]
        #sg = cmds.createNode('shadingEngine', n = shader + 'SG')
        sg = cmds.sets(r = True, nss = True,  n = shader + 'SG')
        #print sg
        cmds.connectAttr(shader + '.outColor', sg + '.surfaceShader', f = True )
        cmds.sets(selIns,e = True, forceElement = sg)
    else:
        sg = sg[0].split('.')[0]
    #cmds.select(selIns)
        cmds.sets(selIns, e = True, forceElement = sg)
    
    
def createMat(*arg):
    for i in shadersValidatedList.keys():
        if not cmds.objExists(i):
            shader = cmds.shadingNode('phong', n = i, asShader = True)
            cmds.setAttr(shader + '.color',  randint(0,255)/255.0, randint(0,255)/255.0, randint(0,255)/255.0, type = "double3")
            
def turnToDamageShader(*arg):
    if cmds.objExists('DAMAGETEX'):
        cmds.delete('DAMAGETEX')
        if cmds.objExists('DAMAGEGLASSTEX'):
            cmds.delete('DAMAGEGLASSTEX')
        return
    damagedShaders = ['paint_white', 'chrome_1']
    damageGlassShaders = ['windowglass_1', 'windowglass_black']
    damageTex = cmds.shadingNode('file',n = 'DAMAGETEX', asTexture = True)
    damageGlassTex = cmds.shadingNode('file',n = 'DAMAGEGLASSTEX', asTexture = True)
    cmds.setAttr(damageTex + '.fileTextureName', '//glassegg.com/Projects/Scenes/Audatex/tech/Scratch_Car.tga', type = 'string')
    cmds.setAttr(damageGlassTex + '.fileTextureName', '//glassegg.com/Projects/Scenes/Audatex/tech/Dent_Glass.tga', type = 'string')
    for s in damagedShaders:
        cmds.connectAttr(damageTex + '.outColor', s + '.color', f = True)
    for s in damageGlassShaders:
        cmds.connectAttr(damageGlassTex + '.outColor', s + '.color', f = True)
        
def groupGlassChromeMesh(*arg):
    ####--------- CREATE GROUP----------------------------------------------
    if not py.objExists('proxyUV'):
        gNode= py.group(em = True, n = 'proxyUV')
    ####--------- CREATE GLASS_PROXY_UV----------------------------------------------
    if not py.objExists('glass_proxy_UV'):
        meshes = py.ls('*DTaSI')# + py.ls('*DaS')
        dupMeshes = py.duplicate(meshes)
        py.polyUnite(dupMeshes, ch = 0, n = 'glass_proxy_UV')
        py.parent('glass_proxy_UV','proxyUV')
    ####--------- CREATE PAINT_CHROME_PROXY_UV----------------------------------------------
    if not py.objExists('chrome_paint_proxy_UV'):
        meshes = py.ls('*DaS')# + py.ls('*DaS')
        dupMeshes = py.duplicate(meshes)
        py.polyUnite(dupMeshes, ch = 0, n = 'chrome_paint_proxy_UV')
        py.parent('chrome_paint_proxy_UV','proxyUV')
    ####--------- CREATE DISPLAY LAYER----------------------------------------------
    if py.objExists('proxy_UV_layer'):
        cmds.createDisplayLayer(n = 'proxy_UV_layer')
    try:
        cmds.editDisplayLayerMembers('proxy_UV_layer', cmds.ls('chrome_paint_proxy_UV'), noRecurse = True)
        cmds.editDisplayLayerMembers('proxy_UV_layer', cmds.ls('glass_proxy_UV'), noRecurse = True)
    except: 
        pass
        
def execute(*arg):
    print '--------------- RENAME SHAPENODE-------------------------'
    meshes = cmds.ls(type= 'mesh')
    for mesh in meshes:
        transformNode = cmds.listRelatives(mesh, parent = True, type = 'transform')[0]
        if mesh != transformNode + 'Shape':
            cmds.rename(mesh, transformNode + 'Shape')
            print '-- Renamed shape node on mesh:' + mesh
            
    print '--------------- RENAME SHADINGNODE-------------------------'
    shaders = py.ls(materials = True)
    for s in shaders:
        try:
            sg = str(s.listConnections(s= True, t= 'shadingEngine')[0])
            py.rename(sg, s+'SG')
            print '-- Renamed shading node: ' + sg + ' to: ' + s + 'SG'
        except:
            pass
    
    print '--------------- RENAME TEXTURENODE-------------------------' 
    textures = py.ls(tex = True)
    for t in textures:
        try:
            name = t.getAttr('fileTextureName').split('/')[-1].split('.')[0] + '_file'
            py.rename(t, name)   
            print '-- Renamed texture node: ' + t + ' to: ' + name
        except:
            pass
            
def flattenCombineSeparate(*arg):
    mel.eval('source geNFS14_FixCorruptObject;')
    mel.eval('geNFS14_FixCorruptObjectGUI;')
    
            
#shadersValidatedList ={'chrome_1':'_DaS', 'diffuse_black_plastic':'_D', 'diffuse_holes':'_D', 'diffuse_light':'_N', 'diffusebumped_tire':'_DM','lightglass':'_DTaSI','paint_white':'_DaS','transparent_grill':'_D','windowglass_1':'_DTaSI','windowglass_':'_DTaSI'}

                
def createGUI():
    if cmds.window('Audatex_Tools', exists = True):
        cmds.deleteUI('Audatex_Tools')
    cmds.window('Audatex_Tools', w = 2, h = 50)
    cmds.columnLayout(rowSpacing = 5, columnWidth = 250, columnAttach = ('both', 2))
    cmds.button(label = 'Setup Locators', command = createLocatorGroup)
    cmds.button(label = 'Naming', command = naming)
    cmds.button(label = 'Validation Materials', command = checkMaterial)
    cmds.button(label = 'Validation Meshes', command = checkMeshes)
    cmds.separator()
    cmds.button(label = 'Set UV Ratio', command = setUVRatio)
    cmds.rowColumnLayout(numberOfColumns = 1)
    #cmds.textScrollList(w = 170, h = 25, append = shadersValidatedList.keys())
    cmds.optionMenu( w= 245, label='Materials:', changeCommand=setShaderToSelectedFaces )
    cmds.menuItem( label='chrome_1')
    cmds.menuItem( label='diffuse_black_plastic')
    cmds.menuItem( label='diffuse_holes')
    cmds.menuItem( label='diffuse_light')
    cmds.menuItem( label='diffusebumped_tire')
    cmds.menuItem( label='lightglass')
    cmds.menuItem( label='paint_white')
    cmds.menuItem( label='transparent_grill')
    cmds.menuItem( label='windowglass_1')
    cmds.menuItem( label='windowglass_')
    cmds.button(label = 'Create Material', h = 25, c = createMat)
    cmds.button(label = 'Damage Material', h = 25, c = turnToDamageShader)
    cmds.button(label = 'Correct Shape Node', h = 25, c = execute)
    cmds.button(label = 'FCO', h = 25, c = flattenCombineSeparate)
    cmds.button(label = 'Group Glass + Chrome Shader',c = groupGlassChromeMesh)
    cmds.separator()
    cmds.showWindow()
    
createGUI()
