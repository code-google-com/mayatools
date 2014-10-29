import pymel.core as py
import maya.cmds as cmds
import os


mat_def_Ext = {'Aluminium Rough': 1, 'Aluminium Shiny': 2, 'Badge Glossy': 3, 'Badge Shadow': 4, 'Carbon': 5, 'Chrome': 6, 'Light': 7, 'Paint Glossy': 8, 'Paint Mettalic': 9, 'Pitch Black': 10, 'Plastic Rough': 11, 'Plastic Shiny': 12, 'Rubber Rough': 13, 'Rubber Semi Shiny': 14, 'Exhaust Inside Rough': 15, 'Exhaust Inside Shiny': 16}
mat_def_Int = {'Aluminium Rough': 1, 'Aluminium Shiny': 2, 'Badge Glossy': 3, 'Badge Shadow': 4, 'Carbon': 5, 'Chrome': 6, 'Leather':7, 'Light': 8, 'Mirror':9, 'Paint Glossy': 10, 'Paint Mettalic': 11, 'Pitch Black': 12, 'Plastic Rough': 13, 'Plastic Shiny': 14, 'Rubber Rough': 15, 'Rubber Semi Shiny': 16, 'Exhaust Inside Rough': 17, 'Exhaust Inside Shiny': 18}
mat = ['Badge_Material', 'Base_Material', 'Coloured_Material', 'Carbon_Material', 'Glass_Material', 'Grill_Material', 'GroundShadow_Material', 'Light_Material', 'Override_Material', 'Paint_Material', 'Unused_Material', 'Window_Material']

sub_lodAs =['Body','ANIMATED_EngineBlock','ANIMATED_HoodHinge1','ANIMATED_HoodStrutRodLeft','ANIMATED_HoodStrutRodRight','ANIMATED_HoodHinge2','TARGET_HoodStrutLeft','TARGET_HoodStrutRight','ANIMATED_Bootlid','ANIMATED_BootLidStrutRod_Right','ANIMATED_BootLidStrutRod_Left','TARGET_BootLidStrut_Left','TARGET_BootLidStrut_Right','ANIMATED_Door_Left','ANIMATED_Door_Right','ANIMATED_SteeringWheel'] 
sub_Bodys = ['Fender_Rear','Bumper_Rear','Skirt','Bumper_Front','Fender_Front','Roof','Exhaust','Wiper_Left','Wiper_Right','Engine','Chassis','Taillight','Headlight','Windows','Interior','Seat_Right','Seat_Left','Boot']
sub_materials = ['Paint_Geo','Carbon_Geo','Grille1_Geo','Coloured_Geo','Badge_Geo','Light_Geo','Glass_Geo']

geo = ['Base_Geo', 'Badge_Geo', 'Grill_Geo', 'Paint_Geo', 'Coloured_Geo', 'Window_Geo', 'Glass_Geo', 'Light_Geo', 'Carbon_Geo','Glass_Geo']
sub_geo = ['Bumper_Front', 'Hood', 'Fender_Front', 'Door', 'Fender_Rear', 'Skirt', 'Bumper_Rear', 'Roof', 'Mirror', 'Spoiler', 'Bootlid']


def getSlot(material):
    return (mat_def[material]/8 + 1 if mat_def[material] < 8 else mat_def[material]/8 + 1 , mat_def[material] % 8 if (mat_def[material] % 8) != 0 else mat_def[material])
def getSlot_Int(material):
    return mat_def_Int[material]

def unwrapToSlot_Int(material):
    facesSel =  py.ls(sl = True)
    transformNode = py.ls(hl = True)[0]
    shapeNode = transformNode.listRelatives(c = True)[0]
    print shapeNode
    py.polyProjection(t = 'spherical', ch = True, isu = 1/80.0, isv =1/80.0 )
    uvs = py.polyListComponentConversion(facesSel, tuv = True)
    py.select(uvs)
    # --------------------
    n = getSlot_Int(material)
    print('tem: ',n)
    #du = (getSlot_Int(material)-1) * 1/8.0 + 1/18.0 
    du = 4/1024.00 + (2*n-1)*(7.50/1024)+(n-1)*3/1024.00 
    #du = 0.004 + n*(0.0075)+(n-1)*0.003
    print("Du: ",du)
    dv = 1 -(4 + 7.5)/1024.00
    
    # --------------------
    pPos = shapeNode.getAttr('uvPivot')
    print('pPos 0: ',pPos[0])
    print('pPos 1: ',pPos[1])
    py.polyEditUV(r = True, u = du - pPos[0], v = dv - pPos[1])
    shapeNode.setAttr('uvPivot', (du, dv), type = 'double2')






