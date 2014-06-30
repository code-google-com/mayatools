$root = $PSScriptRoot;
$uis_dir = $root.Rep "source", "";
$files = Get-ChildItem $uis_dir -Recurse -Filter *.ui;
foreach($f in $files)
{
    $p = $f.FullName.Replace(".ui" , ".py");
    $s = $f.FullName
    pyuic4 $s -o $p;
    # (the parenthesis around the Get-Content to ensure that Ge-Content is completely done before Set-Content is executed.)

    (Get-Content $p)|    
    ForEach-Object{ 
            $_ -creplace "import IconResource_rc", "import developer.main.source.IconResource_rc"
    } | Set-Content $p;
    
    # { should be on the same line with ForEach unless Foreach consider the code in between { and } is outside the command.

       
}