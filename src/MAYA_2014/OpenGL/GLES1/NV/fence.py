'''OpenGL extension NV.fence

This module customises the behaviour of the 
OpenGL.raw.GLES1.NV.fence to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/fence.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.NV.fence import *
from OpenGL.raw.GLES1.NV.fence import _EXTENSION_NAME

def glInitFenceNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glDeleteFencesNV.fences size not checked against n
glDeleteFencesNV=wrapper.wrapper(glDeleteFencesNV).setInputArraySize(
    'fences', None
)
glGenFencesNV=wrapper.wrapper(glGenFencesNV).setOutput(
    'fences',size=lambda x:(x,),pnameArg='n',orPassIn=True
)
glGetFenceivNV=wrapper.wrapper(glGetFenceivNV).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
### END AUTOGENERATED SECTION