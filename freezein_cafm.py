#get freezed in atomic positions from phonon calculation OUTCAR
#for 1 1 2 superlattice
import numpy as np
import string,sys

#fname = sys.argv[1]
modename=sys.argv[1]
poscar=sys.argv[2]
Natom=20
a=[]

f=open(poscar,'r')
lines1=f.readlines()
for i in range(len(lines1)):
	if string.find(lines1[i],'POSCAR') >= 0:
		zero=i+1
		break
for i in range(3):
	scale=string.split(lines1[1+zero])
	temp=string.split(lines1[2+i+zero])
	a.append(string.atof(temp[i])*string.atof(scale[0]))
f.close()
print 'a=',a
print zero

f=open(modename,'r')
lines2=f.readlines()
f.close()

sequence=[1,2,3,4,5,6,7,8,9,10,13,16,14,15,11,12,17,20,18,19]
x=[]
y=[]
z=[]
norm=0
startline=8
for i in range(Natom/2):
    for j in range(2):
	print lines1[startline+zero+sequence[i*2+j]-1]
	temp1=string.split(lines1[startline+zero+sequence[i*2+j]-1])
	temp2=string.split(lines2[i])
	x.append((string.atof(temp1[0])+string.atof(temp2[1])))
	y.append((string.atof(temp1[1])+string.atof(temp2[2])))
	z.append((string.atof(temp1[2])+string.atof(temp2[3])))

for i in range(7):
	print lines1[i+zero]
print 'Cartesian'
for i in range(Natom):
	print x[i],y[i],z[i]



