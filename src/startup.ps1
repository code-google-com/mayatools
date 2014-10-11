$Root = $PSScriptRoot;

Function getNumberMaya()
{
    $out = @{}
    (Get-ChildItem -Path HKLM:\SOFTWARE\Autodesk\Maya\ -Recurse )|
    ForEach-Object{
        if ($_.Name.Contains("InstallPath"))
        {
            $p = $_.GetValue("MAYA_INSTALL_LOCATION")
            $out.Add($p.Split("\")[3], $p)
        }
    }
    return $out
}

Function getNumberMax()
{
    $out = @{}
    (Get-ChildItem -Path HKLM:\SOFTWARE\Autodesk\3dsMax\)|
    ForEach-Object{
       Try
       {
            $p = $_.GetValue("installdir")
            $out.Add($p.Split("\")[3], $p)
       }
       Catch{
            $ErrorMessage = $_.Exception.Message
            $ErrorMessage
       }

    }
    return $out 
}

function setEnvPathMaya($version)
{
    $env:PROJECT_DIR = $Root + "\developer\"
    $env:PYTHONPATH += ";" + $Root + "\" + $version + ";" + $Root
    $env:MAYA_SCRIPT_PATH += ";" + $Root
    if ($version -eq "Maya2015")
    {
        $env:MAYA_MODULE_PATH += ";" + $Root + "\" + $version + "\FabricSpliceMaya2015SP2"
    }
    if ($version -eq "Maya2014")
    {
        $env:MAYA_MODULE_PATH +=  ";" + $Root + "\" + $version + "\FabricSpliceMaya2014SP3"
    }
}

function execMaya($item)
{
        setEnvPathMaya($item.Name)
        & ($item.Value + 'bin\maya.exe') -c 'python(\"import startup_on_maya\")'
}

function execMax($item)
{
        #setEnvPathMaya($item.Name)
        & ($item.Value + '\3dsmax.exe') #-c 'python(\"import startup_on_maya\")'
}

function showWindow()
{
    Add-Type -AssemblyName System.Windows.Forms
    $Form = New-Object System.Windows.Forms.Form
    $numMaya = getNumberMaya
    $numMax = getNumberMax
    $xpos = 0; $ypos = 0
    foreach($item in $numMaya.GetEnumerator())
    {

        $button = New-Object System.Windows.Forms.Button
        $button.Location = New-Object System.Drawing.Point($xpos, $ypos)
        $button.Size = New-Object System.Drawing.Size(100, 100)
        $button.add_Click({execMaya($item)}.GetNewClosure())
        $button.Text = $item.Name
        $Form.Controls.Add($button)
        $ypos += 120
    }

    $xpos = 120; $ypos = 0

    foreach($item in $numMax.GetEnumerator())
    {

        $button = New-Object System.Windows.Forms.Button
        $button.Location = New-Object System.Drawing.Point($xpos, $ypos)
        $button.Size = New-Object System.Drawing.Size(100, 100)
        $button.add_Click({execMax($item)}.GetNewClosure())
        $button.Text = $item.Name
        $Form.Controls.Add($button)
        $ypos += 120
    }
    $Form.StartPosition = "CenterScreen"
    # add button base on info get from registry
    $Form.ShowDialog()
}


#createShortCutApplication -app "maya" -version 2014
#getNumberMax
showWindow