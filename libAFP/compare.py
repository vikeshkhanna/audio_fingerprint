import base64
import binascii
f1 = open("in1","r")
f2 = open("in2","r")

x1 = f1.read()
x2 = f2.read()

s1 = base64.b64decode(x1)
s2 = base64.b64decode(x2)

print binascii.a2b_base64(x1)


