import os, re, random, inspect
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *
import pymel.core as py
import pymel.core.datatypes as dt

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]

description = 'Convert shader to DirectX 11.'
name = '_01_convertShader'

def execute():
    cameraNode = py.ls(type = 'camera')
    