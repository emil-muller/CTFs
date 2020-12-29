# Nisse Omvendt
We get the code:
```
nisse_omvendt.py:

import sys

besked = sys.argv[1]

filnavn = 'kodet_besked.bin'

kodet_besked = ''
for i in range(0, len(besked)):
    c = ord(besked[i])
    nc = ord(besked[(i + 1) % len(besked)])
    c = (c ^ 64) & 0xFF
    c = (c -  1) & 0xFF
    c = (c ^  1) & 0xFF
    c = (c +  i) & 0xFF
    c = (c +  nc) & 0xFF
    kodet_besked += chr(c)

f = open(filnavn, 'w')
f.write(kodet_besked)
f.close()


f = open(filnavn, 'r')
kodet_besked = f.read()
f.close()

dekodet_besked = ''
for i in range(0, len(kodet_besked)):
    c = ord(kodet_besked[i])
$$2133248hfdsfBIIIIPP!!!123213123dddddCRASH!
```
And the encrypted message:
```
8F 57 F0 B7 A2 9D AC AD AE 9B 93 98 98 93 95 96
A3 A0 9D 9E AB AE AF A8 9C AC A5 AF B3 AF C7 BC
A7 B2 B5 B3 AA A5 B3 B8 BE CA C3 C8 CB BF D0 DA
```

We see that all of the operations made on c are easily reversable (except the one involving nc).
Since we know the flag format (nc3{}), we can assume the first character to be `n` and therefore get a value
for the first nc. Thus we generate the code: 
```
def decrypt(kodet_besked):
	dekodet_besked = 'n'
	for i in range(len(kodet_besked)-1, 0, -1):
		print("--------dec----------")
		c = ord(kodet_besked[i])
		nc = ord(dekodet_besked[-1])
		c = (c - nc) & 0xFF
		c = (c -  i) & 0xFF
		c = (c ^  1) & 0xFF
		c = (c +  1) & 0xFF
		c = (c ^ 64) & 0xFF
		dekodet_besked += chr(c)
	print(dekodet_besked)
```
The output we get is:
```
n}emtirogla_giledyrbu_ne_teval_rah_gej_ssssey{3c
```
Reversing everything but the firs character we have:
```
nc3{yessss_jeg_har_lavet_en_ubrydelig_algoritme}
```
