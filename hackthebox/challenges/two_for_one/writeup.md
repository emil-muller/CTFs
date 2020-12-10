# Two for One
From the hint, we learn that Alice sent the same message to Bob two times.
After extracting the files in the zip, we're presented with four files:
```
➜  TwoForOne ls -la
total 16
drwx------  2 emil emil 120 Dec 10 13:49 .
drwxrwxrwt 15 root root 320 Dec 10 13:49 ..
-rw-r--r--  1 emil emil 450 Nov 18 14:05 key1.pem
-rw-r--r--  1 emil emil 450 Nov 18 14:05 key2.pem
-rw-r--r--  1 emil emil 344 Nov 18 14:05 message1
-rw-r--r--  1 emil emil 344 Nov 18 14:05 message2
```
Checking the keys we recognize that they are RSA keys:
```
➜  TwoForOne cat key1.pem 
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxqy430huZnHUpVZIA+HD
IUqOJ03grABD7CjIWJ83fH6NMIvD4wKFA4Q0S6eYiIViCkGOatlVV4KE/ATyifEm
s4oBgWJRzvmhT9TCSdlraQh/qRsuGtvcgMuW/wzLYSnY9nN9qFDEUfLtP2y2HDaJ
Hckk0Kso8mrfDtNXzoSNAv/gCRJxTM9jcsH0EIDoZ0egMD61zfbOkS8RRP1PVXQ8
eWh1oU/f+Pi2YhUMVr5YsJI5dx3ETZaQecStj9mTvGMLeFXS4C6L4Wgk3NWrOBMj
HBcxEQqL0CjXod+riS51KUVXuvxxrq9eSNsCZ6bbY9NQ+ZUGjuHK1tMt8RpJvSS6
lwIDAQAB
-----END PUBLIC KEY-----
```
Analyzing the keys with `openssl` we see that both of them have their modulus and exponent at offset 19.
We can extract those with:
```
➜  TwoForOne openssl asn1parse -inform PEM -in key1.pem -strparse 19
    0:d=0  hl=4 l= 266 cons: SEQUENCE          
    4:d=1  hl=4 l= 257 prim: INTEGER           :C6ACB8DF486E6671D4A5564803E1C3214A8E274DE0AC0043EC28C8589F377C7E8D308BC3E302850384344BA7988885620A418E6AD955578284FC04F289F126B38A01816251CEF9A14FD4C249D96B69087FA91B2E1ADBDC80CB96FF0CCB6129D8F6737DA850C451F2ED3F6CB61C36891DC924D0AB28F26ADF0ED357CE848D02FFE00912714CCF6372C1F41080E86747A0303EB5CDF6CE912F1144FD4F55743C796875A14FDFF8F8B662150C56BE58B09239771DC44D969079C4AD8FD993BC630B7855D2E02E8BE16824DCD5AB3813231C1731110A8BD028D7A1DFAB892E75294557BAFC71AEAF5E48DB0267A6DB63D350F995068EE1CAD6D32DF11A49BD24BA97
  265:d=1  hl=2 l=   3 prim: INTEGER           :010001
➜  TwoForOne openssl asn1parse -inform PEM -in key2.pem -strparse 19 
    0:d=0  hl=4 l= 266 cons: SEQUENCE          
    4:d=1  hl=4 l= 257 prim: INTEGER           :C6ACB8DF486E6671D4A5564803E1C3214A8E274DE0AC0043EC28C8589F377C7E8D308BC3E302850384344BA7988885620A418E6AD955578284FC04F289F126B38A01816251CEF9A14FD4C249D96B69087FA91B2E1ADBDC80CB96FF0CCB6129D8F6737DA850C451F2ED3F6CB61C36891DC924D0AB28F26ADF0ED357CE848D02FFE00912714CCF6372C1F41080E86747A0303EB5CDF6CE912F1144FD4F55743C796875A14FDFF8F8B662150C56BE58B09239771DC44D969079C4AD8FD993BC630B7855D2E02E8BE16824DCD5AB3813231C1731110A8BD028D7A1DFAB892E75294557BAFC71AEAF5E48DB0267A6DB63D350F995068EE1CAD6D32DF11A49BD24BA97
  265:d=1  hl=2 l=   3 prim: INTEGER           :053CB7
```
Here we see that only the exponent differs.
Lucky for us we gcd(0x010001,0x053CB7)=1.
That means that there exists a,b in Z such that:
```
a*0x010001+b*0x053CB7=1
```

We have that:
```
c_1 = m^(e_1) mod n
c_2 = m^(e_2) mod n
=>
c_1*c_2 = m^(e_1)*m^(e_2) mod n
=>
c_1^(a)*c_2^(b) = m^(e_1*a)*m^(e_2*b) mod n
=>
c_1^(a)*c_2^(b) = m^(e_1*a+e_2*b) mod n
=>
c_1^(a)*c_2^(b) = m^1 mod n
=>
c_1^(a)*c_2^(b) = m mod n
```
We can easily find the pair `(a,b)` with the extended euclidian algorithm.

This means we're able to calculate `m` quite quickly.
I wrote a dirty python script that calculates the flag.
It's placed in the `key_cracker.py` file.
Challenge done. 
