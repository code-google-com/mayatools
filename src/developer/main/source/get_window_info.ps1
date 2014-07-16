function Get-OSVersion{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )
    $os = Get-WmiObject -class Win32_OperatingSystem -ComputerName $ComputerName
    $prop = @{'OSVersion' = $os.version;
              'SPVersion' = $os.servicepackmajorversion;
              'OSBuild'   = $os.buildnumber}
    New-Object -TypeName PSObject -Property $prop
}

