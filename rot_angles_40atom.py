# Calculate octahedra rotations in perovskites

import sys
import numpy as np
import string as st
from numpy import linalg as LA

fname= sys.argv[1]
f=open(fname,'r')
lines=f.readlines()
f.close()

# read scale and bases vectors
scale = float(st.split(lines[1])[0])
print scale

vec=[]
for i in range(3):
    temp=st.split(lines[2+i])
    vec.append([float(temp[0]),float(temp[1]),float(temp[2])])
vec=np.array(vec)
###seclect atoms
for i in range(len(lines)):
    if st.find(lines[i],'Direct') >=0:
        num=i
        break

Ti=[]
Ticar=[]
for i in range(6):
    temp=st.split(lines[num+5+i])
    Ti.append(np.array([float(temp[0]),float(temp[1]),float(temp[2])]))
    Ticar.append(scale*np.array([np.dot(Ti[i],vec[:,0]),np.dot(Ti[i],vec[:,1]),np.dot(Ti[i],vec[:,2])]))
O=[]
Ocar=[]
for i in range(24):
    temp=st.split(lines[num+9+i])
    O.append(np.array([float(temp[0]),float(temp[1]),float(temp[2])]))
    Ocar.append(scale*np.array([np.dot(O[i],vec[:,0]),np.dot(O[i],vec[:,1]),np.dot(O[i],vec[:,2])]))
M=[]
Mcar=[]
for i in range(6):
    temp=st.split(lines[num+5+i])
    M.append(np.array([float(temp[0]),float(temp[1]),float(temp[2])]))
    Mcar.append(scale*np.array([np.dot(M[i],vec[:,0]),np.dot(M[i],vec[:,1]),np.dot(M[i],vec[:,2])]))


#theta001=np.arccos((LA.norm(Mncar[0][0:2]-Ocar[4][0:2])**2+LA.norm(Mncar[1][0:2]-Ocar[4][0:2])**2-LA.norm(Mncar[0]-Mncar[1]#)**2)/(2*LA.norm(Mncar[0][0:2]-Ocar[4][0:2])*LA.norm(Mncar[1][0:2]-Ocar[4][0:2])))
#theta001=0.5*(180-theta001/np.pi*180)

print 'O6=',Ocar[6]

theta001=np.arccos((LA.norm((Mncar[0]+scale*vec[1])[0:2]-Ocar[6][0:2])**2+LA.norm(Mncar[1][0:2]-Ocar[6][0:2])**2-LA.norm(Mncar[0]-Mncar[1]+vec[1]*scale)**2)/(2*LA.norm((Mncar[0]+vec[1]*scale)[0:2]-Ocar[6][0:2])*LA.norm(Mncar[1][0:2]-Ocar[6][0:2])))
                            
             
theta001=0.5*(180-theta001/np.pi*180) 

theta110=np.arccos((LA.norm(Mncar[0]-Ocar[2])**2+LA.norm(Mncar[2]-Ocar[2])**2-LA.norm(Mncar[0]-Mncar[2])**2)/(2*LA.norm(Mncar[0]-Ocar[2])*LA.norm(Mncar[2]-Ocar[2])))


print 'theta001=',theta001
print 'theta110=', theta110

