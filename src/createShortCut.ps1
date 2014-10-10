$Root = $P()SScriptRoot;

function createMayaShortCut($version)
{
        $appPath = ""

        if ($version -eq "2014")
        {
            $appPath = (Get-ItemProperty -Path HKLM:\SOFTWARE\Autodesk\Maya\2014\Setup\InstallPath -Name MAYA_INSTALL_LOCATION).MAYA_INSTALL_LOCATION
        }
        if ($version -eq '2015')
        {
            $appPath = (Get-ItemProperty -Path HKLM:\SOFTWARE\Autodesk\Maya\2015\Setup\InstallPath -Name MAYA_INSTALL_LOCATION).MAYA_INSTALL_LOCATION
        }
}

function createMaxShortCut($version)
{
        $appPath = ""

        if ($version -eq "2014")
        {
            $appPath = (Get-ItemProperty -Path HKLM:\SOFTWARE\Autodesk\3dMax\16.0 -Name MAYA_INSTALL_LOCATION).installdir
        }
        if ($version -eq '2015')
        {
            $appPath = (Get-ItemProperty -Path HKLM:\SOFTWARE\Autodesk\3dsMax\17.0\ -Name MAYA_INSTALL_LOCATION).installdir
        }   
        $WshShell = New-Object -ComObject WScript.Shell;
        $WshShell.CreateShortCut($Root)
}


function createShortCutApplication ( $app, $version)
{
    $WshShell = New-Object -ComObject WScript.Shell;

    $appPath = ""
    if ($app -eq "maya")
    {
        createMayaShortCut($version)   
    }
    if ($app -eq "3dsMax")
    {
        createMaxShortCut($version)   
    }

}

createShortCutApplication("maya", "2014")