def unwrapToSlot(material):
    facesSel =  py.ls(sl = True)
    transformNode = py.ls(hl = True)[0]
    shapeNode = transformNode.listRelatives(c = True)[0]
    print shapeNode
    py.polyProjection(t = 'spherical', ch = True, isu = 1/64.0, isv =1/64.0 )
    uvs = py.polyListComponentConversion(facesSel, tuv = True)
    py.select(uvs)
    # --------------------
    du = (getSlot(material)[1] - 1) * 1/8.0 + 1/16.0 
    print('Du Trung:',du)
    dv = (8 - getSlot(material)[0]) * 1/8.0 + 1/16.0
    print dv
    # --------------------
    pPos = shapeNode.getAttr('uvPivot')
    py.polyEditUV(r = True, u = du - pPos[0], v = dv - pPos[1])
    shapeNode.setAttr('uvPivot', (du, dv), type = 'double2')



    
def createMat(*arg):
    for i in mat:
        if not cmds.objExists(i):
            shader = cmds.shadingNode('phong', n = i, asShader = True)
            if i == 'Coloured_Material':
                cmds.setAttr(shader + '.color',  0, 255, 0, type = "double3")
            if i == 'Paint_Material':
                cmds.setAttr(shader + '.color',  255, 0, 0, type = "double3")
            if i == 'Grill_Material':
                cmds.setAttr(shader + '.color',  0, 0, 0, type = "double3")
            if i == 'Light_Material':
                cmds.setAttr(shader + '.color',  0, 0, 0, type = "double3")
            if i == 'Unused_Material':
                cmds.setAttr(shader + '.color',  0, 255, 0, type = "double3")
            if i == 'Window_Material':
                cmds.setAttr(shader + '.color',  29, 65, 33, type = "double3")
                cmds.setAttr(shader + '.transparency',  0.27, 0.27, 0.27, type = "double3")
            if i == 'Base_Material':
                cmds.setAttr(shader + '.color',  0, 0, 0, type = "double3")
                
    
