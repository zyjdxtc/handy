# This is a code to switch columns of data, especially POSCAR.
# USE: python change_column.py POSCAR 0(or 1,2, whichever we want it to be the first column)

import string as st
import sys

fname = sys.argv[1]
firstcol=int(sys.argv[2])
secondcol=int(sys.argv[3])
thirdcol=int(sys.argv[4])
f=open(fname,'r')
lines=f.readlines()
for l in range(len(lines)):
    temp=lines[l].split()
    if l >= 8:
	print temp[firstcol], temp[secondcol],temp[thirdcol]
    else:
	print lines[l].rstrip()
