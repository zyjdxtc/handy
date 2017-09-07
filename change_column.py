# This is a code to switch columns of data, especially POSCAR.
# USE: python change_column.py POSCAR 0(or 1,2, whichever we want it to be the first column)

import string as st
import sys

fname = sys.argv[1]
firstcol=int(sys.argv[2])
f=open(fname,'r')
lines=f.readlines()
for l in lines:
    temp=l.split()
    if len(temp)== 3:
	print temp[firstcol], temp[(firstcol+1)%3],temp[(firstcol+2)%3]
    else:
	print l
