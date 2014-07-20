'''
Chris Zukowski
Pipe Maker Script Simple V2.0
This version of the script does not have custom pipe. It is only the straightup bendpipes. 
Still very useful, but not nearly as powerful.

Move the script the documents/maya/scripts   folder
Copy and Paste this section of code to run. Make sure you set it to python.

import zPipeMakerSimple 
reload(zPipeMakerSimple)
zPipeMakerSimple.gui()

More info on how to use it can be found at 
http://zukodesign.com/?page_id=369
'''

import os
import math
import ConfigParser
import maya.cmds as cmds
import sys


window = "zPipeMakerV01"
if( cmds.window(window, ex=True)):
    cmds.deleteUI(window)

class zPipeMaker(object):

    def __init__(self):
        #DEBUG MODE 1=ON 0=OFF
        self.scriptVersion = 2.11
        self.debugMode = 0
        #-------------
        #self.fnDebug("check for config file")
        #Get INI File for rest of script
        filename=os.path.basename(__file__)
        curFileDirectory=os.path.realpath(__file__)
        curFileDirectory=curFileDirectory[0:(len(curFileDirectory)-len(filename))]

        self.window = "zPipeMakerV01"
        self.iniFile=curFileDirectory+"zPipeMakerSimpleConfig.ini"
        self.mayaVersion=cmds.about(v=True)
        # self.config["chk_AutoUpdate"][2]='False'
        # self.config["chk_AutoOptimize"][2]='False'
        self.curLengthRepeat=1
        self.ApplySetting_Cs_Selected=1
        self.skipConfig = 0

        self.crvMultiplier=3.14/180
        self.crvDivider=180

        if(self.mayaVersion[0:4]=="2014"):
            self.crvMultiplier=1

        self.fnInitializeGui()
    #LETS ROLL!
    def fnInitializeGui(self):
        self.fnGetMayaSettings()
        self.fnGetConfig()

        #2010 Layout Changer
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            self.windowWidth01=320
            self.windowWidth02=320
        else:
            self.windowWidth01=305
            self.windowWidth02=370

        cmds.window(self.window, title="zPipeMakerV"+str(self.scriptVersion), w=self.windowWidth01,h=465)

        self.fnLayout()
        
        cmds.showWindow(self.window)

        temp_lsControlGroup=[]
        for cGrp in self.lsControlGroup:
            if(cmds.objExists(cGrp)):
                # self.MP_Amt_Str=self.lsControlGroup[len(self.lsControlGroup)-3:len(self.lsControlGroup)]
                # self.MP_Amt=int(self.MP_Amt_Str)
                temp_lsControlGroup.append(cGrp)
        if not len(temp_lsControlGroup)==0:
            cmds.select(temp_lsControlGroup)
            self.fnConnectControls(0)

    def fnLayout(self):
        '''<<< Open 1 TabIndex01 '''
        cmds.scrollLayout('zPipeScroll',width=320, scrollAreaWidth=320,scrollAreaHeight=465,p=self.window)
        form = cmds.formLayout('zPipeIndex')
        self.tabs = cmds.tabLayout('tabMain',innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout( form, edit=True,w=310, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )

        self.fnLayoutMainControls()
        self.fnLayoutSettings()
        self.fnLayoutAbout()        

        cmds.setParent('..')
        ''' Close 2 zPipeIndex'''
        cmds.setParent('..')
        ''' Close 1 ltMain    '''
        cmds.setParent( '..' )

    def fnLayoutMainControls(self):
        ######  START TABS #######
        cmds.setParent( "tabMain" )
        self.child1=cmds.columnLayout('TabIndex01',w=300)
        cmds.columnLayout('TI1',w=300)
        #Maya 2010 Layout Changer (MAIN BUTTONS)
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Main Buttons")
        else:
            '''<<< Open 1.1 FL1 '''
            cmds.frameLayout('FL1', label='Main Buttons',
                p="TabIndex01",borderStyle='in',
                bgc=[0.123,0.196,0.023], w=365,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_MainSliders"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )

        '''<<< Open 2 RCL1 '''
        cmds.rowColumnLayout('RCL1',nc=3,w=360, cw=[(1,100),(2,100),(3,100)])

        #-------------------- Main Buttons ------------------#
        cmds.button('btElbowPipe', label="Add Pipe", c=lambda x:self.fnElbowPipe("add"))
        cmds.button('btElbowPipeNew', label="New Pipe", c=lambda x:self.fnElbowPipe("new"))
        cmds.button('btConnectControl', label="Connect Controls", c=lambda x:self.fnConnectControls(0))
        cmds.setParent( '..' )

        cmds.rowColumnLayout('RCL1_2',nc=3,w=360,  cw=[(1,100),(2,100),(3,100)])

        #self.fnDebug(self.Cs_Selected-1)

        '''>>> Close 2 RCL1 '''
        cmds.setParent( '..' )

        #-------------------- Main Controls ------------------#
        '''<<< Open 2.2 RCL2 '''
        cmds.rowColumnLayout('RCL2',nc=3,w=360, cw=[(1,80),(2,160),(3,60)])

        #Sub Axis
        cmds.text(l="  Sub Axis", align="left")
        cmds.intSlider( 'slPipe_SubAxis', min=0, max=self.config["sldr_subAxis"][2])
        cmds.intField( 'ifPipe_SubAxis')

        #Sub Height
        cmds.text(l="  Sub Height", align="left")
        cmds.intSlider( 'slPipe_SubHt', min=1, max=self.config["sldr_subHeight"][2] )
        cmds.intField( 'ifPipe_SubHt')

        #Width
        cmds.text(l="  Radius", align="left")
        cmds.floatSlider( 'slPipe_ScaleXZ', min=0.001, max=self.config["sldr_width"][2], v=25 )
        cmds.floatField( 'ifPipe_ScaleXZ',pre=2)

        #Curve Length
        cmds.text(l="  Curve Length", align="left")
        cmds.floatSlider( 'slPipe_Length',
            min=-self.config["sldr_length"][2],
            max=self.config["sldr_length"][2],
            v=0 ,
            cc=lambda x:self.fnCurveLength())

        cmds.floatField( 'ifPipe_Length',pre=2, cc=lambda x:self.fnCurveLength(1))

        #Curve Scale
        cmds.text(l="  Curve Scale", align="left")
        cmds.floatSlider( 'slPipe_Scale',
            min=0.001,
            max=self.config["sldr_curScale"][2],
            v=self.config["sldr_curScale"][2],)

        cmds.floatField( 'ifPipe_Scale',pre=2)

        #Curve Amount
        cmds.text(l="  Curve Amount", align="left")
        cmds.floatSlider( 'slPipe_CurveAmt',
            min=-self.config["sldr_curAmt"][2],
            max=self.config["sldr_curAmt"][2],)

        cmds.floatField( 'ifPipe_CurveAmt',pre=2)

        #Rotation
        cmds.text(l="  Rotation", align="left")
        cmds.floatSlider( 'slPipe_Rotate',
            s=100,
            min=-self.config["sldr_rotation"][2],
            max=self.config["sldr_rotation"][2])

        cmds.floatField( 'ifPipe_Rotate',pre=2)

        '''>>> Close 2.2 RCL2 '''
        cmds.setParent( '..' )

        #-------------------- Quick Settings ------------------#

        #Maya 2010 Layout Changer (QUICK SETTINGS)
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Quick Settings")
        else:
            '''<<< Open 1.3 FL3 '''
            cmds.frameLayout('FL3',
                label='Quick Settings',
                p="TabIndex01",
                borderStyle='in',
                bgc=[0.123,0.196,0.023], w=365 ,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_QuickSettings"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )

        '''<<< Open 2.3 RCL3 '''
        cmds.rowColumnLayout('RCL3',nc=4,w=300,cw=[(1,75),(2,75),(3,75),(4,75)])

        #Quick Buttons  --Bend--
        cmds.button('btQSK0', label="Bend "+self.lsQKSettings[0], c=lambda x: self.fnQuickSettings('B',self.lsQKSettings[0]))
        cmds.button('btQSK1', label="Bend "+self.lsQKSettings[1], c=lambda x: self.fnQuickSettings('B',self.lsQKSettings[1]))
        cmds.button('btQSK2', label="Bend "+self.lsQKSettings[2], c=lambda x: self.fnQuickSettings('B',self.lsQKSettings[2]))
        cmds.button('btQSK3', label="Bend "+self.lsQKSettings[3], c=lambda x: self.fnQuickSettings('B',self.lsQKSettings[3]))
        #Quick Buttons  --Rotate--
        cmds.button('btQSK4', label="Rot "+self.lsQKSettings[4], c=lambda x: self.fnQuickSettings('R',self.lsQKSettings[4]))
        cmds.button('btQSK5', label="Rot "+self.lsQKSettings[5], c=lambda x: self.fnQuickSettings('R',self.lsQKSettings[5]))
        cmds.button('btQSK6', label="Rot "+self.lsQKSettings[6], c=lambda x: self.fnQuickSettings('R',self.lsQKSettings[6]))
        cmds.button('btQSK7', label="Rot "+self.lsQKSettings[7], c=lambda x: self.fnQuickSettings('R',self.lsQKSettings[7]))
        '''>>> Close 2.3 RCL3 '''
        cmds.setParent( '..' )
        if(self.mayaVersion[0:4]!="2010"or self.mayaVersion[0:4]!="2009"):
            '''>>> Close 1.3 FL3 '''
            cmds.setParent( '..' )
        #Maya 2010 Layout Changer  (OTHER OPTIONS)
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Other Options")
        else:
            '''<<< Open 1.4 FL4 '''
            cmds.frameLayout('FL4',
                label='Other Options',
                p="TabIndex01",
                borderStyle='in',
                bgc=[0.123,0.196,0.023],
                w=365,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_OtherOptions"][2]),
                cc=lambda :self.fnApplyUIConfig(),
                ec=lambda :self.fnApplyUIConfig()
                )
        '''<<< Open 2.4 RCL4 '''
        cmds.rowColumnLayout('RCL4',nc=3,w=300,cw=[(1,150),(2,75),(3,75)])

        #Optimize Buttons
        cmds.button('btOptimizeAP', label="Optimize All Pipes", c=lambda x: self.fnOptimizePipe("ALL"))
        cmds.text(l="Opt Threshold")
        cmds.floatField( 'ifPipeOptimize', v=self.config["if_OptimizeThreshold"][2], cc=lambda x: self.fnApplyUIConfig())
        cmds.button('btOptimizeCP', label="Optimize Control Pipe", c=lambda x: self.fnOptimizePipe("CONTROL"))
        cmds.text(l="")
        cmds.text(l="")

        #Auto Checkboxes

        cmds.setParent("..")
        cmds.rowColumnLayout('RCL6',nc=2,w=300,cw=[(1,150),(2,150)])

        cmds.checkBox('ckAutoOptimize',
            label='Use Auto Optimize Pipe', v=self.config["chk_AutoOptimize"][2],cc=lambda x: self.fnChkUpdate("ckAutoOptimize"), ofc=lambda x: self.fnOptimizePipe("CHECKBOX"))
        cmds.button('btDupPipe', label="Duplicate Pipe", c=lambda x:self.fnDuplicate())
        cmds.checkBox('ckRememberRotation',
            label='Remember Rotation', v=self.config["chk_rememberRotation"][2],cc=lambda x: self.fnChkUpdate("ckRememberRotation"))
        cmds.button('btFinishPipe', label="Finish Pipe", c=lambda x:self.fnFinishPipe())

    def fnLayoutSettings(self):
        cmds.setParent( "tabMain" )

        #----------------------------- SETTINGS TAB --------------------------
        self.child3=cmds.columnLayout('TabIndex03',w=300,adj=True)
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Slider Min and Max Settings")
        else:
            cmds.frameLayout('FLSettings1',
                label='Slider Min and Max Settings',
                p="TabIndex03",
                borderStyle='in',
                bgc=[0.123,0.196,0.023],
                w=300,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_Settings"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )

        cmds.rowColumnLayout('RCSettings1',nc=3,w=300,cw=[(1,90),(2,60),(3,150)])

        cmds.text(l="   Sub Axis", align="left")
        cmds.text(l="Max", align="left")
        cmds.intField( 'ifSPipe_SubAxis', v=self.config["sldr_subAxis"][2])

        cmds.text(l="   Sub Height", align="left")
        cmds.text(l="Max", align="left")
        cmds.intField( 'ifSPipe_SubHt', v=self.config["sldr_subHeight"][2])

        cmds.text(l="   Radius", align="left")
        cmds.text(l="Max", align="left")
        cmds.floatField( 'ifSPipe_ScaleXZ', v=self.config["sldr_width"][2])

        cmds.text(l="   Length", align="left")
        cmds.text(l="Max/Min", align="left")
        cmds.floatField( 'ifSPipe_length', v=self.config["sldr_length"][2],pre=2)

        cmds.text(l="   Curve Scale", align="left")
        cmds.text(l="Max", align="left")
        cmds.floatField( 'ifSPipe_Scale', v=self.config["sldr_curScale"][2],pre=2)

        cmds.text(l="   Curve Amount", align="left")
        cmds.text(l="Max/Min", align="left")
        cmds.floatField( 'ifSPipe_CurveAmt', v=self.config["sldr_curAmt"][2],pre=2)

        cmds.text(l="   Rotate", align="left")
        cmds.text(l="Max/Min", align="left")
        cmds.floatField( 'ifSPipe_Rotate', v=self.config["sldr_rotation"][2],pre=2)
        cmds.setParent( '..' )
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Starter Pipe Settings")
        else:
            cmds.frameLayout('FLSettingsStarterPipe2',
                label='Starter Pipe Settings',
                p="TabIndex03",
                borderStyle='in',
                bgc=[0.123,0.196,0.023],
                w=300,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_StarterPipe"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )
        cmds.rowColumnLayout('RCSettingsStarterPipe1',nc=2,w=300,cw=[(1,150),(2,150)])
        cmds.text(l="   Starter Pipe Sub Axis", align="left")
        cmds.intField( 'ffSPipe_MainSubAxis', v=float(self.config["ff_StarterPipeSubAxis"][2]))
        cmds.text(l="   Starter Pipe Sub Height", align="left")
        cmds.floatField( 'ffSPipe_MainSubHeight', v=float(self.config["ff_StarterPipeSubHeight"][2]), pre=2)
        cmds.text(l="   Starter Pipe Length/Scale", align="left")
        cmds.floatField( 'ffSPipe_MainScale', v=float(self.config["ff_StarterPipeScale"][2]), pre=2)
        cmds.text(l="   Starter Pipe Radius", align="left")
        cmds.floatField( 'ffSPipe_MainWidth', v=float(self.config["ff_StarterPipeWidth"][2]), pre=2)
        cmds.setParent( '..' )
        #----------------------- QUICK SETTINGS SECTION--------------------
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Quick Settings")
        else:
            cmds.frameLayout('FLSettings2',
                label='Quick Settings',
                p="TabIndex03",
                borderStyle='in',
                bgc=[0.123,0.196,0.023],
                w=300,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_SettingsQuick"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )

        
        cmds.rowColumnLayout('RCQuickSettings2',nc=4,w=300,cw=[(1,75),(2,75),(3,75),(4,75)])
        cmds.floatField( 'ffSPipe_qkBend01', v=float(self.lsQKSettings[0]), pre=2)
        cmds.floatField( 'ffSPipe_qkBend02', v=float(self.lsQKSettings[1]), pre=2)
        cmds.floatField( 'ffSPipe_qkBend03', v=float(self.lsQKSettings[2]), pre=2)
        cmds.floatField( 'ffSPipe_qkBend04', v=float(self.lsQKSettings[3]), pre=2)

        cmds.floatField( 'ffSPipe_qkRot01', v=float(self.lsQKSettings[4]), pre=2)
        cmds.floatField( 'ffSPipe_qkRot02', v=float(self.lsQKSettings[5]), pre=2)
        cmds.floatField( 'ffSPipe_qkRot03', v=float(self.lsQKSettings[6]), pre=2)
        cmds.floatField( 'ffSPipe_qkRot04', v=float(self.lsQKSettings[7]), pre=2)

        cmds.setParent( '..' )

        #------------------------Other Switches--------------------------
        if(self.mayaVersion[0:4]=="2010"or self.mayaVersion[0:4]=="2009"):
            cmds.text("Other Switches")
        else:
            cmds.frameLayout('FLSettings3',
                label='Other Switches',
                p="TabIndex03",
                borderStyle='in',
                bgc=[0.123,0.196,0.023],
                w=300,
                cll=bool(self.config["FLC_Toggle"][2]) ,
                cl=bool(self.config["FLC_SettingsOtherSwitches"][2]),
                cc=lambda : self.fnApplyUIConfig(),
                ec=lambda : self.fnApplyUIConfig()
                )

        cmds.rowColumnLayout('RColSettings2',nc=2,w=300,cw=[(1,150),(2,150)])

        
        cmds.checkBox('ckSettings_CollapseMenu',
            label='Use Collapsible Menus', v=bool(self.config["FLC_Toggle"][2]))
        cmds.text(" ")
        cmds.checkBox('ckFinishPipeUnfold',
            label='Unfold Final Pipe UVs', v=self.config["chk_unfoldFinalPipeUV"][2], cc=lambda x: self.fnChkUpdate("ckFinishPipeUnfold"))
        cmds.text(" ")
        cmds.checkBox('ckFinishPipeDelete',
            label='Delete zPipes on Finish', v=self.config["chk_deleteFinishPipe"][2], cc=lambda x: self.fnChkUpdate("ckFinishPipeDelete"))

        cmds.setParent( 'TabIndex03' )
        cmds.rowColumnLayout('RCSettings3',nc=2,w=300,cw=[(1,150),(2,150)])

        cmds.button('btSetDefaults', label="Set Default", c=lambda x: self.fnWriteConfig(1))
        cmds.button('btApplySettings', label="Apply Settings", c=lambda x: self.fnApplySettings(0))

        cmds.setParent( '..' )


        cmds.setParent( '..' )
        #self.fnDebug("Layout2")

    def fnLayoutAbout(self):
        cmds.setParent( "tabMain" )
        #------------------------------------ABOUT------------------------------
        self.child4=cmds.columnLayout('TabIndex04',w=300,adj=True)
        cmds.text("About zPipeMaker")
        ######## FINISH PARENTS ########
        cmds.text(" ")
        cmds.text("zPipeMaker v"+str(self.scriptVersion))
        cmds.text("Created By: Chris Zukowski")
        cmds.text(" ")
        cmds.text("Special Thanks")
        cmds.text("Steve Ross")
        cmds.text("Robert White")
        cmds.text("Paul Lohman")
        cmds.text(" ")
        # cmds.columnLayout()
        cmds.text("  More information on how to use the script can be found at")
        cmds.text("  www.zukodesign.com/?page_id=369")
        cmds.text(" ")
        cmds.text("  If you have any bug reports or major issues please feel ")
        cmds.text("  free to contact me at chriszuko@gmail.com.")
        cmds.text(" ")
        cmds.text("  Lastly, if you want to use custom meshes you can! Just  ")
        cmds.text("  check out zPipemaker Advanced!")

        # cmds.setParent( '..' )
        cmds.text(" ")
        cmds.text("Thanks for using this script.")
        cmds.text("Have a good day!")
        cmds.text("-Zuko")

        cmds.tabLayout( self.tabs,
                edit=True,
                tabLabel=((self.child1, 'Main Controls'),(self.child3, 'Settings'),(self.child4, 'About')),
                sti=self.config["TL_SelectedTab"][2],
                cc=lambda:self.fnApplyUIConfig())

    def fnChkUpdate(self, chkBoxName):
        chkAmt=cmds.checkBox(chkBoxName, q=True,v=True)

        if (chkBoxName=="ckRememberRotation"):
            self.config["chk_rememberRotation"][2]=int(chkAmt)
        elif(chkBoxName=="ckAutoOptimize"):
            self.config["chk_AutoOptimize"][2]=int(chkAmt)
        elif(chkBoxName=="ckFinishPipeUnfold"):
            self.config["chk_unfoldFinalPipeUV"][2]=int(chkAmt)
        elif(chkBoxName=="ckFinishPipeDelete"):
            self.config["chk_deleteFinishPipe"][2]=int(chkAmt)

        self.fnWriteConfig(0)

    def fnCurveLength(self):
        # print(self.lsControlGroup)
        for cGrp in self.lsControlGroup:
            if not cmds.objExists(cGrp):
                self.fnError("Object Doesn't Exist", cGrp+" does not exist in the scene. Please select a zPipe and hit Connect Controls")
            else:
                self.P_Amt=int(cGrp[len(cGrp)-7:len(cGrp)-4])
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)
                self.fnGetVariables()

                crvAmt=cmds.getAttr(self.ePHC_Name+".curvature")
                crvLength=cmds.getAttr(self.ePG_Name+".crvLength")
                crvLengthAdd=cmds.getAttr(self.ePG_Name+".crvLengthAdd")
                cmds.setAttr(self.ePG_Name+".crvLength",crvLength+crvLengthAdd)
                cmds.setAttr(self.ePG_Name+".crvLengthAdd", 0)
                if(self.mayaVersion[0:4]=="2014"):
                    cmds.setAttr(self.ePG_Name+".crvAmt",crvAmt)
                else:
                    cmds.setAttr(self.ePG_Name+".crvAmt",math.degrees(crvAmt))

    def fnApplyUIConfig(self):
        self.config["TL_SelectedTab"][2] = cmds.tabLayout(self.tabs,q=True, sti=True)
        #if collapsed frames layouts is on or off!
        if(self.config["FLC_Toggle"][2] == 1):
            #Set all Frame Collapses
            self.config["FLC_MainSliders"][2] = int(cmds.frameLayout( 'FL1' , cl=True, q=True))
            self.config["FLC_QuickSettings"][2] = int(cmds.frameLayout( 'FL3' , cl=True, q=True))
            self.config["FLC_OtherOptions"][2] = int(cmds.frameLayout( 'FL4' , cl=True, q=True))
            self.config["FLC_Settings"][2] = int(cmds.frameLayout( 'FLSettings1' ,cl=True, q=True))
            self.config["FLC_SettingsOtherSwitches"][2] = int(cmds.frameLayout( 'FLSettings3' ,cl=True, q=True))
            self.config["FLC_SettingsQuick"][2] = int(cmds.frameLayout( 'FLSettings2' ,cl=True, q=True))
            # self.config["FLC_CustomMeshList"][2] = int(cmds.frameLayout( 'ASFL1' ,cl=True, q=True))
            self.config["FLC_StarterPipe"][2] = int(cmds.frameLayout( 'FLSettingsStarterPipe2' ,cl=True, q=True))


            
        # cmds.optionMenu('OM01', edit=True, sl=self.Cs_Selected)
        self.config["if_OptimizeThreshold"][2] = cmds.floatField( 'ifPipeOptimize', q=True, v=True)
        self.fnWriteConfig(0)

    def fnApplySettings(self, default):

        self.lsQKSettings[0]= str(cmds.floatField('ffSPipe_qkBend01',q=True, v=True))
        self.lsQKSettings[1]= str(cmds.floatField('ffSPipe_qkBend02',q=True, v=True))
        self.lsQKSettings[2]= str(cmds.floatField('ffSPipe_qkBend03',q=True, v=True))
        self.lsQKSettings[3]= str(cmds.floatField('ffSPipe_qkBend04',q=True, v=True))

        self.lsQKSettings[4]= str(cmds.floatField('ffSPipe_qkRot01',q=True, v=True))
        self.lsQKSettings[5]= str(cmds.floatField('ffSPipe_qkRot02',q=True, v=True))
        self.lsQKSettings[6]= str(cmds.floatField('ffSPipe_qkRot03',q=True, v=True))
        self.lsQKSettings[7]= str(cmds.floatField('ffSPipe_qkRot04',q=True, v=True))
        self.config["rawQKSettings"][2]=','.join(self.lsQKSettings)


        self.config["sldr_subHeight"][2] = cmds.intField( 'ifSPipe_SubHt', v=True,q=True)
        self.config["sldr_subAxis"][2]   = cmds.intField( 'ifSPipe_SubAxis', v=True,q=True)
        self.config["sldr_width"][2]     = cmds.floatField( 'ifSPipe_ScaleXZ',  v=True,q=True)
        self.config["sldr_length"][2] = cmds.floatField( 'ifSPipe_length',  v=True,q=True)
        self.config["sldr_curScale"][2] = cmds.floatField( 'ifSPipe_Scale',  v=True,q=True)
        self.config["sldr_curAmt"][2] = cmds.floatField( 'ifSPipe_CurveAmt',  v=True,q=True)
        self.config["sldr_rotation"][2] = cmds.floatField( 'ifSPipe_Rotate',  v=True,q=True)
        self.config["ff_StarterPipeWidth"][2] = cmds.floatField( 'ffSPipe_MainWidth',  v=True,q=True)
        self.config["ff_StarterPipeSubHeight"][2] = cmds.floatField( 'ffSPipe_MainSubHeight',  v=True,q=True)
        self.config["ff_StarterPipeSubAxis"][2] = cmds.intField( 'ffSPipe_MainSubAxis',  v=True,q=True)
        self.config["ff_StarterPipeScale"][2] = cmds.floatField( 'ffSPipe_MainScale',  v=True,q=True)
        self.config["FLC_Toggle"][2] = int(cmds.checkBox('ckSettings_CollapseMenu',v=True,q=True))
        self.fnDebug('SETTINGS THAT ARE GETTING LOST!!'+str(self.config["ff_StarterPipeWidth"][2]))
        # if(self.ApplySetting_Cs_Selected==1):
            # self.config["Cs_Selected"][2] = cmds.textScrollList('ASTSL1', sii=True, q=True)
            # self.config["Cs_Selected"][2] = self.config["Cs_Selected"][2][0]
        # else:
            # self.config["Cs_Selected"][2] = 1

        #self.fnDebug("Apply Settings")
        self.fnWriteConfig(default)
        self.fnRefreshGUI()

        temp_lsControlGroup=[]
        for cGrp in self.lsControlGroup:
            if(cmds.objExists(cGrp)):
                # self.MP_Amt_Str=self.lsControlGroup[len(self.lsControlGroup)-3:len(self.lsControlGroup)]
                # self.MP_Amt=int(self.MP_Amt_Str)
                temp_lsControlGroup.append(cGrp)
        if not len(temp_lsControlGroup)==0:
            cmds.select(temp_lsControlGroup)
            self.fnConnectControls(0)

    def fnRefreshGUI(self):
        cmds.select(cl=True)

        cmds.deleteUI("zPipeScroll",lay=True)
        self.fnLayout()

    def fnGetConfig(self):
        #self.fnDebug("Try to find Config File")
        # Set Config Dictionary that both read and write will correspond to.

        self.config={
            'scriptConfigVersion':         ['ScriptVersion','Version',self.scriptVersion , self.scriptVersion, 'float'],
            'rawControlGroup':             ['Main_Objects', 'controlGroup','zBendPipe_zgrp001_001','zBendPipe_zgrp001_001','str'],
            'sldr_subAxis':                ['Main_Sliders', 'sldr_subAxis',             20,     20, 'int'],
            'sldr_subHeight':              ['Main_Sliders', 'sldr_subHeight',           30,     30, 'int'],
            'sldr_width':                  ['Main_Sliders', 'sldr_width',               5.0,    5.0, 'float'],
            'sldr_length':                 ['Main_Sliders', 'sldr_length',              2.0,  2.0, 'float'],
            'sldr_curScale':               ['Main_Sliders', 'sldr_curScale',            50.0,  50.0, 'float'],
            'sldr_curAmt':                 ['Main_Sliders', 'sldr_curAmt',              360.0,  360.0, 'float'],
            'sldr_rotation':               ['Main_Sliders', 'sldr_rotation',            360.0,  360.0, 'float'],
            'rawQKSettings':               ['Quick_Settings', 'qkSettings', '90,45,15,0,90,-90,45,-45', '90,45,15,0,90,-90,45,-45','str'],
            'chk_AutoUpdate':              ['Other_Options', 'chk_autoCurveUpdate',    0,   0, 'int'],
            'chk_AutoOptimize':            ['Other_Options', 'chk_autoOptimizePipe',   0,   0, 'int'],
            'if_OptimizeThreshold':        ['Other_Options', 'flt_OptimizeThreshold',  0.35,0.35, 'float'],
            'chk_unfoldFinalPipeUV':       ['Other_Options', 'chk_unfoldFinalPipeUV',  1,   1, 'int'],
            'chk_rememberRotation':        ['Other_Options', 'chk_rememberRotation',   0,   0, 'int'],
            'chk_deleteFinishPipe':        ['Other_Options', 'chk_deleteFinishPipe',   0,   0, 'int'],
            'TL_SelectedTab':              ['Other_Options', 'TL_SelectedTab',         1,   1, 'int'],
            'FLC_SettingsQuick':           ['Other_Options', 'FLC_SettingsQuick',      0,   0, 'int'],
            'FLC_CustomMeshList':          ['Other_Options', 'FLC_CustomMeshList',     0,   0, 'int'],
            'FLC_MainSliders':             ['Other_Options', 'FLC_MainSliders',        0,   0, 'int'],
            'FLC_QuickSettings':           ['Other_Options', 'FLC_QuickSettings',      0,   0, 'int'],
            'FLC_OtherOptions':            ['Other_Options', 'FLC_OtherOptions',       0,   0, 'int'],
            'FLC_Settings':                ['Other_Options', 'FLC_Settings',           0,   0, 'int'],
            'FLC_SettingsOtherSwitches':   ['Other_Options', 'FLC_SettingsOtherSwitches',0, 0, 'int'],
            'FLC_StarterPipe':             ['Other_Options', 'FLC_StarterPipe',        0,   0, 'int'],
            'FLC_Toggle':                  ['Other_Options', 'FLC_Toggle',             0,   0, 'int'],
            'Cs_Name':                     ['Custom_Mesh', 'lst_Cs_Names',             'None','None','str'],
            'Cs_Selected':                 ['Custom_Mesh', 'Cs_Selected',              1,   1,'int'],
            'ff_StarterPipeSubAxis':       ['StarterPipe', 'ff_StarterPipeSubAxis',    12,  12, 'int'],
            'ff_StarterPipeSubHeight':     ['StarterPipe', 'ff_StarterPipeSubHeight' , 5,  5, 'int'],
            'ff_StarterPipeWidth':         ['StarterPipe', 'ff_StarterPipeWidth' ,   3,  3, 'float'],
            'ff_StarterPipeScale':         ['StarterPipe', 'ff_StarterPipeScale' ,   25,  25, 'float']
            }


        if (os.path.exists(self.iniFile)==True):
            #self.fnDebug("Config Already Exists")
            #self.fnReadConfig()
            self.fnReadConfig()
        else:
            #self.fnWriteConfig()
            self.fnWriteConfig(1)

    def fnReadConfig(self):
        #self.fnDebug("reading config file")
        config = ConfigParser.RawConfigParser()
        config.read(self.iniFile)

        # self.scriptConfigVersion = config.get('ScriptVersion', 'Version')
        # if float(self.scriptConfigVersion) <= float(1.6):
            # self.fnError('Outdated Config File', 'Your config file is outdated, at this time the only way to get the script to run is to delete the config file. Sorry :(')
            # sys.exit()
        for cfg in self.config:
            
            try:
                if self.config[cfg][4]=="str":
                    self.config[cfg][2]=str(config.get(self.config[cfg][0], self.config[cfg][1]))
                elif self.config[cfg][4]=="int":
                    self.config[cfg][2]=int(config.get(self.config[cfg][0], self.config[cfg][1]))
                elif self.config[cfg][4]=="float":
                    self.config[cfg][2]=float(config.get(self.config[cfg][0], self.config[cfg][1]))
                self.fnDebug("TRY "+str(self.config[cfg][2])+" "+cfg+" "+self.config[cfg][0]+" "+self.config[cfg][1]+" "+str(self.config[cfg][2]))
            except:
                self.fnDebug("Use Default Values")
                # setattr(self,self.config[cfg][2], config.get(self.config[cfg][0], self.config[cfg][1]))
        # self.+"go"=
        self.lsControlGroup = self.config["rawControlGroup"][2].split(',')
        self.lsQKSettings = self.config["rawQKSettings"][2].split(',')
        self.lsCs_Name = self.config["Cs_Name"][2].split(',')
        if float(self.config["scriptConfigVersion"][2]) < float(self.scriptVersion):
            self.config["scriptConfigVersion"][2]=self.config["scriptConfigVersion"][3]
            #self.scriptConfigVersion = self.scriptVersion
            os.remove(self.iniFile)
            self.fnWriteConfig(0)
        
        if (len(self.lsControlGroup)==0):
            self.config["rawControlGroup"][2] ="zBendPipe_zgrp001_001"
            self.lsControlGroup = self.config["rawControlGroup"][2].split(',')
            

    def fnWriteConfig(self, default):
        if self.skipConfig==0:
            '''WriteFile'''
            #self.fnDebug("Writing config file")
            config = ConfigParser.RawConfigParser()

            config.add_section('ScriptVersion')
            config.add_section('Main_Objects')
            config.add_section('Main_Sliders')
            config.add_section('Quick_Settings')
            config.add_section('Other_Options')
            config.add_section('Custom_Mesh')
            config.add_section('StarterPipe')
            self.fnDebug(self.config)
            for cfg in self.config:
                
                if default==1:
                    self.fnDebug(self.config[cfg][3])
                    self.fnDebug("DEFAULT"+cfg+self.config[cfg][0]+self.config[cfg][1]+str(self.config[cfg][3]))
                    config.set(self.config[cfg][0], self.config[cfg][1], self.config[cfg][3] )
                else:
                    try:
                        self.fnDebug("TRY "+str(self.config[cfg][2])+" "+cfg+" "+self.config[cfg][0]+" "+self.config[cfg][1]+" "+str(self.config[cfg][2]))
                        config.set(self.config[cfg][0], self.config[cfg][1], self.config[cfg][2] )
                    except:
                        try:
                            self.fnDebug("DEFAULT"+cfg+self.config[cfg][0]+self.config[cfg][1]+str(self.config[cfg][2]))
                            config.set(self.config[cfg][0], self.config[cfg][1], self.config[cfg][3] )
                        except:
                            self.fnError('Outdated Config File', 'Your config file is outdated, at this time the only way to get the script to run is to delete the config file. Sorry :(')

            with open(self.iniFile, 'wb') as configfile:
                config.write(configfile)

            if default==1:
                self.fnDebug("REFRESH GUI!")
                self.fnReadConfig()
                self.fnRefreshGUI()
                # self.fnConnectControls(0)

                # self.fnConnectControls(0)
            # self.fnGetConfig()


            '''ReadFile'''

    def fnGetMayaSettings(self):
        mayaUnit=cmds.currentUnit(q=True,l=True)
        self.fnDebug(mayaUnit)
        self.unitMultiplier=1.0
        
        if(mayaUnit=="mm"):
            # self.unitMultiplier=0.1
            self.unitMultiplier=10
        elif(mayaUnit=="cm"):
            self.unitMultiplier=1.0
        elif(mayaUnit=="m"):
            self.unitMultiplier=.01
            #self.unitMultiplier=1.0
        elif(mayaUnit=="in"):
            self.unitMultiplier=0.393701
            #self.unitMultiplier=1.0
        elif(mayaUnit=="ft"):
            self.unitMultiplier=0.0328084
            # self.unitMultiplier=1.0
        elif(mayaUnit=="yd"):
            self.unitMultiplier=0.0109361
            # self.unitMultiplier=1.0
        
        

        self.mayaAxis=cmds.upAxis(q=True,ax=True)


        #self.fnDebug('UNITMULTIPLIER----'+str(self.unitMultiplier))
    
    def fnQuickSettings(self, mode, setting):
        # self.fnWriteConfig(0)
        skipEnd=0
        for cGrp in self.lsControlGroup:
            if not cmds.objExists(cGrp):
                self.fnError("Object Doesn't Exist", cGrp+" does not exist in the scene. Please select a zPipe and hit Connect Controls")
                skipEnd=1
            else:
                doElbowPipe=0
                trimNumber=len("zBendPipe_zgrp")
                self.P_Amt=cGrp
                self.P_Amt=self.P_Amt[trimNumber:trimNumber+3]
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)
                self.P_Amt=int(self.P_Amt)



                nchk=1
                self.fnGetVariables()

                flt_curAmt=cmds.getAttr(self.ePG_Name+".crvAmt")
                flt_rotate=cmds.getAttr(self.ePG_Name+".rotateY")

                if((flt_curAmt)>=0):
                    nchk=1
                else:
                    nchk=-1

                if(mode=='B'):
                    setting=float(setting)
                    if(abs(flt_curAmt)==abs(setting)):
                        doElbowPipe=1
                        #self.fnOptimizePipeCheck()
                    else:
                        cmds.setAttr(self.ePG_Name+".crvAmt", setting*nchk )
                        cmds.select(cl=True)
                elif(mode=='R'):
                    cmds.setAttr(self.ePG_Name+".rotateY", flt_rotate+float(setting) )
                    #self.fnOptimizePipeCheck()
        if skipEnd==0:
            if doElbowPipe==1:
                self.fnElbowPipe("add")

    def fnGetVariables(self):
        self.P_Amt_Str=str(self.P_Amt).zfill(3)
        self.P_Amt_Str_Minus=str(self.P_Amt-1).zfill(3)
        self.P_Amt_Str_Plus=str(self.P_Amt+1).zfill(3)

        self.eP_Name=      "zmBendPipe"+            str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.eP_NameOld=   "zmBendPipe"+            str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        self.ePG_Name=     "zBendPipe_zgrp"+        str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.ePG_Name2=    "zBendPipe_zgrp"+        str(self.P_Amt_Str_Plus)+"_"+self.MP_Amt_Str   
        self.ePG_NameOld=  "zBendPipe_zgrp"+        str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        self.ePH_Name=     "zElbowPipeHistory"+     str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.ePH_NameOld=  "zElbowPipeHistory"+     str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        self.ePHC_Name=    "zElbowPipeHistoryCurve"+str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.ePHC_NameOld= "zElbowPipeHistoryCurve"+str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        self.ePC_Name=     "zElbowPipeCurve"+       str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.ePC_NameOld=  "zElbowPipeCurve"+       str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        self.ePT_Name=     "zElbowPipeTwist"+       str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  
        self.ePHT_Name=    "zElbowPipeHistoryTwist"+str(self.P_Amt_Str)+"_"+self.MP_Amt_Str                  

        #Bend and twist sets (Custom Pipe)
        #self.ePDBS="bend"+str(self.P_Amt)+"Set"
        #self.ePDTS="twist"+str(self.P_Amt)+"Set"
        self.ePCs_Name="zmCBendPipe"+str(self.P_Amt_Str)+"_"+self.MP_Amt_Str
        self.ePCs_NameOld="zmCBendPipe"+str(self.P_Amt_Str_Minus)+"_"+self.MP_Amt_Str
        #Custom Var

    def fnElbowPipe(self, ePCommand):
        self.fnGetMayaSettings()
        temp_lsControlGroup=[]
        # Multi Control Group Time.
        lsMP_Amt=[]
        controlGroup_small=[]
        for cGrp in self.lsControlGroup:
            if not cmds.objExists(cGrp):
                self.lsControlGroup.remove(cGrp)
        if len(self.lsControlGroup)==0:
            self.lsControlGroup=["zBendPipe_zgrp001_001"]
        for cGrp in self.lsControlGroup:
            MP_Amt=cGrp[len(cGrp)-3:len(cGrp)]
            if MP_Amt not in lsMP_Amt:
                lsMP_Amt.append(MP_Amt)
                controlGroup_small.append(cGrp)

        for cGrp in controlGroup_small:
            self.lsControlGroup=[]
            if(cmds.objExists(cGrp)):
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)
            else:
                self.MP_Amt = 1
                self.MP_Amt_Str = str(str(self.MP_Amt).zfill(3))



            #--------------------------------------NEW PIPE----------------------------
            if ePCommand == "new":
                #Make a new pipe.
                #We have to find the newest main pipe number and make it 
                #Start setting up for multiple pipes
                self.MP_Amt = 1
                self.MP_Amt_Str = str(str(self.MP_Amt).zfill(3))
                self.P_Amt=1
                checkAmt=0
                while(checkAmt==0):

                    #Get Variables that we Do for other operations.
                    self.fnGetVariables()
                    if(cmds.objExists(self.ePG_Name)):
                        self.MP_Amt=self.MP_Amt+1
                        self.MP_Amt_Str = str(str(self.MP_Amt).zfill(3))
                    else:
                        checkAmt=1

            #Find Pipe Number now that we have the main number
            self.P_Amt=1
            checkAmt=0
            while(checkAmt==0):

                #Get Variables that we Do for other operations.
                self.fnGetVariables()


                if(cmds.objExists(self.eP_Name)):
                    self.P_Amt=self.P_Amt+1
                else:
                    checkAmt=1
            
            #If there is an existing pipe add on to the end of it.. simple right?
            if(self.P_Amt>>1):


                GSX=cmds.getAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleX')
                GSY=cmds.getAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleY')
                GSZ=cmds.getAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleZ')
                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleX',1)
                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleY',1)
                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleZ',1)

                cmds.select(self.eP_NameOld)

                #----------------Store Old Pipe----------------------------------
                oldP_Amt=self.P_Amt
                self.fnConnectControls(0)
                self.P_Amt=oldP_Amt
                # Swap it back after function is finished
                self.fnGetVariables()

                #Get Variables
                int_subAxis=cmds.intField( 'ifPipe_SubAxis', q=True, v=True)
                int_subHt=cmds.intField( 'ifPipe_SubHt', q=True, v=True)
                int_width=cmds.floatField( 'ifPipe_ScaleXZ', q=True, v=True)
                flt_curScl=cmds.floatField( 'ifPipe_Scale',q=True, v=True)
                flt_curAmt=cmds.getAttr(self.ePG_NameOld+".crvAmt")
                flt_rotate=cmds.floatField( 'ifPipe_Rotate', q=True,v=True)

            #make the cylinder
            cmds.polyCylinder(name=self.eP_Name, r=1, h=2, sx=20, sy=12, rcp=0, cuv=3, ch=1)
            ls_name=cmds.listHistory(pdo=True)
            cmds.rename(ls_name[0], self.ePH_Name)
            cmds.xform(pivots=[0,-1,0])
            cmds.xform(translation=[0,1,0])
            cmds.xform(scale=[1,1*self.unitMultiplier,1])
            cmds.FreezeTransformations()

            #make twist deformer and rename the crap out of it.
            cmds.nonLinear(type='twist',lowBound=0)
            ls_name=cmds.ls(sl=True)
            cmds.rename(ls_name[0], self.ePT_Name)
            historyName01=cmds.listHistory(pdo=True)
            cmds.rename(historyName01[0], self.ePHT_Name)
            cmds.xform(scale=[1,1,1])
            cmds.xform(ws=True,  t=[0,0,0])            

            cmds.select(self.eP_Name)

            #make bend deformer and rename the crap out of it.
            cmds.nonLinear(n=self.ePC_Name,type='bend',lowBound=-1, highBound=1, curvature=0)
            ls_name=cmds.ls(sl=True)
            cmds.rename(ls_name[0], self.ePC_Name)
            historyName01=cmds.listHistory(pdo=True)
            cmds.rename(historyName01[0], self.ePHC_Name)

            cmds.setAttr(self.ePHC_Name+".lowBound",0)

            #Move pivot to correct location
            cmds.xform(scale=[2,2,2])
            cmds.xform(ws=True,  t=[0,0,0])

            cmds.scaleConstraint(self.ePC_Name, self.eP_Name,mo=True, skip=["x","z"], weight=1)
            cmds.scaleConstraint(self.ePC_Name,self.ePT_Name,mo=True, skip=["x","z"], weight=1)

            cmds.group(self.ePC_Name,self.eP_Name,self.ePT_Name,n=self.ePG_Name)

            cmds.addAttr(self.ePG_Name, longName="subAxis",  at="long",  keyable=True, hnv=True, minValue=0)
            cmds.addAttr(self.ePG_Name, longName="subHeight",at="long",  keyable=True)
            cmds.addAttr(self.ePG_Name, longName="width",at="float",  keyable=True)
            cmds.addAttr(self.ePG_Name, longName="crvAmt",      at="float", keyable=True)
            cmds.addAttr(self.ePG_Name, longName="crvLength",   at="float", keyable=True, hnv=True, minValue=0.001)
            cmds.addAttr(self.ePG_Name, longName="crvLengthAdd",at="float", keyable=True)
            cmds.addAttr(self.ePG_Name, longName="optToggle",at="long",  keyable=True)
            cmds.addAttr(self.ePG_Name, longName="optAmt",   at="float", keyable=True, hnv=True, minValue=0.001)

            cmds.expression(n="EXP_Width"+str(self.P_Amt),
                s=self.eP_Name+".scaleX="+self.ePG_Name+".width;"+self.eP_Name+".scaleZ="+self.ePG_Name+".width;",
                ae=0)

            cmds.expression(
                n="EXP_SubAxis"+str(self.P_Amt),
                s="if ("+self.ePG_Name+".subAxis < 3) "+self.ePH_Name+".subdivisionsAxis=3;"
                +"if ("+self.ePG_Name+".subAxis >= 3)"+self.ePH_Name+".subdivisionsAxis="+self.ePG_Name+".subAxis;",
                ae=0,
                uc='all')


            cmds.expression(n="EXP_Curvature"+str(self.P_Amt),
                s="float $ePHC_CLA = "+self.ePG_Name+".crvLengthAdd;"
                +"float $ePHC_CL  = "+self.ePG_Name+".crvLength;"
                +"float $ePHC_CA  = "+self.ePG_Name+".crvAmt;"
                +"if($ePHC_CLA == 0)"
                +"{"+self.ePHC_Name+".curvature=$ePHC_CA*"+str(self.crvMultiplier)+";}"
                +"else"
                +"{"+self.ePHC_Name+".curvature=$ePHC_CA/($ePHC_CL/($ePHC_CL+$ePHC_CLA))*"+str(self.crvMultiplier)+";}",
                ae=0, uc='all')


            cmds.xform(ws=True, pivots=[0,0,0])
            #Curve Length Expression!
            cmds.expression(n="EXP_crvLength"+str(self.P_Amt), s="float $SC = "+self.ePG_Name+".crvLengthAdd + "+self.ePG_Name+".crvLength; "
                +self.ePC_Name+".scaleX = $SC/"+str(self.unitMultiplier)+"; "
                +self.ePC_Name+".scaleY = $SC/"+str(self.unitMultiplier)+"; "
                +self.ePC_Name+".scaleZ = $SC/"+str(self.unitMultiplier)+";",
                ae=0)
            #Twist Expression
            if self.P_Amt >>1:
                twistAdd = self.eP_NameOld+".rotateY"
            else:
                twistAdd = "0"



            cmds.expression(n="EXP_twist"+str(self.P_Amt),
                s="float $int_subAxis = "+self.ePG_Name+".subAxis;"
                +"float $flt_rotate = "+self.ePG_Name+".rotateY;"
                +"float $nchk = 1;"
                +"float $twistAmt02 = 1;"
                +"if ($int_subAxis==0)"
                +"{$int_subAxis=0.001;}"
                +"if($flt_rotate>=0)"
                +"{ $nchk=1; }"
                +"else"
                +"{ $nchk=-1; }"
                +"float $div_subAxis=(360/$int_subAxis);"
                +"float $twistAmt01=abs($flt_rotate)-$div_subAxis;"
                +"float $numMinus=abs($flt_rotate)/$div_subAxis;"
                +"while ($twistAmt01>=$div_subAxis/2)"
                +"{$twistAmt01=abs($flt_rotate)-$div_subAxis;"
                +"$flt_rotate=abs($flt_rotate)-$div_subAxis;}"
                +"if ($twistAmt01<=0)"
                +"{$twistAmt02=($twistAmt01)+$div_subAxis;}"
                +"else"
                +"{$twistAmt02=($twistAmt01)-$div_subAxis;}"
                +"if(abs($twistAmt01)<=abs($twistAmt02))"
                +"{"+self.ePHT_Name+".startAngle = $twistAmt01*$nchk;}"
                +"else"
                +"{"+self.ePHT_Name+".startAngle = $twistAmt02*$nchk;}",
                ae=0)
            #Optimize Expression
            cmds.expression(n="EXP_optimize"+str(self.P_Amt),
                s="float $flt_curAmt=abs("+self.ePG_Name+".crvAmt);"
                +"float $flt_curScl=abs("+self.ePC_Name+".scaleX);"
                +"float $OptAmt="+self.ePG_Name+".optAmt;"
                +"float $flt_curAmtSeg=abs(int($flt_curAmt));"
                +"float $finalSegments=$flt_curAmtSeg;"
                +"if("+self.ePG_Name+".optToggle==0)"
                +"{$finalSegments = "+self.ePG_Name+".subHeight;}"
                +"else if($finalSegments==0)"
                +"{$finalSegments=1;}"
                +"else if($finalSegments<=2)"
                +"{$finalSegments=2;}"
                +"else"
                +"$finalSegments=pow((($flt_curAmtSeg/15)*((((abs($flt_curScl))/(3.14/180)))/($OptAmt/2*15))),$OptAmt/2);"
                +"{$finalSegments=int($finalSegments);}"
                +self.ePH_Name+".subdivisionsHeight = $finalSegments;",
                ae=0)

            if(self.P_Amt>>1):

                cmds.select(self.ePG_NameOld, add=True)
                cmds.parent()
                #Solve For translateX For Auto Curve Snap
                if(self.mayaVersion[0:4]=="2014"):
                    cmds.expression(n="EXP_TransX"+str(self.P_Amt),
                        s="if("+self.ePG_NameOld+".crvAmt==0) "
                        +self.ePG_Name+".translateX = 0; "
                        +"else"
                        +" { float $X1 =((((360/"+self.ePHC_NameOld+".curvature)*"+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+")/3.141592654)/2);"
                        +" float $X2 = cos(deg_to_rad("+self.ePHC_NameOld+".curvature))*$X1; "
                        +self.ePG_Name+".translateX = $X1 - $X2;}",
                        ae=0)
                else:
                    cmds.expression(n="EXP_TransX"+str(self.P_Amt),
                        s="if("+self.ePG_NameOld+".crvAmt==0) "
                        +self.ePG_Name+".translateX = 0;"
                        +" else"
                        +" { float $X1 =((((360/rad_to_deg("+self.ePHC_NameOld+".curvature))*"+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+")/3.141592654)/2);"
                        +" float $X2 = cos("+self.ePHC_NameOld+".curvature)*$X1;"
                        +self.ePG_Name+".translateX = $X1 - $X2;}",
                        ae=0)

                #Solve For translateY For Auto Curve Snap
                if(self.mayaVersion[0:4]=="2014"):
                    cmds.expression(n="EXP_TransY"+str(self.P_Amt),
                        s="if("+self.ePG_NameOld+".crvAmt==0) "
                        +self.ePG_Name+".translateY = "+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+";"
                        +" else { float $X1 =((((360/"+self.ePHC_NameOld+".curvature)*"+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+")/3.141592654)/2); "
                        +self.ePG_Name+".translateY = sin(deg_to_rad("+self.ePHC_NameOld+".curvature))*$X1;}",
                        ae=0)
                else:
                    cmds.expression(n="EXP_TransY"+str(self.P_Amt),
                        s="if("+self.ePG_NameOld+".crvAmt==0) "
                        +self.ePG_Name+".translateY = "+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+"; "
                        +"else"
                        +" { float $X1 =((((360/rad_to_deg("+self.ePHC_NameOld+".curvature))*"+self.ePC_NameOld+".scaleY*"+str(self.unitMultiplier)+")/3.141592654)/2); "
                        +self.ePG_Name+".translateY = sin("+self.ePHC_NameOld+".curvature)*$X1;}",
                        ae=0)
                if(self.mayaVersion[0:4]=="2014"):
                    cmds.expression(n="EXP_rotateYZ"+str(self.P_Amt), s=self.ePG_Name+".rotateZ="+self.ePHC_NameOld+".curvature*-1;",ae=0)
                else:
                    cmds.expression(n="EXP_rotateYZ"+str(self.P_Amt), s=self.ePG_Name+".rotateZ=rad_to_deg("+self.ePHC_NameOld+".curvature)*-1;",ae=0)

                cmds.setAttr(self.ePG_Name+".translateZ", 0)
                cmds.setAttr(self.ePG_Name+".rotateX", 0)
                cmds.setAttr(self.ePG_Name+".rotateY", 0 )
                cmds.setAttr(self.ePG_Name+".subAxis", int_subAxis )
                cmds.setAttr(self.ePG_Name+".subHeight", int_subHt )


                cmds.setAttr(self.ePC_Name+".visibility", 0)
                cmds.setAttr(self.ePT_Name+".visibility", 0)

                cmds.setAttr(self.ePG_Name+".width", int_width )
                # cmds.setAttr(self.eP_Name+".scaleZ", int_width )
                cmds.setAttr(self.ePG_Name+".crvLength", flt_curScl )
                cmds.setAttr(self.ePG_Name+".crvAmt", flt_curAmt )
                if self.config["chk_rememberRotation"][2]==1:
                    cmds.setAttr(self.ePG_Name+".rotateY", flt_rotate )
                cmds.setAttr(self.ePG_Name+".optAmt", cmds.getAttr(self.ePG_NameOld+".optAmt"))
                cmds.setAttr(self.ePG_Name+".optToggle", cmds.getAttr(self.ePG_NameOld+".optToggle"))

                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleX',GSX)
                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleY',GSY)
                cmds.setAttr('zBendPipe_zgrp001_'+self.MP_Amt_Str+'.scaleZ',GSZ)

                temp_lsControlGroup.append(self.eP_Name)

                
                if not ePCommand == "dupAdd":
                    if(cmds.objExists(self.ePCs_NameOld)):
                        customPipe=cmds.addAttr(self.ePCs_NameOld+".CsName", q=True, en=True)
                        self.fnCustomElbowPipe(customPipe)

                # cmds.select(self.ePC_Name,self.ePT_Name)
                # cmds.HideSelectedObjects()

            else:
                cmds.setAttr(self.ePG_Name+".subAxis", self.config['ff_StarterPipeSubAxis'][2] )
                cmds.setAttr(self.ePG_Name+".subHeight", self.config['ff_StarterPipeSubHeight'][2] )
                cmds.setAttr(self.ePG_Name+".width", self.config['ff_StarterPipeWidth'][2] )
                # cmds.setAttr(self.eP_Name+".scaleZ", 20 )
                cmds.setAttr(self.ePG_Name+".crvLength", self.config['ff_StarterPipeScale'][2] )
                cmds.setAttr(self.ePG_Name+".crvAmt", 0 )
                cmds.setAttr(self.ePG_Name+".rotateY", 0 )
                cmds.setAttr(self.ePG_Name+".optAmt", self.config["if_OptimizeThreshold"][2])
                cmds.setAttr(self.ePG_Name+".optToggle", self.config["chk_AutoOptimize"][2])
                cmds.setAttr(self.ePC_Name+".visibility", 0)
                cmds.setAttr(self.ePT_Name+".visibility", 0)

                if(self.mayaAxis=="z"):
                    #self.fnDebug("DO STUFF!!!-- ")
                    cmds.setAttr(self.ePG_Name+".rotateX", 90)

                

                temp_lsControlGroup.append(self.eP_Name)           
            

            #------------------------Store Old Pipe------------------------------
        self.lsControlGroup=temp_lsControlGroup
        cmds.select(temp_lsControlGroup)
        self.fnConnectControls(0)

    def fnConnectControls(self, selGrp):
        # self.selCusMesh = cmds.textScrollList('ASTSL1',q=True,selectItem=True)
        #Remember when throwing shit at this function to select an object first
        selPipesRaw=cmds.ls(sl=True, et="transform")
        selPipes=[]
        startCCommand=1
        for sel in selPipesRaw:
            if "zmBend" in sel or "zmCBend" in sel or "zBend" in sel:
                selPipes.append(sel)
        if len(selPipes)==0:
            selPipes=self.lsControlGroup
            if len(self.lsControlGroup)==0:
                startCCommand=0


        if startCCommand == 1:

            self.lsControlGroup=[]
            list_F_PipeSubAxis=[]
            list_F_Width=[]
            list_F_ePName_SH=[]
            list_F_ePName_OA=[]
            list_F_ePName_OT=[]
            list_F_ePGName_RY=[]
            list_F_ePHCName_CL=[]
            list_F_ePHCName_CA=[]
            list_F_ePHCName_CLA=[]

            for cindex in range(0,len(selPipes)):

                self.P_Amt=selPipes[cindex]
                #self.fnDebug(self.P_Amt)
                if("zBe" in self.P_Amt):
                    trimNumber=len("zBendPipe_zgrp")
                elif("zmB" in self.P_Amt):
                    trimNumber=len("zmBendPipe")
                    #self.fnDebug("YES")
                elif("zmC" in self.P_Amt):
                    trimNumber=len("zmCBendPipe")

                self.MP_Amt_Str=self.P_Amt[len(self.P_Amt)-3:len(self.P_Amt)]
                self.MP_Amt=int(self.MP_Amt_Str)

                cmds.select("zmBend*"+"*_"+self.MP_Amt_Str)
                list_zPipes=cmds.ls(sl=True,et="transform")
                P_Amt02=len(list_zPipes)

                cmds.select(self.P_Amt)

                #self.fnDebug(self.P_Amt[trimNumber:trimNumber+3])
                self.P_Amt=int(self.P_Amt[trimNumber:trimNumber+3])
                self.fnGetVariables()

                numPipes=1
                list_PipeSubAxis=[]
                list_Width=[]
                # list_Optimize=[]
                # list_OptToggle=[]
                for index in range(0,P_Amt02):
                    list_PipeSubAxis.append("zBendPipe_zgrp"+str(numPipes).zfill(3)+"_"+self.MP_Amt_Str+".subAxis")
                    list_Width.append("zBendPipe_zgrp"+str(numPipes).zfill(3)+"_"+self.MP_Amt_Str+".width")
                    numPipes=numPipes+1

                for index in list_PipeSubAxis:
                    if index not in list_F_PipeSubAxis:
                        list_F_PipeSubAxis.append(index)

                for index in list_Width:
                    if index not in list_F_Width:
                        list_F_Width.append(index)

                list_F_ePName_SH.append(self.ePG_Name+".subHeight")
                list_F_ePGName_RY.append(self.ePG_Name+".rotateY")
                list_F_ePHCName_CL.append(self.ePG_Name+".crvLength")
                list_F_ePHCName_CA.append(self.ePG_Name+".crvAmt")
                list_F_ePHCName_CLA.append(self.ePG_Name+".crvLengthAdd")

                list_F_ePName_OA.append(self.ePG_Name+".optAmt")
                list_F_ePName_OT.append(self.ePG_Name+".optToggle")

                self.lsControlGroup.append(self.ePG_Name)
                



            cmds.connectControl( 'slPipe_SubAxis', list_F_PipeSubAxis)
            cmds.connectControl( 'ifPipe_SubAxis', list_F_PipeSubAxis)
            cmds.connectControl( 'slPipe_SubHt', list_F_ePName_SH)
            cmds.connectControl( 'ifPipe_SubHt', list_F_ePName_SH)
            cmds.connectControl( 'slPipe_ScaleXZ', list_F_Width)
            cmds.connectControl( 'ifPipe_ScaleXZ', list_F_Width)
            cmds.connectControl( 'slPipe_Scale', list_F_ePHCName_CL)
            cmds.connectControl( 'ifPipe_Scale', list_F_ePHCName_CL)
            cmds.connectControl( 'slPipe_CurveAmt', list_F_ePHCName_CA)
            cmds.connectControl( 'ifPipe_CurveAmt', list_F_ePHCName_CA)
            cmds.connectControl( 'slPipe_Rotate', list_F_ePGName_RY)
            cmds.connectControl( 'ifPipe_Rotate', list_F_ePGName_RY)
            cmds.connectControl( 'slPipe_Length', list_F_ePHCName_CLA)
            cmds.connectControl( 'ifPipe_Length', list_F_ePHCName_CLA)
            cmds.connectControl( 'ifPipeOptimize', list_F_ePName_OA)
            cmds.connectControl( 'ckAutoOptimize', list_F_ePName_OT)

            cmds.select(self.lsControlGroup)
            
            self.config["rawControlGroup"][2]=','.join(self.lsControlGroup)
            self.fnDebug(self.lsControlGroup)
            # self.MP_Amt_Str=self.ePG_Name[len(self.lsControlGroup)-3:len(self.lsControlGroup)]
            # self.MP_Amt=int(self.MP_Amt_Str)
            self.fnWriteConfig(0)

        else:
            cmds.confirmDialog( title='Outdated Config File', 
                message='Cannot Connect Controls. Please try selecting an object on the zPipe chain and try again.', 
                button=['Ok'], 
                defaultButton='Ok', 
                cancelButton='No', 
                dismissString='No') 

    def fnOptimizePipe(self, optCommand):

        optAmt=cmds.floatField( 'ifPipeOptimize', q=True, v=True)
        #-----------------------------------ALL-------------------------------------
        if(optCommand=="ALL"):
            controlGroup_small=[]
            lsMP_Amt=[]
            # Minimize Control group down to only unique Main Pipe Amount
            for cGrp in self.lsControlGroup:
                MP_Amt=cGrp[len(cGrp)-3:len(cGrp)]
                if MP_Amt not in lsMP_Amt:
                    lsMP_Amt.append(MP_Amt)
                    controlGroup_small.append(cGrp)
            # Throw the minimized list into a for loop that only works if the object exists in the first place.
            for cGrp in controlGroup_small:
                if(cmds.objExists(cGrp)):
                    self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                    self.MP_Amt=int(self.MP_Amt_Str)

                    cmds.select("zBend*"+"_*"+self.MP_Amt_Str)
                    list_zPipesAll=cmds.ls(sl=True,et="transform")
                    selPipe=list_zPipesAll[-1]
                    trimNumber=len("zBendPipe_zgrp")
                    self.P_Amt=selPipe
                    self.P_Amt=int(self.P_Amt[trimNumber:trimNumber+3])

                    for index in range(0,self.P_Amt):
                        self.P_Amt=index+1
                        self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]

                        self.fnGetVariables()
                        cmds.setAttr(self.ePG_Name+".optAmt", optAmt)
                        #optToggle=cmds.getAttr("zmBendPipe"+str(index)+".optToggle")
                        cmds.setAttr(self.ePG_Name+".optToggle",1)
                        cmds.setAttr(self.ePG_Name+".subHeight", cmds.getAttr(self.ePH_Name+".subdivisionsHeight"))
                        cmds.setAttr(self.ePG_Name+".optToggle", self.config["chk_AutoOptimize"][2])
        #------------------------------------Control--------------------------------
        if(optCommand=="CONTROL"):
            for cGrp in self.lsControlGroup:
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)

                trimNumber=len("zBendPipe_zgrp")
                self.P_Amt=int(cGrp[trimNumber:trimNumber+3])
                self.fnGetVariables()
                cmds.setAttr(self.ePG_Name+".optAmt", optAmt)
                cmds.setAttr(self.ePG_Name+".optToggle",1)
                cmds.setAttr(self.ePG_Name+".subHeight", cmds.getAttr(self.ePH_Name+".subdivisionsHeight"))
                cmds.setAttr(self.ePG_Name+".optToggle",self.config["chk_AutoOptimize"][2])
        #------------------------------------CheckBox--------------------------------
        if(optCommand=="CHECKBOX"):
            for cGrp in self.lsControlGroup:
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)

                trimNumber=len("zBendPipe_zgrp")
                self.P_Amt=int(cGrp[trimNumber:trimNumber+3])
                self.fnGetVariables()
                cmds.setAttr(self.ePG_Name+".optAmt", optAmt)
                cmds.setAttr(self.ePG_Name+".optToggle",1)
                cmds.setAttr(self.ePG_Name+".subHeight", cmds.getAttr(self.ePH_Name+".subdivisionsHeight"))
                cmds.setAttr(self.ePG_Name+".optToggle",0)

        cmds.select(self.lsControlGroup)

    def fnFinishPipe(self):
        # self.config["chk_deleteFinishPipe"][2]=0
        selPipes=cmds.ls(sl=True)
        if len(selPipes)==0:
            selPipes=self.lsControlGroup
        fp_Name_All=[]
        lsMP_Amt=[]
        controlGroup_small=[]
        for cGrp in selPipes:
            MP_Amt=cGrp[len(cGrp)-3:len(cGrp)]
            if MP_Amt not in lsMP_Amt:
                lsMP_Amt.append(MP_Amt)
                controlGroup_small.append(cGrp)

        for cGrp in controlGroup_small:
            if(cmds.objExists(cGrp)):
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)

            unfold=cmds.checkBox('ckFinishPipeUnfold',q=True,v=True)
            #Get Main Group Transforms

            gTX=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateX")
            gTY=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateY")
            gTZ=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateZ")
            gRX=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateX")
            gRY=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateY")
            gRZ=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateZ")
            gSX=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleX")
            gSY=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleY")
            gSZ=cmds.getAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleZ")
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateX",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateY",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateZ",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateX",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateY",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateZ",0)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleX",1)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleY",1)
            cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleZ",1)

            #Start the Finish Pipe Process By Duplicating the pipes,
            #unparent them and delete the extra scale transforms.
            #Then delete caps, combine, merge and create uv's.
            if cmds.objExists("zmCBendPipe001_"+self.MP_Amt_Str):
                #self.fnDebug("DO SHIT")
                cmds.select("zmCBend*"+"*_"+self.MP_Amt_Str+"*")
                cmds.duplicate(rr=True)
                list_zPipes=cmds.ls(sl=True,et="transform")
                list_zScale=cmds.ls(sl=True,et="scaleConstraint")
                #self.fnDebug(list_zPipes)
                #self.fnDebug(list_zScale)

                cmds.select(list_zScale)
                cmds.delete()
                cmds.select(list_zPipes)
                cmds.parent(w=True)
                cmds.select(cl=True)

                P_Amt=1
                checkAmt=0
                while(checkAmt==0):
                    fp_Name="FinishPipe"+str(P_Amt)
                    if(cmds.objExists(fp_Name)):
                        P_Amt=P_Amt+1
                    else:
                        checkAmt=1
                fp_Name="FinishPipe"+str(P_Amt)

                cmds.polyUnite( list_zPipes, n=fp_Name,ch=False )
                cmds.polyMergeVertex(fp_Name+".vtx[0:500000000]",d=0.5 ,am=1,ch=1)
                cmds.select(list_zPipes)
                cmds.delete()

                fp_Name_All.append(fp_Name)
                cmds.select(fp_Name)
                cmds.xform( ro=[gRX,gRY,gRZ], t=[gTX,gTY,gTZ], scale=[gSX,gSY,gSZ])
                #DO Custom Mesh Operations instead of default pipe operations.
            else:

                cmds.select("zmBend*"+"*_"+self.MP_Amt_Str+"*")
                self.fnDebug(self.MP_Amt_Str)

                # cmds.select("zmCBend*"+"*_"+self.MP_Amt_Str)
                cmds.duplicate(rr=True)
                

                list_zPipes=cmds.ls(sl=True,et="transform")
                list_zScale=cmds.ls(sl=True,et="scaleConstraint")

                cmds.select(list_zScale)
                cmds.delete()
                cmds.select(list_zPipes)
                cmds.parent(w=True)
                cmds.select(cl=True)


                for index in range(0,len(list_zPipes)):
                    int_subAxis=cmds.getAttr("zElbowPipeHistory"+str(index+1).zfill(3)+"_"+self.MP_Amt_Str+".subdivisionsAxis")
                    int_subHt=cmds.getAttr("zElbowPipeHistory"+str(index+1).zfill(3)+"_"+self.MP_Amt_Str+".subdivisionsHeight")
                    int_selFace=int_subAxis*int_subHt
                    cmds.select(list_zPipes[index]+"Shape.f["+str(int_selFace)+"]", add=True)
                    cmds.select(list_zPipes[index]+"Shape.f["+str(int_selFace+1)+"]", add=True)
                    if(index==0):
                        eAmt=((int_subHt+1)*int_subAxis)
                cmds.delete()

                P_Amt=1
                checkAmt=0
                while(checkAmt==0):
                    fp_Name="FinishPipe"+str(P_Amt)
                    if(cmds.objExists(fp_Name)):
                        P_Amt=P_Amt+1
                    else:
                        checkAmt=1
                cmds.polyUnite( list_zPipes, n=fp_Name,ch=False )
                cmds.polyMergeVertex(fp_Name+".vtx[0:5000000]",d=0.5 ,am=1,ch=1)
                cmds.select(fp_Name)
                cmds.polyForceUV(unitize=True)
                cmds.select(list_zPipes)
                cmds.delete()


                eAmt=eAmt+1
                cmds.select(fp_Name+".e["+str(eAmt)+"]")
                cmds.polySelectSp( loop=True)

                #self.fnDebug(eAmt)
                cmds.select(fp_Name+".e[0:50000000]", tgl=True)
                cmds.polyMapSewMove(nf=10, lps=0, ch=1)
                #cmds.polyLayoutUV()
                if(unfold==1):
                    cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=1)
                cmds.select(fp_Name+".e[0:50000000]")
                cmds.polySoftEdge(a=180, ch=1)
                cmds.polyLayoutUV()
                    

                fp_Name_All.append(fp_Name)

                cmds.select(fp_Name)
                cmds.xform( ro=[gRX,gRY,gRZ], t=[gTX,gTY,gTZ], scale=[gSX,gSY,gSZ])
            if self.config["chk_deleteFinishPipe"][2]==0:
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateX",gTX)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateY",gTY)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".translateZ",gTZ)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateX",gRX)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateY",gRY)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".rotateZ",gRZ)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleX",gSX)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleY",gSY)
                cmds.setAttr("zBendPipe_zgrp001_"+self.MP_Amt_Str+".scaleZ",gSZ)
            else:
                cmds.delete("zBendPipe_zgrp001_"+self.MP_Amt_Str)

            #Reapply Main Group Transforms

        cmds.select(fp_Name_All)

    def fnDebug(self, printCmd):
        #takes in a #self.fnDebug command that will be only displayed in debug mode.zPipeMaker
        if self.debugMode == 1:
            print(printCmd)

    def fnProgress(self, progTitle, status, command):
        if command == "start":
            self.progressAmount = 0
            cmds.progressWindow(title=progTitle,
                progress=self.progressAmount,
                status=status,
                isInterruptable=True )

        if command == "edit":
            cmds.progressWindow( edit=True, progress=self.progressAmount, status=status )

        if command == "end":
            cmds.progressWindow( endProgress=1)

    def fnError(self, title, message):
            cmds.confirmDialog( title=title, message=message, 
                button=['Ok'], 
                defaultButton='Ok', 
                cancelButton='No', 
                dismissString='No' )

    def fnDuplicate(self):
       
        # Duplicate and rename EVERYTHING!
        selPipesRaw=cmds.ls(sl=True)
        selPipes=[]
        selectFinal=[]
        # If selected Pipes is 0 move on to the control group.
        if len(selPipesRaw)==0:
            selPipes=self.lsControlGroup
        else:
            # Filter out non zPipes
            for sel in selPipesRaw:
                if "zmBend" in sel or "zmCBend" in sel or "zBend" in sel:
                    selPipes.append(sel)
        lsMP_Amt=[]
        controlGroup_small=[]
        # Minimize Control group down to only unique Main Pipe Amount
        for cGrp in selPipes:
            MP_Amt=cGrp[len(cGrp)-3:len(cGrp)]
            if MP_Amt not in lsMP_Amt:
                lsMP_Amt.append(MP_Amt)
                controlGroup_small.append(cGrp)
        # Throw the minimized list into a for loop that only works if the object exists in the first place.
        for cGrp in controlGroup_small:

            self.progressAmount=0
            self.fnProgress( "Duplicating Pipes", "Duplicating"+cGrp, "start")

            if(cmds.objExists(cGrp)):
                stopErrors=0
                self.MP_Amt_Str=cGrp[len(cGrp)-3:len(cGrp)]
                self.MP_Amt=int(self.MP_Amt_Str)
                # Because Duplicate un=True doesn't work well with the renaming process of everything.. 
                # the only other option is to recreate the pipe.. which may be even faster than duplicate. We shall see


                cmds.select("zBend*"+"*_"+self.MP_Amt_Str)
                zGrpPipes=cmds.ls(sl=True, et="transform")
                tN=len("zBendPipe_zgrp")

                zGrpPipesDict = {'translateX':[],'translateY':[],'translateZ':[],'rotateX':[],'rotateY':[],'rotateZ':[],'scaleX':[],'scaleY':[],'scaleZ':[],
                    'subAxis':[],'subHeight':[],'width':[],'crvAmt':[],'crvLength':[],'crvLengthAdd':[],'optToggle':[],'optAmt':[]}
                setAttrList=["translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ",
                    "subAxis","subHeight","width","crvAmt","crvLength","crvLengthAdd","optToggle","optAmt"]
                setAttrList02=["translateZ","rotateX","rotateY","scaleX","scaleY","scaleZ",
                    "subAxis","subHeight","width","crvAmt","crvLength","crvLengthAdd","optToggle","optAmt"]
                # Setup everything to be stored in a dictionary so that we can easily run through a for loop.
                for zGrp in zGrpPipes:
                    self.P_Amt_Str=zGrp[tN:tN+3]
                    self.P_Amt=int(self.P_Amt_Str)
                    # print(zGrp)
                    # print self.P_Amt
                    self.fnGetVariables()
                    # print(self.ePG_Name)
                    # Check for new name. 
                    for attr in setAttrList:
                        if attr=="CsName":
                            if cmds.objExists(self.ePCs_Name):
                                zGrpPipesDict[attr].append(cmds.addAttr(self.ePCs_Name+"."+attr, q=True, en=True))
                            else:
                                zGrpPipesDict[attr].append("None")
                        else:
                            zGrpPipesDict[attr].append(cmds.getAttr(self.ePG_Name+"."+attr))
                    self.progressAmount=self.progressAmount+(10.0/len(setAttrList))
                    self.fnProgress( "Duplicating Pipes", "Duplicating "+cGrp, "edit")
                        

                # print zGrpPipesDict
                # lsCPipeError=[]
                # for cPipe in zGrpPipesDict["CsName"]:
                    # if cPipe not in lsCPipeError:
                        # lsCPipeError.append(cPipe)
                # for cPipe in lsCPipeError:
                    # if not cmds.objExists(cPipe):
                        # if not cPipe=="None":
                            # self.fnError(cPipe+" Does not Exist", cPipe+" cannot be located. Are you sure that you didn't delete it or rename it?")
                            # stopErrors=1