def createHierachy(*arg):
    model = cmds.group(n = 'Model', em = True)
    loda = cmds.group(n = 'lodA', em = True)
    anim_Body = cmds.spaceLocator(n='ANIMATED_Body')
    for sub_lodA in sub_lodAs:
        if not cmds.objExists(sub_lodA):
            if sub_lodA =='Body':
                g_body = cmds.group(n = sub_lodA, em = True)
                for sub_Body in sub_Bodys:
                    if not cmds.objExists(sub_lodA + '|' + sub_Body):
                        g_subBody = cmds.group(n = sub_Body, em =True)
                        for sub_material in sub_materials:
                            if not cmds.objExists(sub_lodA + '|' + sub_Body+'|'+sub_material):
                                g_subMaterial = cmds.group(n = sub_material, em =True)
                                g_Outer = cmds.group(n = 'Outer', em =True)
                                g_Floating = cmds.group(n = 'Floating', em =True)
                                cmds.parent(g_Floating, g_Outer)
                                cmds.parent(g_Outer,g_subMaterial)
                                cmds.parent(g_subMaterial,g_subBody)
                        cmds.parent(g_subBody,g_body)
                cmds.parent(g_body,anim_Body)
                
            else:
                #g_anim = cmds.spaceLocator(n=sub_lodA)
                if sub_lodA=='ANIMATED_EngineBlock':
                    # Tao Group EngineBlock va nhung Group con cua no.
                    ANIMATED_EngineBlock = cmds.group(n = 'ANIMATED_EngineBlock', em =True)
                    g_engineBlock = cmds.group(n = 'EngineBlock', em =True)
                    #Engine_Geo
                    g_Engine_Geo = cmds.group(n = 'Engine_Geo', em =True)
                    g_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_Inner,g_Engine_Geo)
                    cmds.parent(g_Engine_Geo,g_engineBlock)
                    # Badge_Geo
                    g_Badge_Geo = cmds.group(n = 'Badge_Geo', em =True)
                    g_Badge_Geo_inner = cmds.group(n = 'Inner', em =True)
                    g_Badge_Geo_Floating = cmds.group(n = 'Floating', em =True)
                    g_Badge_Geo_Floating_Badge_Geo = cmds.group(n = 'Badge_Geo', em =True)
                    cmds.parent(g_Badge_Geo_Floating_Badge_Geo,g_Badge_Geo_Floating)
                    cmds.parent(g_Badge_Geo_Floating,g_Badge_Geo_inner)
                    cmds.parent(g_Badge_Geo_inner,g_Badge_Geo)
                    cmds.parent(g_Badge_Geo,g_engineBlock)
                    # Coloured_Geo:
                    g_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    g_Coloured_Geo_Inner_Floating = cmds.group(n = 'Floating', em =True)
                    cmds.parent(g_Coloured_Geo_Inner_Floating,g_Coloured_Geo_Inner)
                    cmds.parent(g_Coloured_Geo_Inner,g_Coloured_Geo)
                    cmds.parent(g_Coloured_Geo,g_engineBlock)
                    # Parent voi g_Anim:
                    cmds.parent(g_engineBlock,ANIMATED_EngineBlock)
                elif sub_lodA=='ANIMATED_HoodHinge1':
                    ANIMATED_HoodHinge1 = cmds.spaceLocator(n='ANIMATED_HoodHinge1')
                    # tao HoodHinge1 va nhung group con:
                    
                    g_HoodHinge1 = cmds.group(n = 'HoodHinge1', em =True)
                    g_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodHinge1_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodHinge1_Coloured_Geo_Inner,g_Coloured_Geo)
                    cmds.parent(g_Coloured_Geo,g_HoodHinge1)
                    cmds.parent(g_HoodHinge1,ANIMATED_HoodHinge1)
                    
                    # ANIMATED_Hood va nhung group con.
                    ANIMATED_Hood = cmds.spaceLocator(n='ANIMATED_Hood')
                    cmds.parent(ANIMATED_Hood,ANIMATED_HoodHinge1)
                    #sub cua ANIMATED_Hood
                    #ANIMATED_HoodStrutLeft
                    ANIMATED_HoodStrutLeft = cmds.spaceLocator(n='ANIMATED_HoodStrutLeft')
                    g_HoodStrut = cmds.group(n = 'HoodStrut', em =True)
                    g_HoodStrut_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodStrut_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodStrut_Coloured_Geo_Inner,g_HoodStrut_Coloured_Geo)
                    cmds.parent(g_HoodStrut_Coloured_Geo,g_HoodStrut)
                    cmds.parent(g_HoodStrut,ANIMATED_HoodStrutLeft)
                    cmds.parent(ANIMATED_HoodStrutLeft,ANIMATED_Hood)
                    # ANIMATED_HoodStrutRight
                    ANIMATED_HoodStrutRight = cmds.spaceLocator(n='ANIMATED_HoodStrutRight')
                    g_HoodStrutRight = cmds.group(n = 'HoodStrut', em =True)
                    g_HoodStrut_Coloured_Geo_Right = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodStrut_Coloured_Geo_Inner_Right = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodStrut_Coloured_Geo_Inner_Right,g_HoodStrut_Coloured_Geo_Right)
                    cmds.parent(g_HoodStrut_Coloured_Geo_Right,g_HoodStrutRight)
                    cmds.parent(g_HoodStrutRight,ANIMATED_HoodStrutRight)
                    cmds.parent(ANIMATED_HoodStrutRight,ANIMATED_Hood)
                    # Hood
                    g_Hood = cmds.group(n = 'Hood', em =True)
                    #Coloured_Geo
                    g_Hood_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_Hood_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    g_Hood_Coloured_Geo_Inner_Floating = cmds.group(n = 'Floating', em =True)
                    cmds.parent(g_Hood_Coloured_Geo_Inner_Floating,g_Hood_Coloured_Geo_Inner)
                    cmds.parent(g_Hood_Coloured_Geo_Inner,g_Hood_Coloured_Geo)
                    cmds.parent(g_Hood_Coloured_Geo,g_Hood)
                    #Paint_Geo:
                    g_Hood_Paint_Geo = cmds.group(n = 'Paint_Geo', em =True)
                    g_Hood_Paint_Geo_Outer = cmds.group(n = 'Paint_Geo', em =True)
                    cmds.parent(g_Hood_Paint_Geo_Outer,g_Hood_Paint_Geo)
                    cmds.parent(g_Hood_Paint_Geo,g_Hood)
                    #Badge_Geo:
                    g_Hood_Badge_Geo = cmds.group(n = 'Badge_Geo', em =True)
                    g_Hood_Badge_Geo_Outer = cmds.group(n = 'Outer', em =True)
                    g_Hood_Badge_Geo_Outer_Floating = cmds.group(n = 'Floating', em =True)
                    cmds.parent(g_Hood_Badge_Geo_Outer_Floating,g_Hood_Badge_Geo_Outer)
                    cmds.parent(g_Hood_Badge_Geo_Outer,g_Hood_Badge_Geo)
                    
                    g_Hood_Badge_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    g_Hood_Badge_Geo_Inner_Floating = cmds.group(n = 'Floating', em =True)
                    cmds.parent(g_Hood_Badge_Geo_Inner_Floating,g_Hood_Badge_Geo_Inner)
                    cmds.parent(g_Hood_Badge_Geo_Inner,g_Hood_Badge_Geo)
                    cmds.parent(g_Hood_Badge_Geo,g_Hood)
                    #Grille1_Geo
                    g_Hood_Grille1_Geo = cmds.group(n = 'Grille1_Geo', em =True)
                    g_Hood_Grille1_Geo_Outer = cmds.group(n = 'Outer', em =True)
                    cmds.parent(g_Hood_Grille1_Geo_Outer,g_Hood_Grille1_Geo)
                    g_Hood_Grille1_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_Hood_Grille1_Geo_Inner,g_Hood_Grille1_Geo)
                    cmds.parent(g_Hood_Grille1_Geo,g_Hood)
                    #Carbon_Geo
                    g_Hood_Carbon_Geo = cmds.group(n = 'Carbon_Geo', em =True)
                    g_Hood_Carbon_Geo_Inner = cmds.group(n = 'Carbon_Geo', em =True)
                    cmds.parent(g_Hood_Carbon_Geo_Inner,g_Hood_Carbon_Geo)
                    cmds.parent(g_Hood_Carbon_Geo,g_Hood)
                    cmds.parent(g_Hood,ANIMATED_Hood)
                    #TARGET_HoodStrutRodLeft:
                    TARGET_HoodStrutRodLeft = cmds.spaceLocator(n='TARGET_HoodStrutRodLeft')
                    cmds.parent(TARGET_HoodStrutRodLeft,ANIMATED_Hood)
                    #TARGET_HoodStrutRodRight:
                    TARGET_HoodStrutRodRight = cmds.spaceLocator(n='TARGET_HoodStrutRodRight')
                    cmds.parent(TARGET_HoodStrutRodRight,ANIMATED_Hood)
                    #TARGET_HoodHinge2:
                    TARGET_HoodHinge2 = cmds.spaceLocator(n='TARGET_HoodHinge2')
                    cmds.parent(TARGET_HoodHinge2,ANIMATED_Hood)
                elif sub_lodA=='ANIMATED_HoodStrutRodLeft':
                    ANIMATED_HoodStrutRodLeft = cmds.spaceLocator(n='ANIMATED_HoodStrutRodLeft')
                    g_HoodStrutRod = cmds.group(n = 'HoodStrutRod', em =True)
                    g_HoodStrutRod_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodStrutRod_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodStrutRod_Coloured_Geo_Inner,g_HoodStrutRod_Coloured_Geo)
                    cmds.parent(g_HoodStrutRod_Coloured_Geo,g_HoodStrutRod)
                    cmds.parent(g_HoodStrutRod,ANIMATED_HoodStrutRodLeft)
                    
                    
                elif sub_lodA=='ANIMATED_HoodStrutRodRight':
                    ANIMATED_HoodStrutRodRight = cmds.spaceLocator(n='ANIMATED_HoodStrutRodRight')
                    g_HoodStrutRod = cmds.group(n = 'HoodStrutRod', em =True)
                    g_HoodStrutRod_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodStrutRod_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodStrutRod_Coloured_Geo_Inner,g_HoodStrutRod_Coloured_Geo)
                    cmds.parent(g_HoodStrutRod_Coloured_Geo,g_HoodStrutRod)
                    cmds.parent(g_HoodStrutRod,ANIMATED_HoodStrutRodRight)    
                    
                elif sub_lodA=='ANIMATED_HoodHinge2':
                    ANIMATED_HoodHinge2 = cmds.spaceLocator(n='ANIMATED_HoodHinge2')
                    g_HoodHinge2 = cmds.group(n = 'HoodHinge2', em =True)
                    g_HoodHinge2_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    g_HoodHinge2_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    cmds.parent(g_HoodHinge2_Coloured_Geo_Inner,g_HoodHinge2_Coloured_Geo)
                    cmds.parent(g_HoodHinge2_Coloured_Geo,g_HoodHinge2)
                    cmds.parent(g_HoodHinge2,ANIMATED_HoodHinge2)
                
                elif sub_lodA=='TARGET_HoodStrutLeft':
                    TARGET_HoodStrutLeft = cmds.spaceLocator(n='TARGET_HoodStrutLeft')

                elif sub_lodA=='TARGET_HoodStrutRight':
                    TARGET_HoodStrutLeft = cmds.spaceLocator(n='TARGET_HoodStrutRight')
                
                elif sub_lodA=='ANIMATED_Bootlid':
                    ANIMATED_Bootlid = cmds.spaceLocator(n='ANIMATED_Bootlid')
                    g_BootLid = cmds.group(n = 'BootLid', em =True)
                    cmds.parent(g_BootLid,ANIMATED_Bootlid)
                    
                    ANIMATED_BootLidStrut_Left = cmds.spaceLocator(n='ANIMATED_BootLidStrut_Left')
                    #g_BootLidStrut_Left = cmds.group(n = 'BootLidStrut_Left', em =True)
                    #g_BootLidStrut_Left_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    #g_BootLidStrut_Left_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    
                    #cmds.parent(g_BootLidStrut_Left_Coloured_Geo_Inner,g_BootLidStrut_Left_Coloured_Geo)
                    #cmds.parent(g_BootLidStrut_Left_Coloured_Geo,g_BootLidStrut_Left)
                    #cmds.parent(g_BootLidStrut_Left,ANIMATED_BootLidStrut_Left)    
                    cmds.parent(ANIMATED_BootLidStrut_Left,ANIMATED_Bootlid)    
                    
                    ANIMATED_BootLidStrut_Right = cmds.spaceLocator(n='ANIMATED_BootLidStrut_Right')
                    #g_BootLidStrut_Right = cmds.group(n = 'BootLidStrut_Right', em =True)
                    #g_BootLidStrut_Right_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    #g_BootLidStrut_Right_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    
                    #cmds.parent(g_BootLidStrut_Left_Coloured_Geo_Inner,g_BootLidStrut_Left_Coloured_Geo)
                    #cmds.parent(g_BootLidStrut_Left_Coloured_Geo,g_BootLidStrut_Left)
                    #cmds.parent(g_BootLidStrut_Left,ANIMATED_BootLidStrut_Left)    
                    cmds.parent(ANIMATED_BootLidStrut_Right,ANIMATED_Bootlid)              
                
                elif sub_lodA=='ANIMATED_BootLidStrutRod_Right':
                    ANIMATED_BootLidStrutRod_Right = cmds.spaceLocator(n='ANIMATED_BootLidStrutRod_Right')
                    #g_BootLidStrutRob_Right = cmds.group(n = 'BootLidStrutRob_Right', em =True)
                    #g_BootLidStrut_Right_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    #g_BootLidStrut_Right_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    
                    #cmds.parent(g_BootLidStrut_Right_Coloured_Geo_Inner,g_BootLidStrut_Right_Coloured_Geo)
                    #cmds.parent(g_BootLidStrut_Right_Coloured_Geo,g_BootLidStrutRob_Right)
                    #cmds.parent(g_BootLidStrutRob_Right,ANIMATED_BootLidStrutRod_Right)    
                      
                    
                elif sub_lodA=='ANIMATED_BootLidStrutRod_Left':
                    ANIMATED_BootLidStrutRod_Left = cmds.spaceLocator(n='ANIMATED_BootLidStrutRod_Left')
                    #g_BootLidStrutRob_Left = cmds.group(n = 'BootLidStrutRob_Right', em =True)
                    #g_BootLidStrutRob_Left_Coloured_Geo = cmds.group(n = 'Coloured_Geo', em =True)
                    #g_BootLidStrutRob_Left_Coloured_Geo_Inner = cmds.group(n = 'Inner', em =True)
                    
                    #cmds.parent(g_BootLidStrutRob_Left_Coloured_Geo_Inner,g_BootLidStrutRob_Left_Coloured_Geo)
                    #cmds.parent(g_BootLidStrutRob_Left_Coloured_Geo,g_BootLidStrutRob_Left)
                    #cmds.parent(g_BootLidStrutRob_Left,ANIMATED_BootLidStrutRod_Left)    
                
                elif sub_lodA=='TARGET_BootLidStrut_Left':
                    TARGET_BootLidStrut_Left = cmds.spaceLocator(n='TARGET_BootLidStrut_Left')
                
                elif sub_lodA=='TARGET_BootLidStrut_Right':
                    TARGET_BootLidStrut_Right = cmds.spaceLocator(n='TARGET_BootLidStrut_Right')
                
                elif sub_lodA=='ANIMATED_Door_Left':
                    ANIMATED_Door_Left = cmds.spaceLocator(n='ANIMATED_Door_Left')
                    #g_Mirror_Left = cmds.group(n = 'Mirror_Left', em =True)
                    #cmds.parent(g_Mirror_Left,ANIMATED_Door_Left)
                    #g_Door_Left = cmds.group(n = 'Mirror_Left', em =True)
                    #cmds.parent(g_Door_Left,ANIMATED_Door_Left)
                    
                    #ANIMATED_DoorWindow_Left = cmds.spaceLocator(n='ANIMATED_DoorWindow_Left')
                    #g_DoorWindow_Left = cmds.group(n = 'DoorWindow_Left', em =True)
                    #cmds.parent(g_DoorWindow_Left,ANIMATED_DoorWindow_Left)
                    #cmds.parent(ANIMATED_DoorWindow_Left,ANIMATED_Door_Left)                    
                
                elif sub_lodA=='ANIMATED_Door_Right':
                    ANIMATED_Door_Right = cmds.spaceLocator(n='ANIMATED_Door_Right')
                    #g_Mirror_Right = cmds.group(n = 'Mirror_Left', em =True)
                    #cmds.parent(g_Mirror_Right,ANIMATED_Door_Right)
                    #g_Door_Right = cmds.group(n = 'Door_Right', em =True)
                    #cmds.parent(g_Door_Right,ANIMATED_Door_Right)
                    
                    #ANIMATED_DoorWindow_Right = cmds.spaceLocator(n='ANIMATED_DoorWindow_Right')
                    #g_DoorWindow_Right = cmds.group(n = 'DoorWindow_Right', em =True)
                    #cmds.parent(g_DoorWindow_Right,ANIMATED_DoorWindow_Right)
                    #cmds.parent(ANIMATED_DoorWindow_Right,ANIMATED_Door_Right)
                
                elif sub_lodA=='ANIMATED_SteeringWheel':      
                     ANIMATED_SteeringWheel = cmds.spaceLocator(n='ANIMATED_SteeringWheel')
                     g_SteeringWheel = cmds.group(n = 'SteeringWheel', em =True)
                     cmds.parent(g_SteeringWheel,ANIMATED_SteeringWheel)
                cmds.parent(sub_lodA,anim_Body)
                     
    cmds.parent(anim_Body,loda)                           
    '''
    for g in geo:
        if not cmds.objExists(g):
            g_Group = cmds.group(n = g, em = True)
            for sg in sub_geo:
                if not cmds.objExists(g + '|' + sg):
                    sg_Group = cmds.group(n = sg, em =True)
                    cmds.parent(sg_Group, g_Group)
        cmds.parent(g_Group, loda)
    cmds.parent(loda, model)
    '''
    
