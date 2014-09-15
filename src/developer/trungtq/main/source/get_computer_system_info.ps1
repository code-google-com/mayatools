function Get-InfoCompSystem{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$ComputerName
    )
    $cs = Get-WmiObject -class Win32_ComputerSystem -ComputerName $ComputerName
    $prop =@{'Model' =  $cs.model;
             'Manufacturer' = $cs.manufacturer;
             'RAM (GB)' = "{0:N2}" -f ($cs.totalphysicalmemory / 1GB);
             'Socket' = $cs.numberofprocessors;
             'Cores' = $cs.numberoflogicalproccessors
    }
    New-Object -TypeName PSObject -Property $prop
}
