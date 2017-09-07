#get freezed in atomic positions from phonon calculation OUTCAR
#for 1 1 2 superlattice
import numpy as np
import string,sys

#fname = sys.argv[1]
#modeNUM=sys.argv[1]
Natom=10
a=[]




f=open('data','r')
lines=f.readlines()
leng=len(lines)
flag1=0 # flag of finding 'TOTEN'
flag2=0 #flag for a complete outcar

x=[]
y=[]
z=[]
norm=0
for i in range (Natom):
	print lines[i]
	temp=string.split(lines[i])

	if (temp[1]<='9' and temp[1]>='-'):
		x.append(string.atof(temp[0])/4.0845)
		y.append(string.atof(temp[1])/4.0845)
		z.append(string.atof(temp[2])/3.89/1.92)
#		norm+=string.atof(temp[3])**2+string.atof(temp[4])**2+string.atof(temp[5])**2
f.close()
#	print x[i],y[i],z[i]
f=open('data1','r')
lines=f.readlines()
x1=[]
y1=[]
z1=[]
for i in range (Natom):
        print lines[i]
        temp=string.split(lines[i])

        if (temp[1]<='9' and temp[1]>='-'):
                x1.append(string.atof(temp[0])/4.0845)
                y1.append(string.atof(temp[1])/4.0845)
                z1.append(string.atof(temp[2])/3.89/1.92)
#               norm+=string.atof(temp[3])**2+string.atof(temp[4])**2+string.atof(temp[5])**2                                
for i in range(Natom):

        print x[i]+x1[i],y[i]+y1[i],z[i]+z1[i]


#print 'eigenvector normalized to',norm

f.close()

