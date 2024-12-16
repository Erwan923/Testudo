# Reconnaissance Initiale

## Initial Scan
`nmap -sn {target}`
`nmap -sS -sV -Pn {target}`

## Service Enumeration
`enum4linux -a {target}`
`nikto -h {target}`

## Port Scanning
`nmap -p- -T4 {target}`
`masscan -p1-65535 {target} --rate=1000`

# Analyse de Vulnérabilités

## Basic Vuln Scan
`nmap --script vuln {target}`
`nmap --script safe {target}`

## Service Specific
`smbclient -L {target}`
`showmount -e {target}`