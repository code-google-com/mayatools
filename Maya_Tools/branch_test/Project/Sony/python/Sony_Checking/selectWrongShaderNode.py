description = 'Select Mesh using wrong shader'
name = 'selectWrongShaderNode'
import os, inspect

fileDirCommmon = os.path.split(os.path.split(os.path.split(inspect.getfile(inspect.currentframe()))[0])[0])[0]

try:
    reload(GE_QA)
except:
    import GE_QA

def execute():
    form = GE_QA.shaderValidator(fileDirCommmon + '/XMLFiles/shaderDefinition.xml')
    form.show()  