$Root = $PSScriptRoot;

$WshShell = New-Object -ComObject WScript.Shell;

$MyShortCut = $WshShell.CreateShortcut($Root);