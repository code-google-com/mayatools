
from maya import cmds, OpenMaya, OpenMayaUI
from pymel.core import *

class AEspliceMayaBaseTemplate(ui.AETemplate):
  def __init__(self, nodeName):
    ui.AETemplate.__init__(self, nodeName)

    self.__nodeName = nodeName

    cmds.editorTemplate(beginScrollLayout = True, collapse = False)
    cmds.editorTemplate(beginLayout = "Splice", collapse = False)
    
    self.callCustom(self.new, self.replace, '')
    
    cmds.editorTemplate(endLayout = True)
    cmds.editorTemplate(endScrollLayout = True)

  def __openSpliceEditor(self, arg):
    selectedNames = cmds.ls(sl=True)
    nodeName = self.__nodeName
    for selectedName in selectedNames:
      nodeType = cmds.nodeType(selectedName)
      if nodeType.startswith('splice'):
        nodeName = selectedName
        break
    cmds.fabricSpliceEditor(action="setNode", node=nodeName)
    
  def new(self, attr):
    cmds.setUITemplate("attributeEditorTemplate", pushTemplate=True)
    cmds.button(label='Open Splice Editor', command=self.__openSpliceEditor)
    cmds.setUITemplate(popTemplate=True)

  def replace(self, attr):
    pass

class AEspliceMayaNodeTemplate(AEspliceMayaBaseTemplate):
  _nodeType = 'spliceMayaNode'
  
class AEspliceMayaDeformerTemplate(AEspliceMayaBaseTemplate):
  _nodeType = 'spliceMayaDeformer'
  
