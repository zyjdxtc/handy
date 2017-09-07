import numpy as np
import string as st
import sys,random

fname=sys.argv[1]
scale=float(sys.argv[2])
f=open(fname,'r')
lines=f.readlines()
for i in range(8):
        print lines[i].strip()
for l in lines[8:]:
	temp=l.split()
	for i in range(len(temp)):
		temp[i]=float(temp[i])+scale*(random.random()-0.5)
	print '%.7f  %.7f  %.7f' % (temp[0] % 1.0 ,temp[1] % 1.0,temp[2] % 1.0)

