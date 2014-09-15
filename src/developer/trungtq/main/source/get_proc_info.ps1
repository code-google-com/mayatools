function Get-OSVersion{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )

function Get-InfoProc{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )
    $procs = Get-WmiObject -Class Win32_Process -ComputerName $ComputerName
    foreach ($proc in $procs){
        $prop = @{'ProcName' = $proc.name;
                  'Executable' = $proc.ExecutablePath
        }
        New-Object -TypeName PSObject -Property $prop
    }
}

    