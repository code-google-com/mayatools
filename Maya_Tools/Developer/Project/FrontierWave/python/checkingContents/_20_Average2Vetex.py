description = 'Average 2 Vetex'
name = 'Average2Vetex'

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import os, inspect

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    
    # check and warn if nothing is selected
    sel = cmds.ls( sl=True, fl=True )
    print('sel ', sel)
    if sel == []:
        cmds.confirmDialog( title="Selection Error", message="No vertex selected. Please select one or two vertex.", button=["Ok"], defaultButton="Ok" )

    # calculate number of selected vertex and warn in case of selection errors    
    verNum = cmds.polyEvaluate( vc=True )
    print('verNum',verNum)
    if verNum == 0:
        cmds.confirmDialog( title="Selection Error", message="No vertex selected. Please select one or two vertex.", button=["Ok"], defaultButton="Ok" )
    if verNum > 2 and sel != []:
        cmds.confirmDialog( title="Selection Error", message="More than two vertex are selected. Please select only one or two.", button=["Ok"], defaultButton="Ok" )

    # if only one vertex is selected
    if verNum == 1:
    # get the position of the vertex
        pos = cmds.xform( sel, q=True, ws=True, t=True )
        pX = pos[0]
        pY = pos[1]
        pZ = pos[2]

    # move pivot to the position of the vertex         
        selObj = cmds.ls( hl=True )
        cmds.xform( selObj, ws=True, rp=(pX, pY, pZ) )        
    # go back to object mode
        cmds.select( selObj )        

    # if two vertex are selected
    if verNum == 2:
    # get the position of both vertex    
        posFir = cmds.xform( sel[0], q=True, ws=True, t=True )
        posSec = cmds.xform( sel[1], q=True, ws=True, t=True )
        pXFir = posFir[0]
        pYFir = posFir[1]
        pZFir = posFir[2]
        pXSec = posSec[0]
        pYSec = posSec[1]
        pZSec = posSec[2]
    # calculate the average between the two
        pXTot =( posFir[0] + posSec[0] ) / 2
        print('pX ',pXTot)
        pYTot =( posFir[1] + posSec[1] ) / 2
        print('pY ',pYTot)
        pZTot =( posFir[2] + posSec[2] ) / 2
        print('pZ ',pZTot)
    # move pivot to the average position 
        #selObj = cmds.ls( hl=True)
        cmds.xform( sel, ws=True, rp=(pXTot, pYTot, pZTot) )
        #for i in sel:
            #cmds.polyMoveVertex(i,s=(pXTot, pYTot, pZTot))
    # go back to object mode
        cmds.select( sel )
        print('selObj: ',sel)
    
    
    