SET COMMONPATH=%~dp0
%COMMONPATH%pyrcc4.exe %COMMONPATH%\icons\IconResource.qrc  -o %COMMONPATH%IconResource_rc.py
%COMMONPATH%pyrcc4.exe %COMMONPATH%\icons\test.qrc  -o %COMMONPATH%test_rc.py