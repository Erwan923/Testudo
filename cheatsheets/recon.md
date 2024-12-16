# Initial Reconnaissance

`nmap -sn {target}`
`nmap -sS -sV -Pn {target}`
`masscan -p1-65535 {target} --rate=1000`

# Service Enumeration

`enum4linux -a {target}`
`nikto -h {target}`
`nmap -p- --script vuln {target}`

# Intelligence Gathering

`dig {target}`
`whois {target}`
`theHarvester -d {target} -l 500 -b all`