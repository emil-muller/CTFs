# Webservice enumeration
Quick and dirty checklist for webserver enumeration

# Tools
* [nmap](https://nmap.org/) - Essential tool for open port discovery and service version enumeration
* [wfuzz](https://github.com/xmendez/wfuzz) - API parameter fuzzer
* [gobuster](https://github.com/OJ/gobuster) - Directory/file bruteforce finder
* [sqlmap](http://sqlmap.org/) - Automatic SQLi tool
* [enum4linux-ng](https://github.com/cddmp/enum4linux-ng) - Samba enumeration tool

# Interesting files/dirs
- [ ]  `robots.txt`?
- [ ] `.git`?
- [ ] `app.py`?

# Versions
- [ ] Any outdated software running?
- [ ] Any public exploits for software versions?
- [ ] Any security fixes in change log for the version after?
- [ ] Are old API versions still reachable?

# FTP
- [ ] Allow anonymous login?
- [ ] Does any previous credentials provide access?
- [ ] Any writable directories that can be accessed though other webservice?
- [ ] Any interesting files?

# SMB
- [ ] Any public users?
- [ ] Does any previous credentials provide access?
- [ ] Any publicly accessible shares?
- [ ] Any writable shares that can be accessed by other means?

# SQLi
- [ ] Are any form parameters injectable?

# XXS
- [ ] Is stored XXS possible and can higher privileged users be tricked into executing it?
- [ ] Is reflected XXS possible and can higher privileged users be tricked into executing it?

# SSRF
- [ ] Is SSRF possible and can filters be by passed? Fx. by `[0:0:0:0:0:ffff:127.0.0.1]`

# Auth bypass
- [ ] Is SQLi able to bypass auth?
- [ ] Weak session cookies?
- [ ] Hidden usertype variables in user registration?
