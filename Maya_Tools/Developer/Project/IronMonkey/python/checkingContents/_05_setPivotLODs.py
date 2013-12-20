import inspect, os, re
import maya.mel as mel
import pymel.core as py
import pymel.core.datatypes as dt

description = 'Set car\'s position to proper place'
name = 'carSetup'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')
    
def getCenterPointOfMesh(mesh):
    py.xform(mesh, cp = 1)
    cp = dt.Vector(py.xform(mesh, q= True, sp = True, ws = True))
    return cp

def execute():
    loc = py.ls('wheel_arch_loc')
    if not len(loc):
        print 'Cannot set up car. Please create a wheel_arch locator'
        return 
    pos_loc = py.xform(loc, q= True, t= True)
    if pos_loc == [0.0, 0.0, 0.0]:
        print 'please make sure the wheel_arch_loc not freeze transform'
        return
    print 'Set up position for J_car\n'
    print '---------------------------'
    J_Root = py.ls('J_car')[0]
    J_Root.translateX.set(0)
    curr_pos = J_Root.translateY.get()
    J_Root.translateY.set(-pos_loc[1] + curr_pos)
    J_Root.translateZ.set(0)
    print 'Set position for J_chassis'
    
    cp_archos_01 = getCenterPointOfMesh('mesh_rotor_front_left_a_lod00')
    cp_archos_02 = getCenterPointOfMesh('mesh_rotor_rear_left_a_lod00')
    cp = (cp_archos_02 + cp_archos_01)/2

    joints = py.ls('mesh','J_suspension_top_front_left','J_suspension_top_front_right','J_suspension_top_rear_left','J_suspension_top_rear_right')
    for j in joints:
        curr_pos = j.translateZ.get()
        j.translateZ.set(curr_pos - cp[2])
        
    # create wheel match dimension
    cyl_01 = py.polyCylinder(r = 0.36, h = 0.25)
    cyl_01[0].rotateZ.set(90)
    cyl_01[0].translate.set(cp_archos_01)
    
    # create wheel match dimension
    cyl_02 = py.polyCylinder(r = 0.36, h = 0.25)
    cyl_02[0].rotateZ.set(90)
    cyl_02[0].translate.set(cp_archos_02)
    
    print 'Set up position for locator\n'
    print '---------------------------'
    
    
    