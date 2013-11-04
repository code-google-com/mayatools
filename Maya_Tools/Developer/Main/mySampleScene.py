'''
Created on Oct 21, 2013

@author: thohoang
'''
# sampleScene.py

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginCmdName = "mySampleScene"

# Vertices used to define a planar house shape within a single MFnMesh object:
#
#              [4]
#             /   \
#            /     \
#          [3]-----[2]        where the bracketed numbers correspond
#           |       |         to the vertex index.
#           |       |
#          [0]-----[1]
#
vertices = [ # Square plane:
             OpenMaya.MPoint( -2, -2, 0), # index 0: bottom left corner
             OpenMaya.MPoint(  2, -2, 0), # index 1: bottom right corner
             OpenMaya.MPoint(  2,  2, 0), # index 2: top right corner
             OpenMaya.MPoint( -2,  2, 0), # index 3: top left corner
             # Vertex used to define the roof:
             OpenMaya.MPoint(  0,  5, 0)  # index 4: tip of the roof.
           ]

# Count the number of times this command has been instantiated.
commandInstanceCounter = 1

##########################################################
# Plug-in 
##########################################################
class SampleSceneCommand(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxCommand.__init__(self)
        
        # We keep track of the number of times the command was instantiated, and we label this particular
        # instance of the command with it. This will help us name the objects manipulated by this particular instance 
        # of the command.
        global commandInstanceCounter
        self.commandExecution = commandInstanceCounter
        commandInstanceCounter = commandInstanceCounter + 1
    
    
    def doIt(self, args):
        ''' Set up the objects which the command will use. '''
        
        # This MDagModifier object will allow us to undo and redo the creation of DAG nodes in our command.
        self.dagModifier = OpenMaya.MDagModifier()
        
        # We first create the required MObjects using the MDagModifer assigned to self.dagModifier.
        #   (!) The 'transform', 'spotLight' and 'camera' strings are recognized by the MDagModifier as valid node type names. 
        #       For a complete list of node type names, consult the Maya User Guide  > Technical Documentation > Nodes section.
        self.meshTransformObj = self.dagModifier.createNode( 'transform' )
        self.meshShapeObj = self.createHouseMesh() # This function will create a mesh under the self.meshTransformObj node.
        
        self.lightTransformObj = self.dagModifier.createNode( 'transform' )
        self.lightShapeObj = self.dagModifier.createNode( 'spotLight', self.lightTransformObj )
        
        self.cameraTransformObj = self.dagModifier.createNode( 'transform' )
        self.cameraShapeObj = self.dagModifier.createNode( 'camera', self.cameraTransformObj )
        
        # Create the shading node.
        self.shadingNodeName = 'myMaterial' + str( self.commandExecution )
        self.dagModifier.commandToExecute( 'shadingNode -asShader -name ' + self.shadingNodeName + ' phong;' )
        self.dagModifier.commandToExecute( 'setAttr "' + self.shadingNodeName + '.color" -type double3 0.7 0.2 0.15;')
        
        # Create the shading group.
        self.shadingGroupName = 'myShadingGroup' + str( self.commandExecution )
        self.dagModifier.commandToExecute( 'sets -renderable true -noSurfaceShader true -empty -name ' + self.shadingGroupName + ';')
        self.dagModifier.commandToExecute( 'connectAttr -f ' + self.shadingNodeName + '.outColor ' + self.shadingGroupName + '.surfaceShader;' )
        
        # Invoke the command's redoIt() function to actually create and manipulate these objects.
        self.redoIt()
    
    
    def createHouseMesh(self):
        ''' Create a house mesh. '''
        global vertices # we want to access the list of vertices defined as a static variable  
        
        meshFn = OpenMaya.MFnMesh()
        mergeVertices = True   # a parameter indicating whether or not nearby vertices will be merged.
        pointTolerance = 0.001 # the distance which determines if any two nearby vertices will be merged.
        
        # Create the base of the house.
        squareVertexArray = OpenMaya.MPointArray()
        squareVertexArray.setLength( 4 )
        squareVertexArray.set( vertices[0], 0 )
        squareVertexArray.set( vertices[1], 1 )
        squareVertexArray.set( vertices[2], 2 )
        squareVertexArray.set( vertices[3], 3 )
        
        # Add the square polygon to the mesh whose parent is self.meshTransformObj.
        meshFn.addPolygon( squareVertexArray, mergeVertices, pointTolerance, self.meshTransformObj)
        
        # Create the roof of the house.
        triangleVertexArray = OpenMaya.MPointArray()
        triangleVertexArray.setLength( 3 )
        triangleVertexArray.set( vertices[3], 0 )
        triangleVertexArray.set( vertices[2], 1 )
        triangleVertexArray.set( vertices[4], 2 ) 
        
        # Add a triangular polygon to the mesh whose parent is self.meshTransformObj. The returned meshShapeObj is
        # a reference to the mesh geometry object.
        meshShapeObj = meshFn.addPolygon( triangleVertexArray, mergeVertices, pointTolerance, self.meshTransformObj)
        
        # Set the name of the mesh.
        meshFn.setName( 'myMeshShape' + str( self.commandExecution ) )
        
        return meshShapeObj
        
    
    def redoIt(self):
        ''' 
        Manipulate the objects created in doIt(). This function is also called by Maya when
        the user re-does the operation after undoing it.
        '''
        
        # Perform the operations enqueued within our reference to MDagModifier.
        self.dagModifier.doIt()
        
        #=======================================
        # MESH MANIPULATION
        #=======================================
        # Set the translation value of the mesh's transform node, as well as its name.
        transformFn = OpenMaya.MFnTransform( self.meshTransformObj )
        transformFn.setTranslation( OpenMaya.MVector( 0, 2, 0 ), OpenMaya.MSpace.kTransform )
        transformFn.setName( 'myMeshTransform' + str( self.commandExecution ) )
        
        # Obtain the DAG path of the mesh transform node. This will be used to create
        # an aiming constraint between the light and the mesh.
        meshTransformDagPath = OpenMaya.MDagPath()
        transformFn.getPath( meshTransformDagPath )
        
        # The DAG path of the mesh shape node will be used to apply a material.
        meshShapeDagPath = OpenMaya.MDagPath()
        meshFn = OpenMaya.MFnMesh( self.meshShapeObj )
        meshFn.getPath( meshShapeDagPath )
                
        #=======================================
        # LIGHT MANIPULATION
        #=======================================
        # Set the translation value of the light's transform node, as well as its name.
        transformFn = OpenMaya.MFnTransform( self.lightTransformObj )
        transformFn.setTranslation( OpenMaya.MVector( 4, 9.5, 12 ), OpenMaya.MSpace.kTransform )
        transformFn.setName( 'myLightTransform' + str( self.commandExecution ) )
        
        # Obtain the DAG path of the light transform node. This will be used to create
        # an aiming constraint between the light and the mesh.
        lightTransformDagPath = OpenMaya.MDagPath()
        transformFn.getPath( lightTransformDagPath )
        
        # Change the name of the light shape
        spotLightFn = OpenMaya.MFnSpotLight( self.lightShapeObj )
        spotLightFn.setName( 'myLightShape' + str( self.commandExecution ) )

        #=======================================
        # CAMERA MANIPULATION
        #=======================================
        # Set the translation value of the camera's transform node, as well as its name. 
        transformFn = OpenMaya.MFnTransform( self.cameraTransformObj )
        transformFn.setTranslation( OpenMaya.MVector( 0, 5, 30 ), OpenMaya.MSpace.kTransform )
        transformFn.setName( 'myCameraTransform' + str( self.commandExecution ) )
        
        # Change the name of the camera shape.
        cameraFn = OpenMaya.MFnCamera( self.cameraShapeObj )
        cameraFn.setName( 'myCameraShape' + str( self.commandExecution ) )
        
        # Store the previous camera before we switch to the camera created within this command.
        # In undo() we will revert to this previous camera.
        self.previousCamera = OpenMaya.MDagPath()
        currentView = OpenMayaUI.M3dView.active3dView()
        currentView.getCamera( self.previousCamera ) # self.previousCamera is now populated with the current camera before we switch.
        
        # Get the DAG path of our camera shape node.
        cameraDagPath = OpenMaya.MDagPath()
        dagNodeFn = OpenMaya.MFnDagNode( self.cameraShapeObj )
        dagNodeFn.getPath( cameraDagPath )
        
        # Set the camera view to the one we switched
        currentView.setCamera( cameraDagPath )
        
        #=======================================
        # AIM CONSTRAINT
        #=======================================
        # Enqueue a MEL command to aim the light to the mesh's transform node. We must use MEL
        # because there is currently no way to enqueue calls to the maya.cmds Python module.
        self.dagModifier.commandToExecute( 'aimConstraint -aimVector 0.0 0.0 -1.0 ' 
                                           + meshTransformDagPath.fullPathName() + ' ' 
                                           + lightTransformDagPath.fullPathName() )
        
        # Execute the MEL command we just added to the MDagModifier. By adding this command to the MDagModifier,
        # we are able to undo it using MDagModifier.undoIt() in our command's undoIt() method. 
        self.dagModifier.doIt()
        
        #=======================================
        # PHONG MATERIAL
        #=======================================
        # Include our mesh shape in the shading group we have defined in this command's doIt() function.
        self.dagModifier.commandToExecute( 'sets -e -forceElement ' + self.shadingGroupName + ' ' + meshShapeDagPath.fullPathName() )
        
        # Execute the queued MEL command.
        self.dagModifier.doIt()
        
        
        # Print the contents of the scene.
        self.printScene()
        
    
    def undoIt(self):
        ''' Undo the command. '''
        
        # Switch back to the previous camera
        currentView = OpenMayaUI.M3dView.active3dView()
        currentView.setCamera( self.previousCamera )
        
        # This call to MDagModifier.undoIt() undoes all the operations within the MDagModifier.
        # Observe that the number of calls to MDagModifier.undoIt() does not need to match the number of calls to MDagModifier.doIt().
        self.dagModifier.undoIt()
        
    
    def isUndoable(self):
        ''' This command must be undoable because it affects the structure of the DAG. '''
        return True
    
        
    def printScene(self):
        ''' Traverse and print the elements in the scene graph (DAG)  '''
        # Create a function set which we will re-use throughout our scene graph traversal.
        dagNodeFn = OpenMaya.MFnDagNode()
        
        # Create an iterator to traverse the scene graph starting at the world node
        # (the scene's origin). We use a depth-first traversal, and we do not filter for
        # any scene elements, as indicated by the 'OpenMaya.MFn.kInvalid' parameter.
        dagIterator = OpenMaya.MItDag( OpenMaya.MItDag.kDepthFirst,
                                       OpenMaya.MFn.kInvalid )

        print '====================='
        print ' SCENE GRAPH (DAG):  '
        print '====================='
        
        # Traverse the scene.
        while( not dagIterator.isDone() ):
            
            # Obtain the current item.
            currentObj = dagIterator.currentItem()
            depth = dagIterator.depth()
            
            # Make our dag node function set operate on the current object.
            dagNodeFn.setObject( currentObj )
                       
            # Extract the dag node information to print.
            name = dagNodeFn.name()
            type = currentObj.apiTypeStr()
            path = dagNodeFn.fullPathName()
            
            # generate our output by first incrementing the tabs based on the depth
            # of the current object. This formats our output nicely.
            output = ''
            for i in range( 0, depth ):
                output += '\t'
                
            output += name + ': ' + type + ' [' + path + ']'
            print output
            
            # Increment to the next item.
            dagIterator.next()
        
        print '====================='
                
        
##########################################################
# Plug-in initialization.
##########################################################       
def cmdCreator():
    ''' Creates an instance of the scripted command. '''
    return OpenMayaMPx.asMPxPtr( SampleSceneCommand() )
    
def initializePlugin(mobject):
    ''' Initializes the plug-in.'''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )

def uninitializePlugin(mobject):
    ''' Uninitializes the plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )


##########################################################
# Sample usage.
##########################################################

# Copy the following lines and run them in Maya's Python Script Editor:

import maya.cmds as cmds
cmds.loadPlugin('D:/foxforest/Maya_tools/Developer/Main/mySampleScene.py')
cmds.mySampleScene()