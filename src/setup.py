'''
Created on Jun 23, 2014

@author: Trung
'''
from distutils.core import setup
import py2exe
from glob import glob

data_files =[()]

setup(console=['startup_on_maya.py'])