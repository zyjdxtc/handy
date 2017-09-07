#This code is to print out the displacment amplitude of each atom in a specific eigenvector

import numpy as np
import string as st
import sys

modenum=sys.argv[2]
fname=sys.argv[1]
Natom=10

f=open(fname,'r')
lines=f.readlines()
f.close()
if fname=='OUTCAR':

    for i in range(len(lines)):
        if st.find(lines[len(lines)-1-i],'THz') >0 and st.find(lines[len(lines)-1-i],modenum+' f') >=0:
            startline=len(lines)-1-i
            break
    print lines[startline]
    for i in range(Natom):
        temp=st.split(lines[startline+2+i])
        print temp[0],temp[1],temp[2],'Amp^2',float(temp[3])**2+float(temp[4])**2,'amp',\
	np.sqrt(float(temp[3])**2+float(temp[4])**2),float(temp[3])/abs(float(temp[3]))\
	*np.sqrt(float(temp[3])**2+float(temp[4])**2)

else:
    for i in range(Natom):
        temp=st.split(lines[i])
        print temp[0],'Amp^2',float(temp[1])**2+float(temp[2])**2,'amp',np.sqrt(float(temp[1])**2+float(temp[2])**2),\
	float(temp[1])/abs(float(temp[1]))*np.sqrt(float(temp[1])**2+float(temp[2])**2)
