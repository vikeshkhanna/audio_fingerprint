#!/usr/bin/python

import sys
import base64
import binascii
import gmpy
import string

c=sys.argv[1]
#c=base64.encodestring(p)



def b1(n):
    return "01"[n%2]

def b2(n):
    return b1(n>>1)+b1(n)

def b3(n):
    return b2(n>>2)+b2(n)

def b4(n):
    return b3(n>>4)+b3(n)

bytes = [ b4(n) for n in range(256)]
def binstring(s):
    return ''.join(bytes[ord(c)] for c in s)


	
 



#p=base64.decodestring(c)
##a=binascii.a2b_base64(c)
b=binstring(c)
print b
c=string.atoi(b, 2)
print c

#bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in "aa"), 0))
#for c in b:
#    print gmpy.digits(ord(c), 2)
