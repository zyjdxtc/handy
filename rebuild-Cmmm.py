# Change unit cell. Enlarge original unitcell and truncate it into the shape we want

import numpy as np
import string as st
from numpy import linalg as LA

def enlarge(vec,pos,ran): # enlarge original unit cell,
                           #calculate atom positions in Cartesian. Need basis vector and atomic pos
    m,n=pos.shape
    multi=(ran*2+1)**3*m
    pos_carte=np.zeros((multi,n))
    origin=[]

    for i in range(ran*2+1):
        for j in range(ran*2+1):
            for k in range(ran*2+1):
                temp=(0-ran+i)*vec[0]+(0-ran+j)*vec[1]+(0-ran+k)*vec[2]
                origin.append([temp[0],temp[1],temp[2]])
    origin=np.array(origin)
    for k in range(multi/m):
      for i in range(m):
        temp=origin[k]
        for j in range(3):
            temp=temp+vec[j]*pos[i,j]
       
        pos_carte[int(k*m+i),0:3]=temp
        pos_carte[int(k*m+i),3]=pos[i,3]
    return pos_carte
    
def trunc(vec,poscar): # change carte pos into reduced pos, and choose in range(0,1)
    m,n=poscar.shape
    newpos=[]
    for i in range(m):
        temp0=np.dot(poscar[i,0:3],vec[0])/LA.norm(vec[0])/LA.norm(vec[0])
        temp1=np.dot(poscar[i,0:3],vec[1])/LA.norm(vec[1])/LA.norm(vec[1])
        temp2=np.dot(poscar[i,0:3],vec[2])/LA.norm(vec[2])/LA.norm(vec[2])
        if temp0 >=0 and temp0< 0.9999 and temp1 >=0 and temp1< 0.9999 and temp2 >=0 and temp2< 0.9999:
            newpos.append([temp0,temp1,temp2,poscar[i,3]])
    newpos=np.array(newpos)
    return newpos

#def sort_pos(pos):
#    m,n=pos.shape
#    for i in range(m-1):
#        for j in range(m-1-i):
#            if pos[j,3] > pos[j+1,3]:
#                temp=pos[j+1,0:4]
#                print temp
#                pos[j+1,0:4]=pos[j,0:4]
#                pos[j,0:4]=temp
#    return pos

def main():
    vec=np.array([[2,0,0],[0,2,0],[0,0,2]])
    rawdata='0     0.75     0 1\
    0     0.25     0 1\
    0.5     0.25     0 1\
    0.5     0.75     0 1\
    0     0.75     0.5 2\
    0     0.25     0.5 2\
    0.5     0.25     0.5 2\
    0.5     0.75     0.5 2\
    0.25     0     0.25 3\
    0.75     0     0.75 3\
    0.75     0     0.25 3\
    0.25     0     0.75 3\
    0.75     0.5     0.25 3\
    0.25     0.5     0.75 3\
    0.25     0.5     0.25 3\
    0.75     0.5     0.75 3\
    0.29418999     0     0 4\
    0.70581001     0     0 4\
    0.79418999     0.5     0 4\
    0.20581001     0.5     0 4\
    0.205809996     0     0.5 4\
    0.79418999     0     0.5 4\
    0.70581001     0.5     0.5 4\
    0.29418999     0.5     0.5 4\
    0     0     0.78125 4\
    0     0     0.21875 4\
    0.5     0.5     0.78125 4\
    0.5     0.5     0.21875 4\
    0     0.5     0.71875 4\
    0     0.5     0.28125 4\
    0.5     0     0.71875 4\
    0.5     0     0.28125 4\
    0.25     0.25     0.25 4\
    0.75     0.75     0.75 4\
    0.75     0.75     0.25 4\
    0.25     0.25     0.75 4\
    0.75     0.25     0.75 4\
    0.25     0.75     0.25 4\
    0.25     0.75     0.75 4\
    0.75     0.25     0.25 4'

    number_in_a_row=4
    temp=st.split(rawdata)
    pos=[]
    for i in range(len(temp)/number_in_a_row):
        pos.append([float(temp[4*i]),float(temp[4*i+1]),float(temp[4*i+2]),float(temp[4*i+3])])

    pos=np.array(pos)

    car=enlarge(vec,pos,5)
    newvec=np.array([[1,-1,0],[1,1,0],[0,0,2]])

    newpos=trunc(newvec,car)
    m,n=newpos.shape
    print 'Number of atoms=',m
    newpos.view('f8, f8, f8, i8').sort(axis=0,order='f3') # built-in sort code from numpy
    for i in range(m):
        print ' %10.8f %10.8f %10.8f'  %(newpos[i,0],newpos[i,1],newpos[i,2])
    print newpos[:,3]
main()
