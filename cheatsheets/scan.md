# Service Scanning

`nmap -sC -sV {target}`
`nmap -sU -sV {target}`
`nmap -p- -T4 {target}`

# Web Application

`nikto -h {target}`
`dirb http://{target}`
`wpscan --url http://{target}`

# Network Services

`smbclient -L {target}`
`enum4linux -a {target}`
`snmpwalk -c public -v2c {target}`