# 
                # SLitems=cmds.textScrollList('ASTSL1', q=True, ai=True)
                # for item in lsCPipeError:
                    # if item not in SLitems:
                        # if not item=="None":
                            # self.fnError(item+" Does not Exist", item+" is not in the custom mesh list. Please go to the Advanced tab and add it using the custom mesh list editor.")
                            # stopErrors=1

                # Now that we have our dictionary. Lets recreate this bitch.
                if stopErrors==1:
                    self.progressAmount=100
                    self.fnProgress( "Duplicating Error", "Error", "end")
                else:
                    counter=1

                    for index in range(len(zGrpPipes)):
                        if counter ==1:
                            self.fnElbowPipe("new")
                            selectFinal.append("zBendPipe_zgrp001_"+self.MP_Amt_Str)
                            # print self.MP_Amt_Str
                            for attr in setAttrList:
                                # first Pipe needs location
                                if attr =="CsName":
                                    if not zGrpPipesDict[attr][index] == "None":
                                        # Jenky ass way of replacing the custom pipe!
                                        cmds.textScrollList('ASTSL1', edit=True, da=True)
                                        cmds.textScrollList('ASTSL1', edit=True, selectItem=zGrpPipesDict[attr][index])
                                        cmds.tabLayout('tabMain',edit=True,selectTabIndex=2 )
                                        cmds.tabLayout('tabMain',edit=True,selectTabIndex=1 )
                                        cmds.select(self.eP_Name)
                                        self.fnCustomSLCmds("replace")
                                        cmds.select(cl=True)
                                else:
                                    cmds.setAttr(self.ePG_Name+"."+attr, zGrpPipesDict[attr][index])
                                    
                        else:
                            self.fnElbowPipe("dupAdd")
                            # second pipe doesn't need location. therefore we have 2 lists.
                            for attr in setAttrList02:
                                if attr =="CsName":
                                    if not zGrpPipesDict[attr][index] == "None":
                                        cmds.textScrollList('ASTSL1', edit=True, da=True)
                                        cmds.textScrollList('ASTSL1', edit=True, selectItem=zGrpPipesDict[attr][index])
                                        cmds.tabLayout('tabMain',edit=True,selectTabIndex=2 )
                                        cmds.tabLayout('tabMain',edit=True,selectTabIndex=1 )
                                        cmds.select(self.eP_Name)

                                        self.fnCustomSLCmds("replace")
                                        cmds.select(cl=True)
                                else:

                                
                                    cmds.setAttr(self.ePG_Name+"."+attr, zGrpPipesDict[attr][index])

                        self.progressAmount=self.progressAmount+(90.0/len(zGrpPipes))
                        self.fnProgress("Duplicating Pipes", "Duplicating "+cGrp,"edit")


                        counter=counter+1
                    self.progressAmount=100
                    self.fnProgress( "Duplicating Finished", "Completed", "end")
                        # print counter

            if stopErrors==0:
                cmds.select(selectFinal)
            else:
                cmds.select(cl=True)


            

def gui(*arg):
    zPipeMaker()

