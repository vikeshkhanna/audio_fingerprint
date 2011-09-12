import os

path = 'clips/test/'
listing = os.listdir(path)
count=1
f = open('out_test_fp', 'w')
f.close()

for infile in listing:
	count = count + 1	
	os.system('./bin/Debug/libAFP -p --file=out_test_fp clips/test/' + infile)
	

