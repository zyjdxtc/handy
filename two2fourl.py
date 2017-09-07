#get enlarge the 1 1 2 lattice to 1 1 4 lattice, with the same atomic positions at the top and botton double-layers

import numpy as np
import string,sys

fname = sys.argv[1]
natom=10
f=open(fname,'r')
lines1=f.readlines()
num=0
for i in range(len(lines1)):
	if (string.find(lines1[len(lines1)-1-i],'Direct')>=0):
		num=len(lines1)-i #atomic positions start
		break
f.close()

print lines1[num]
for i in range(natom):
	temp=string.split(lines1[i+num])
	print temp[0],temp[1],string.atof(temp[2])/2
        print temp[0],temp[1],string.atof(temp[2])/2+0.5




