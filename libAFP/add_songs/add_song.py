#!/usr/bin/python
#from connection import conn
import sys
import binascii
import string
import math

SIZE = 8

#following functions would convert from ascii to binary
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
#################################


#open file containing the fingerprint and read it
fingerprint_file1=sys.argv[1]
fingerprint_file2=sys.argv[2]

fin1 = open("songs/"+fingerprint_file1, "r")
fingerprint_b641 = fin1.read()
fin1.close()


fin2 = open("songs/"+fingerprint_file2, "r")
fingerprint_b642 = fin2.read()
fin2.close()

#print fingerprint_b641

##################################

#convert fingerprint from base64 to ascii and then binary
fingerprint1 = binascii.a2b_base64(fingerprint_b641)
fingerprint2 = binascii.a2b_base64(fingerprint_b642)

#print len(fingerprint)

b1=binstring(fingerprint1)
b2=binstring(fingerprint2)
fout=open("logs", "w+")

#fout.write(b+"\n")
length=len(b1)/SIZE
i=0;
#cursor=conn.cursor()
#cursor.execute("SELECT max(song_id) FROM songs_fingerprints")
#row=cursor.fetchone()
#if row[0]==None:
#    song_id=1
#else:
#    song_id=row[0]+1

#print song_id

difference=0
match=0
while i<length:
#    fout.write(str(string.atoi(b[i*SIZE:(i+1)*SIZE], 2))+"\n")
#    cursor.execute("INSERT INTO SONGS")
    print str(string.atoi(b1[i*SIZE:(i+1)*SIZE], 2))+"  "+str(string.atoi(b2[i*SIZE:(i+1)*SIZE], 2))
    n1=string.atoi(b1[i*SIZE:(i+1)*SIZE], 2)
    n2=string.atoi(b2[i*SIZE:(i+1)*SIZE], 2)
    if n1-n2==0:
        match=match+1
    difference=difference+(n1-n2)*(n1-n2)
    i=i+1
difference=math.sqrt(difference/565)
fout.write(str(difference))
fout.close()
print (str(difference))
print (str(match))
#c=string.atoi(b, 2)
#print c
###################################

#cursor = conn.cursor()
#cursor.execute("SELECT * FROM lut")
