function Get-InfoBadService{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )
    $svcs = Get-WmiObject -Class Win32_Service -ComputerName $ComputerName -Filter "StartMode='Auto' AND State<> 'Runnning'"
    foreach ($sc in $svcs){
        $prop = @{'ServiceName' = $svcs.name;
                  'LogonAccount' = $svcs.startname;
                  'DisplayName' = $svcs.displayname
        }
        New-Object -TypeName PSObject -Property $prop
    }
}


    