# Notes

From the hint we can guess that the user probably saved their password/flag on the desktop as a text file.

Running as `strings` scan on the file and `grep`'ing for `password` yields:
```
➜  /tmp strings image.mem| grep password
passwords.txt
passwords.txt
.
.
.
.
```
This might be what we're looking for.


We can check the memory dump with volatility:
```
➜  /tmp volatility imageinfo -f image.mem                   
Volatility Foundation Volatility Framework 2.6.1
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/tmp/image.mem)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002a3b0a0L
          Number of Processors : 6
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002a3cd00L
                KPCR for CPU 1 : 0xfffff880009f1000L
                KPCR for CPU 2 : 0xfffff88002ea9000L
                KPCR for CPU 3 : 0xfffff88002f1f000L
                KPCR for CPU 4 : 0xfffff88002f95000L
                KPCR for CPU 5 : 0xfffff88002fcb000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2021-03-20 18:16:12 UTC+0000
     Image local date and time : 2021-03-20 13:16:12 -0500
```
And see if the `passwords.txt` file is open in any window.
```
➜  /tmp volatility windows --profile=Win7SP0x64 -f image.mem | grep "passwords.txt"
Volatility Foundation Volatility Framework 2.6.1
Window Handle: #5017c at 0xfffff900c0816b80, Name: passwords.txt - Notepad
```
We can now see that it's open in notepad. We can now isolate that process and carve out the memory from that process.
```
➜  /tmp volatility memdump --profile=Win7SP1x64 -f image.mem -n "notepad.exe" --dump-dir .      
Volatility Foundation Volatility Framework 2.6.1                                          
************************************************************************
Writing notepad.exe [  2696] to 2696.dmp
```
Now we should be able to find the flag in the dumped memory:
```
➜  /tmp strings 2696.dmp | grep "UMASS"
```
Aaaaand we got nothing...
What if we try with little endian strings instead?
```
➜  /tmp strings -e l 2696.dmp | grep "UMASS"                                                   
UMASS{$3CUR3_$70Rag3}
```
Jackpot
