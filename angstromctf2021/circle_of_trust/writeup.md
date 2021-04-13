# AngstromCTF2021 Circle of Trust

We're given the output:
```
(45702021340126875800050711292004769456.2582161398, 310206344424042763368205389299416142157.00357571144)
(55221733168602409780894163074078708423.359152279, 347884965613808962474866448418347671739.70270575362)
(14782966793385517905459300160069667177.5906950984, 340240003941651543345074540559426291101.69490484699)
838371cd89ad72662eea41f79cb481c9bb5d6fa33a6808ce954441a2990261decadf3c62221d4df514841e18c0b47a76
```

This is generated from the code:
```
import random
import secrets
import math
from decimal import Decimal, getcontext
from Crypto.Cipher import AES

BOUND = 2 ** 128
MULT = 10 ** 10

getcontext().prec = 50

def nums(a):
    b = Decimal(random.randint(-a * MULT, a * MULT)) / MULT
    c = (a ** 2 - b ** 2).sqrt()
    if random.randrange(2):
        c *= -1
    return (b, c)


with open("flag", "r") as f:
    flag = f.read().strip().encode("utf8")

diff = len(flag) % 16
if diff:
    flag += b"\x00" * (16 - diff)

keynum = secrets.randbits(128)
ivnum = secrets.randbits(128)

key = int.to_bytes(keynum, 16, "big")
iv = int.to_bytes(ivnum, 16, "big")

x = Decimal(random.randint(1, BOUND * MULT)) / MULT
for _ in range(3):
    (a, b) = nums(x)
    print(f"({keynum + a}, {ivnum + b})")

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
enc = cipher.encrypt(flag)
print(enc.hex())
```

We notice that the function `nums` is responsible for generating the tuples in the out put.
`b` is selected randomly selected from the interval `(-a,a)` and `c` is calculated from the equation `c = (a ** 2 - b ** 2).sqrt()`. Rearranging the equation we get `a^2=b^2+c^2`. In other words the points `(b,c)` are just points on the circle with radius `a`.

Using this information we see that `keynum` and `ivnum` is the center of this circle. Given three points we can find the center of the circle with the formulars found on this site: http://ambrsoft.com/TrigoCalc/Circle3D.htm

Coding it all up we get:
```
from decimal import Decimal, getcontext
from Crypto.Cipher import AES

getcontext().prec = 50

x_1, y_1 = (Decimal(457020213401268758000507112920047694562582161398)/(10**10), Decimal(31020634442404276336820538929941614215700357571144)/(10**11))
x_2, y_2 = (Decimal(55221733168602409780894163074078708423359152279)/(10**9), Decimal(34788496561380896247486644841834767173970270575362)/(10**11))
x_3, y_3 = (Decimal(147829667933855179054593001600696671775906950984)/(10**10), Decimal(34024000394165154334507454055942629110169490484699)/(10**11))

# Get the x-coordinate of the circle center
def x_coor(x_1,x_2,x_3,y_1,y_2,y_3):
    t = (x_1*x_1+y_1*y_1)*(y_2-y_3)+(x_2*x_2+y_2*y_2)*(y_3-y_1)+(x_3*x_3+y_3*y_3)*(y_1-y_2)
    n = 2*(x_1*(y_2-y_3)-y_1*(x_2-x_3)+x_2*y_3-x_3*y_2)
    return t/n

# Get the y-coordinate of the circle center
def y_coor(x_1,x_2,x_3,y_1,y_2,y_3):
    t = (x_1*x_1+y_1*y_1)*(x_3-x_2)+(x_2*x_2+y_2*y_2)*(x_1-x_3)+(x_3*x_3+y_3*y_3)*(x_2-x_1)
    n = 2*(x_1*(y_2-y_3)-y_1*(x_2-x_3)+x_2*y_3-x_3*y_2)
    return t/n

keynum = round(x_coor(x_1,x_2,x_3,y_1,y_2,y_3))
ivnum  = round(y_coor(x_1,x_2,x_3,y_1,y_2,y_3))

key = int.to_bytes(keynum, 16, "big")
iv = int.to_bytes(ivnum, 16, "big")
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
flag = "838371cd89ad72662eea41f79cb481c9bb5d6fa33a6808ce954441a2990261decadf3c62221d4df514841e18c0b47a76"
flag = bytes.fromhex(flag)
flag = cipher.decrypt(flag)
print(flag)
```
Which prints the flag: `actf{elliptical_curve_minus_the_curve}`
