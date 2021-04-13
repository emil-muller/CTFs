from decimal import Decimal, getcontext
from Crypto.Cipher import AES

getcontext().prec = 50

x_1, y_1 = (Decimal(457020213401268758000507112920047694562582161398)/(10**10), Decimal(31020634442404276336820538929941614215700357571144)/(10**11))
x_2, y_2 = (Decimal(55221733168602409780894163074078708423359152279)/(10**9), Decimal(34788496561380896247486644841834767173970270575362)/(10**11))
x_3, y_3 = (Decimal(147829667933855179054593001600696671775906950984)/(10**10), Decimal(34024000394165154334507454055942629110169490484699)/(10**11))


# Formulars for circle center found on http://ambrsoft.com/TrigoCalc/Circle3D.htm
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
# actf{elliptical_curve_minus_the_curve}
