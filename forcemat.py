#For getting the force matrix and eigenval and eigenvecs 

import numpy as np
import cmath as cm
import sys,string,re
import numpy.linalg as li
from numpy.linalg import inv
Ntype=4
Natom=10
fname=['OUTCAR','DYNMAT']
f=open(fname[0],'r')
lstart=0
lines=f.readlines()
mass=[]
eachtype=[1,1,2,6]#[1,1,2,6]
u=1.66053886E-27 #kg
e=1.6E-19 #C
h=6.63E-34

f.close()
for l in range(len(lines)):
    if string.find(lines[len(lines)-l-1],'SECOND DERIVATIVES (NOT SYMMETRIZED)')>=0:
        lstart=len(lines)-l-1
        break

rows=[]
dynmat=[]#temp mat
for i in range(3*Natom):
    temp=string.split(lines[lstart+3+i])
    for j in range(3*Natom):
        rows.append(string.atof(temp[j+1]))
#    print rows
    dynmat.append(rows)
    rows=[]
num=0

for l in lines:
    if num>=Ntype:
        break
    if string.find(l,'POMASS')>0:
        print l
        num+=1
        m=re.match('.*MASS = (.*); .*',l) 
        mass.append(string.atof(string.strip(m.group(1))))
print mass

massM=np.zeros((Natom*3,Natom*3))
mat=-1*np.array(dynmat)

for i in range(3*Natom):
    for j in range(3*Natom):
        mat[j,i]=(mat[i,j]+mat[j,i])*0.5
        mat[i,j]=mat[j,i]

    

#print mat
for RowNum in range(Ntype):
    for rownum in range(3*eachtype[RowNum]):
        i=RowNum
        rnum=0
        while i>0:
            rnum+=3*eachtype[i-1]
            i-=1
        print rnum
        massM[(rownum+rnum),(rownum+rnum)]=mass[RowNum]
       # mat[:,(rownum+rnum)]/=np.sqrt(mass[RowNum])
#print inv(massM)
matnew=np.dot(inv(massM),mat)

#for i in range(3*Natom):
#    for j in range(3*Natom):
#        mat[j,i]=(mat[i,j]+mat[j,i])*0.5
#        mat[i,j]=mat[j,i]
#print mat[1]
#print mat[:,1]
print eachtype

(val,vec)=np.linalg.eig(matnew)
for i in range(len(val)):
    for j in range(len(val)-i-1):
        if val[j]>val[j+1]:
            temp=val[j]
            val[j]=val[j+1]
            val[j+1]=temp
            temp=vec[:,j]
            vec[:,j]=vec[:,j+1]
            vec[:,j+1]=vec[:,j]

for v in range(len(val)):
    if val[v] >0:

        val[v]=np.sqrt(val[v])*15.633302 #VaspToTHz
    else:
        val[v]=-1*np.sqrt(-1*val[v])*15.633302
    
print val
print vec[:,0],vec[:,1]

