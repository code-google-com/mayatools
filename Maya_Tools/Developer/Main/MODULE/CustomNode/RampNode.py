###
###

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.mel as mel


kPluginNodeTypeName = "rpRampNode"

rampNodeId = OpenMaya.MTypeId(0x89010)

# Node definition
class rampNode(OpenMayaMPx.MPxNode):
    
        # class variables
        ramp01    = OpenMaya.MRampAttribute()
        numSegs =        OpenMaya.MObject()
        outTwisty =        OpenMaya.MObject()


        ##AEtemplate proc for the MRampAtributes
        mel.eval('''
                    global proc AErpRampNodeTemplate( string $nodeName )
{
	AEswatchDisplay  $nodeName;
	editorTemplate -beginScrollLayout;
		editorTemplate -beginLayout "ramp Node Template" -collapse 0;
			
			AEaddRampControl ($nodeName+".ramp01");

		editorTemplate -endLayout;
		
		

	editorTemplate -addExtraControls;
	editorTemplate -endScrollLayout;
}

                    ''')
        
        
        def __init__(self):
                OpenMayaMPx.MPxNode.__init__(self)

             
        def compute(self, plug, dataBlock):
                #Set the attribute ramp01 to the plug
                thisNode = self.thisMObject()
                rampPlug = OpenMaya.MPlug( thisNode, rampNode.ramp01 )
                rampPlug.setAttribute(rampNode.ramp01)
                RampPlug01 = OpenMaya.MPlug(rampPlug.node(), rampPlug.attribute())
                
                #Get the atrributes as MRampAttribute
                myRamp = OpenMaya.MRampAttribute(RampPlug01.node(), RampPlug01.attribute())

                # Get the input handle
                dataHandle = dataBlock.inputValue(rampNode.numSegs)
                result = dataHandle.asInt()
 
                #Get output handle and its array data builder
                outputHandle = dataBlock.outputArrayValue(rampNode.outTwisty)
                outputBuilder = outputHandle.builder()
                numElements = outputHandle.elementCount()

                # Some variables
                myValAtPos = []
                dels = []
                
                #Get the float for get the average values
                for i in range(result):
                    quo = 1.0/(result - 1.0)
              
                    myFloat = quo*i

                    #Def to get value at position
                    def getValAtPos():
                    
                        valAt_util = OpenMaya.MScriptUtil()

                        #Get the value as pointer
                        valAt_util.createFromDouble(1.0)
                        valAtPtr = valAt_util.asFloatPtr()

                        #Get the value at position
                        myRamp.getValueAtPosition(myFloat, valAtPtr)

                        #Get the value at pointer as float
                        valAtPos = valAt_util.getFloat(valAtPtr)

                        return (valAtPos)

                    myValAtPos.append(getValAtPos())

                    #Set the myValAtPos in the output attributes array
                    try:
                        outputHandle.jumpToArrayElement(i)
                        outdatahandle = outputHandle.outputValue()
                    except:
                        pass
  
                    outdatahandle.setDouble(myValAtPos[i])
                    
                #Remove the unused elements in the attribute array.
                for w in range(numElements):
                    try:
                        outputHandle.jumpToArrayElement(w)
                        myIndex = outputHandle.elementIndex()
                    except:
                        pass

                    if (myIndex >= result):
                        try:  
                            outputBuilder.removeElement(myIndex)
                        except:
                            pass
                        
                return OpenMaya.kUnknownParameter                


# creator
def nodeCreator():
        return OpenMayaMPx.asMPxPtr( rampNode() )
        
       
# initializer
def nodeInitializer():
       
        #ramp01
        rampNode.ramp01= OpenMaya.MRampAttribute.createCurveRamp('ramp01', 'rmp01')
        

        #NumSegs
        nAttr = OpenMaya.MFnNumericAttribute()
        rampNode.numSegs = nAttr.create ( "numSegs", "nseg", OpenMaya.MFnNumericData.kInt, 0 )
        nAttr.setWritable(1)
        nAttr.setStorable(1)


        #outTwisty
        nAttr = OpenMaya.MFnNumericAttribute()
        rampNode.outTwisty = nAttr.create( "outTwisty", "ot", OpenMaya.MFnNumericData.kDouble, 0.0 )
        nAttr.setArray(1)
        nAttr.setStorable(1)
        nAttr.setUsesArrayDataBuilder(1)


        #Add Attributes
        rampNode.addAttribute( rampNode.ramp01 )
        rampNode.addAttribute ( rampNode.numSegs )
        rampNode.addAttribute( rampNode.outTwisty )


        #Attribute affects
        rampNode.attributeAffects( rampNode.ramp01 , rampNode.outTwisty )
        rampNode.attributeAffects( rampNode.numSegs , rampNode.outTwisty )
        
        

# initialize the script plug-in
def initializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject, "Rosenio Pinto", "1.0", "Any")
        try:
                mplugin.registerNode( kPluginNodeTypeName, rampNodeId, nodeCreator, nodeInitializer )
                
        except:
                sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
                raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterNode( rampNodeId )
        except:
                sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
                raise

###
###
