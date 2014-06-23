@echo off
ECHO 1: press 1 if you would like to run with Maya 2011
ECHO 2: press 2 if you would like to run with Maya 2012
ECHO 3: press 3 if you would like to run with Maya 2013
ECHO 4: press 4 if you would like to run with Maya 2014
ECHO 5: press 5 if you would like to run with Maya 2015


CHOICE /N /C 12345 /M "Enter Maya version:"
IF %ERRORLEVEL% == 1 SET MAYAVERSION=2011
IF %ERRORLEVEL% == 2 SET MAYAVERSION=2012
IF %ERRORLEVEL% == 3 SET MAYAVERSION=2013.5
IF %ERRORLEVEL% == 4 SET MAYAVERSION=2014
IF %ERRORLEVEL% == 5 SET MAYAVERSION=2015

REM #### Set up paths for Maya working properly ### 
REM #### Get This script path

SET COMMONPATH=%~dp0

SET PROJECT_DIR=%COMMONPATH%developer\projects\
 
REM ### Set Python path
SET PYTHONPATH=%COMMONPATH%MAYA_%MAYAVERSION%\;%COMMONPATH%;%PYTHONPATH%
SET MAYA_SCRIPT_PATH=%COMMONPATH%;%MAYA_SCRIPT_PATH%

set MAYA_LAUNCHER=%PROGRAMFILES%\AUTODESK\maya%MAYAVERSION%

REM use call to enter debug mode and see errors out put from cmd
REM call %COMMONPATH%"Maya "%MAYAVERSION%"-internalTools.lnk"

start %COMMONPATH%"Maya "%MAYAVERSION%"-internalTools.lnk"
