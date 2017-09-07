#get freezed in atomic positions from phonon calculation OUTCAR
#for 1 1 2 superlattice
import numpy as np
import string,sys

#fname = sys.argv[1]
modeNUM=sys.argv[1]
Natom=10
a=[]

f=open('POSCAR','r')
lines1=f.readlines()
for i in range(3):
	scale=string.split(lines1[1])
	temp=string.split(lines1[2+i])
	a.append(string.atof(temp[i])*string.atof(scale[0]))
f.close()
print 'a=',a


print modeNUM
f=open('OUTCAR','r')
lines=f.readlines()
leng=len(lines)
flag1=0 # flag of finding 'TOTEN'
flag2=0 #flag for a complete outcar
for l in range(leng):
	if (string.find(lines[leng-l-1],'General timing and accounting informations for this job:')>=0):
		flag2=1
	if (string.find(lines[leng-l-1],'THz')>0 and string.find(lines[leng-l-1],modeNUM+' f')>0): 
		flag1=1
		lnum=leng-l-1
		break
if (flag1==0 or flag2==0):
	print fname, 'has a problem'

lnum_cp=lnum # a copy, in case
flag3=1
x=[]
y=[]
z=[]
norm=0
f.close()
for i in range (Natom+2):
	print lines[lnum+i]
	temp=string.split(lines[lnum+i])

	if (temp[1]<='9' and temp[1]>='-'):
		x.append((string.atof(temp[0])+string.atof(temp[3]))/a[0])
		y.append((string.atof(temp[1])+string.atof(temp[4]))/a[1])
		z.append((string.atof(temp[2])+string.atof(temp[5]))/a[2])
		norm+=string.atof(temp[3])**2+string.atof(temp[4])**2+string.atof(temp[5])**2
for i in range(Natom):
	print x[i],y[i],z[i]
print 'eigenvector normalized to',norm


