import sys
import string as st
import numpy as np

fname=sys.argv[1]
shiftvec=np.array([-0.5,0,0])

f=open(fname,'r')
lines=f.readlines()
for i in range(len(lines)):
	if st.find(lines[i],'Direct')>=0:
		startline=i
		break
for i in range(startline+1):
	print lines[i].rstrip()
N=0
for i in range(len(lines[startline-1].split())):
	N=N+float(lines[startline-1].split()[i]) # total number of atoms
for i in range(int(N)):
	temp=np.array([float(lines[startline+1+i].split()[0]),float(lines[startline+1+i].split()[1]),float(lines[startline+1+i].split()[2])])
	temp=temp+shiftvec
#	for j in range(3):
#		if temp[j] >=1: temp[j]=temp[j]-1.0
#	print ' %10.8f %10.8f %10.8f' %((temp[0]+100.0)%1.0,(temp[1]+100.0)%1.0,(temp[2]+100.0)%1.0)
	if temp[2] > 0.9 and temp[2] < 1:
		print ' %10.8f %10.8f %10.8f' %((temp[0]+100.0)%1.0,(temp[1]+100.0)%1.0,(temp[2]-1))
	else:
		print ' %10.8f %10.8f %10.8f' %((temp[0]+100.0)%1.0,(temp[1]+100.0)%1.0,(temp[2]+100.0)%1.0)
