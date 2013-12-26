description = 'Restore Shader on missing shader.'
name = 'restoreShader'
import maya.cmds as cmds
import maya.mel as mel
import os, inspect, re
from xml.dom.minidom import *

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def loadXML(xmlFile, content, proper):
        kit = list()
        xmlDoc = xml.dom.minidom.parse(xmlFile)
        root = xmlDoc.firstChild
        kitNodes = root.getElementsByTagName(content)
        kit = [x.getAttribute(proper) for x in kitNodes]
        #kit.append([x.getAttribute('shortname') for x in kitNodes])
        return kit

def execute():
    xmlDir = os.path.split(os.path.split(fileDirCommmon)[0])[0] + '/XMLfiles/IronMonkey_CustomNamingTool.xml'
    materials = loadXML(xmlDir,'material','name')
    short_materials = loadXML(xmlDir,'material','shortname')
 
    print '--------------- RESTORE SHADER ON MESH-------------------------'
    sgs = cmds.ls(type = 'shadingEngine')
    for sg in sgs:
        #try:
            members = cmds.sets(sg, q = True)
            try:
                material_short = members[0].split('_')[1]
                material = materials[short_materials.index(material_short)]
                cmds.connectAttr(material + '.outColor', sg + '.surfaceShader')
            except:
                try:
                    if re.search('(.*)badging_alpha(\.*)', members[0]):
                        material = 'badging_alpha'
                    if re.search('(.*)glass_head(\.*)', members[0]):
                        material = 'glass_headlight_tint_alpha_shatter_cull_nozwrite_layer65'
                    if re.search('(.*)glass_alpha(\.*)', members[0]):
                        material = 'glass_window_tint_alpha_shatter_cull_nozwrite_layer65'
                    if re.search('(.*)glass_tail(\.*)', members[0]):
                        material = 'glass_taillight_tint_alpha_shatter_cull_nozwrite_layer65'
                    if re.search('(.*)headlights_cluster(\.*)', members[0]):
                        material = 'headlight_type_a_opaque'
                    if re.search('(.*)headlight_alpha(\.*)', members[0]):
                        material = 'headlight_type_a_alphaadd'
                    if re.search('(.*)additive(\.*)', members[0]):
                        material = 'head_lights_type_a_alphaadd_nozwrite_twosided_layer70'
                    if re.search('(.*)glass_black_windows(\.*)', members[0]):
                        material = 'glass_window_black_opaque_twosided_shatter'
                    if re.search('(.*)additive_taillight(\.*)', members[0]):
                        material = 'taillight_type_a_opaque'
                    cmds.connectAttr(material + '.outColor', sg + '.surfaceShader')
                except:
                    pass
        #except:
        #    pass
        
    