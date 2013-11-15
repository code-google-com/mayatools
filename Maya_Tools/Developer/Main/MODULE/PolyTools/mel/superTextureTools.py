import sys
import time #used to time code execution

import maya.cmds as mc
#import maya.OpenMaya as om
import maya.api.OpenMaya as om
import re
from PIL import Image

#from pymel.all import *
#import pymel.core.datatypes as dt #vector datatype
#import os

def checkTextureAlbedo(path):
#returns 1 if image contains value brighter than 80%
	tex = Image.open(path)
	ext = tex.getextrema()

	if len(ext) == 2: #added to cope with single channel greyscale tifs
		for j in ext:
			if j > 205:
				return 1
		return 0
	else:
		for i in range (0,2): #copes with 3 /4 channel textures
			for j in ext[i]:
				if j > 205:
					return 1
		return 0
	
def getTextureSize(path):
#returns tuple of texture x,y size
	tex = Image.open(path)
	return tex.size