def assignTextures(*arg):
    texDir = os.path.split(os.path.split(cmds.file(q= True, sn = True))[0])[0]
    lightTex = texDir + '/Textures/' + cmds.file(q= True, sn = True).split('/')[2] + '_Light_Material.tga'
    bagdeTex = texDir + '/Textures/' + cmds.file(q= True, sn = True).split('/')[2] + '_Badge_Diffuse.tga'
    geoTex = 'T:/Scenes/NaturalMotion/Tech/texture.tga'
    
    if cmds.objExists('lightTexNode'):
        cmds.delete('lightTexNode')
    lightTexNode = cmds.shadingNode('file',n = 'lightTexNode', asTexture = True)
    cmds.setAttr(lightTexNode + '.fileTextureName', lightTex, type = 'string')
    cmds.connectAttr(lightTexNode + '.outColor', 'Light_Material.color', f = True)
    
    if cmds.objExists('badgeTexNode'):
        cmds.delete('badgeTexNode')
    badgeTexNode = cmds.shadingNode('file',n = 'badgeTexNode', asTexture = True)
    cmds.setAttr(badgeTexNode + '.fileTextureName', bagdeTex, type = 'string')
    cmds.connectAttr(badgeTexNode + '.outColor', 'Badge_Material.color', f = True)
    
    if cmds.objExists('geoTexNode'):
        cmds.delete('geoTexNode')
    geoTexNode = cmds.shadingNode('file',n = 'geoTexNode', asTexture = True)
    cmds.setAttr(geoTexNode + '.fileTextureName', geoTex, type = 'string')
    cmds.connectAttr(geoTexNode + '.outColor', 'Coloured_Material.color', f = True)
    
    
