import numpy as np
import sys
import string as st

fname=sys.argv[1]
Nround= int(sys.argv[2])
f=open(fname,'r')
lines=f.readlines()
atom = lines[6].split()
N = 0
for i in range(len(atom)):
	N=N+int(atom[i])
for i in range(8):
	print lines[i].strip()
for i in range(8,8+N):
	print '%7.6f %7.6f %7.6f' %(round(float(lines[i].split()[0]),Nround)%1.0,\
	round(float(lines[i].split()[1]),Nround)%1.0,round(float(lines[i].split()[2]),Nround)%1.0)

