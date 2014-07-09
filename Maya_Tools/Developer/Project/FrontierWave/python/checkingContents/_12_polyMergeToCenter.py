description = 'Poly Merge To Center'
name = 'polyMergeToCenter'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

def execute():
    mel.eval('polyMergeToCenter')