def createGUI():
    if cmds.window('NaturalMotion_Tools', exists = True):
        cmds.deleteUI('NaturalMotion_Tools')
    cmds.window('NaturalMotion_Tools', w = 2, h = 50)
    cmds.columnLayout(rowSpacing = 5, columnWidth = 250, columnAttach = ('both', 2))
    cmds.optionMenu( w= 245, label='Materials:', changeCommand=unwrapToSlot )
    cmds.menuItem( label='Aluminium Rough')
    cmds.menuItem( label='Aluminium Shiny')
    cmds.menuItem( label='Badge Glossy')
    cmds.menuItem( label='Badge Shadow')
    cmds.menuItem( label='Carbon')
    cmds.menuItem( label='Chrome')
    cmds.menuItem( label='Light')
    cmds.menuItem( label='Paint Glossy')
    cmds.menuItem( label='Paint Mettalic')
    cmds.menuItem( label='Pitch Black')
    cmds.menuItem( label='Plastic Rough')
    cmds.menuItem( label='Plastic Shiny')
    cmds.menuItem( label='Rubber Rough')
    cmds.menuItem( label='Plastic Shiny')
    cmds.menuItem( label='Rubber Semi Shiny')
    cmds.menuItem( label='Rubber Rough')
    cmds.menuItem( label='Exhaust Inside Rough')
    cmds.menuItem( label='Exhaust Inside Shiny')
    
    cmds.optionMenu( w= 245, label='Materials Int:', changeCommand=unwrapToSlot_Int)
    cmds.menuItem( label='Aluminium Rough')
    cmds.menuItem( label='Aluminium Shiny')
    cmds.menuItem( label='Badge Glossy')
    cmds.menuItem( label='Badge Shadow')
    cmds.menuItem( label='Carbon')
    cmds.menuItem( label='Chrome')
    cmds.menuItem( label='Leather')
    cmds.menuItem( label='Light')
    cmds.menuItem( label='Mirror')  
    cmds.menuItem( label='Paint Glossy')
    cmds.menuItem( label='Paint Mettalic')
    cmds.menuItem( label='Pitch Black')
    cmds.menuItem( label='Plastic Rough')
    cmds.menuItem( label='Plastic Shiny')
    cmds.menuItem( label='Rubber Rough')
    cmds.menuItem( label='Rubber Semi Shiny') 
    cmds.menuItem( label='Exhaust Inside Rough')
    cmds.menuItem( label='Exhaust Inside Shiny')
    cmds.separator()
    cmds.button(label = 'Create Material', h = 25, c = createMat)
    cmds.button(label = 'Create Hierarchy', h = 25, c = createHierachy)
    cmds.button(label = 'Assign Textures', h = 25, c = assignTextures)
    cmds.showWindow()


