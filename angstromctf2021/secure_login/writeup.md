# Secure Login
Strings are null terminated in C, therefore the strcmp function will stop comparing when it encounters a null byte. There's a chance the first byte provided by `/dev/urandom` will be a null byte, so if we continue entering empty strings as our password, we'll get a hit at some point.

Letting the following bash command run for a few seconds provides the flag:
```
team7786@actf:/problems/2021/secure_login$ while true; do python2.7 -c "print('\x00')" | ./login | grep actf ; done
Enter the password: actf{if_youre_reading_this_ive_been_hacked}
```
