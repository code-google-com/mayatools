$root = $PSScriptRoot;
$uis_dir = $root.Replace("source", "");
$files = Get-ChildItem $uis_dir -Recurse -Filter *.ui;
foreach($f in $files)
{
    $pythonPath = $f.FullName.Replace(".ui" , ".py");
    $sourcePath = $f.FullName
    pyuic4 $sourcePath -o $pythonPath;
    # (the parenthesis around the Get-Content to ensure that Ge-Content is completely done before Set-Content is executed.)
    (Get-Content $pythonPath)|    
    ForEach-Object{ 
            $_ -creplace "import IconResource_rc", "import developer.main.source.IconResource_rc"
    } | Set-Content $pythonPath;
    
    # {should be on the same line with ForEach unless Foreach consider the code in between { and } is outside the command.
    # should check whether widget .py existed or not.
    $widgetPath = $pythonPath.Replace("ui\" + $f.Name.Replace( ".ui", ".py"), "") + $f.Name.Replace("UI", "Widget").Replace(".ui", ".py");
    $package = $widgetPath.Split("\")[5];
    $module = $widgetPath.Split("\")[6];
    $content = "try:`n`treload(ui)`nexcept:`n`tfrom developer.main." + 
                $package + "." + $module + ".widget.ui import " + $f.Name.Replace(".ui", "") + " as ui" +
                "`n`nfrom PyQt4 import QtGui`n`nclass QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                `n`tdef __init__(self):`n`t`tsuper(QtGui.QMainWindow, self).__init__(parent = None)`n`t`tself.setupUi(self)"; 
    $fileisExist = Test-Path $widgetPath;
    if ($fileisExist -eq $false)
    {
        #Write-Host "File not exist";
        Set-Content $widgetPath $content;
    }
}