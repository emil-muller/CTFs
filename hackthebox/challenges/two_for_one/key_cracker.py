import sympy
import base64

# Shitty implementation of extended euclidian algorithm
def egcd(e1, e2):
    if e1 == 0:
        return (0, 1)
    else:
        y, x = egcd(e2 % e1, e1)
        return (x - (e2 // e1) * y, y)

# Define known constants
modulo = 0xC6ACB8DF486E6671D4A5564803E1C3214A8E274DE0AC0043EC28C8589F377C7E8D308BC3E302850384344BA7988885620A418E6AD955578284FC04F289F126B38A01816251CEF9A14FD4C249D96B69087FA91B2E1ADBDC80CB96FF0CCB6129D8F6737DA850C451F2ED3F6CB61C36891DC924D0AB28F26ADF0ED357CE848D02FFE00912714CCF6372C1F41080E86747A0303EB5CDF6CE912F1144FD4F55743C796875A14FDFF8F8B662150C56BE58B09239771DC44D969079C4AD8FD993BC630B7855D2E02E8BE16824DCD5AB3813231C1731110A8BD028D7A1DFAB892E75294557BAFC71AEAF5E48DB0267A6DB63D350F995068EE1CAD6D32DF11A49BD24BA97
e1 = 0x010001
e2 = 0x053CB7
msg1 = b"RBVdQw7Pllwb42GDYyRa6ByVOfzRrZHmxBkUPD393zxOcrNRZgfub1mqcrAgX4PAsvAOWptJSHbrHctFm6rJLzhBi/rAsKGboWqPAWYIu49Rt7Sc/5+LE2dvy5zriAKclchv9d+uUJ4/kU/vcpg2qlfTnyor6naBsZQvRze0VCMkPvqWPuE6iL6YEAjZmLWmb+bqO+unTLF4YtM1MkKTtiOEy+Bbd4LxlXIO1KSFVOoGjyLW2pVIgKzotB1/9BwJMKJV14/+MUEiP40ehH0U2zr8BeueeXp6NIZwS/9svmvmVi06Np74EbL+aeB4meaXH22fJU0eyL2FppeyvbVaYQ=="
msg1_int = int.from_bytes(base64.b64decode(msg1), "big")
msg2 = b"TSHSOfFBkK/sSE4vWxy00EAnZXrIsBI/Y6mGv466baOsST+qyYXHdPsI33Kr6ovucDjgDw/VvQtsAuGhthLbLVdldt9OWDhK5lbM6e0CuhKSoJntnvCz7GtZvjgPM7JDHQkAU7Pcyall9UEqL+W6ZCkiSQnK+j6QB7ynwCsW1wAmnCM68fY2HaBvd8RP2+rPgWv9grcEBkXf7ewA+sxSw7hahMaW0LYhsMYUggrcKqhofGgl+4UR5pdSiFg4YKUSgdSw1Ic/tug9vfHuLSiiuhrtP38yVzazqOZPXGxG4tQ6btc1helH0cLfw1SCdua1ejyan9l1GLXsAyGOKSFdKw=="
msg2_int = int.from_bytes(base64.b64decode(msg2), "big")

# Calculate a,b such that e_1*a,e_2*b=1
a,b = egcd(e1,e2)

# Calculate cleartext as hex
cleartext_hex = str(hex(pow(msg1_int,a,modulo)*pow(msg2_int,b,modulo)%modulo))
# Decode cleartext to ascii and print 
print(bytearray.fromhex(cleartext_hex[2:]).decode())
