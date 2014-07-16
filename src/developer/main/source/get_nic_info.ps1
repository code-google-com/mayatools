function Get-InfoNIC{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )
    $nics = Get-WmiObject -Class Win32_NetworkAdapter -ComputerName $ComputerName -Filter "PhysicalAdapter=True"
    foreach ($nic in $nics){
        $prop = @{'NICName' = $nic.servicename;
                  'Speed' = $nic.speed/1MB -as [int];
                  'Manufacturer' = $nic.manufacturer;
                  'MACAddress' = $nic.macaddress
        }
        New-Object -TypeName PSObject -Property $prop
    }
}


    