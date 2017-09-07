# Change unit cell. Enlarge original unitcell and truncate it into the shape we want

import numpy as np
import string as st
from numpy import linalg as LA
import sys
def enlarge(vec,pos,ran): # enlarge original unit cell,
                           #calculate atom positions in Cartesian. Need basis vector and atomic pos
    m,n=pos.shape
    multi=(ran*2+1)**3*m # total number of atoms of the enlarged region
    pos_carte=np.zeros((multi,n))
    origin=[]

    for i in range(ran*2+1):
        for j in range(ran*2+1):
            for k in range(ran*2+1):
                temp=(0-ran+i)*vec[0]+(0-ran+j)*vec[1]+(0-ran+k)*vec[2]
                origin.append([temp[0],temp[1],temp[2]])
    origin=np.array(origin)
    for k in range(multi/m): # multi/m origin choices
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
        temp = np.dot(LA.inv(vec),poscar[i,0:3])
        temp0=round(temp[0],5)
        temp1=round(temp[1],5)
        temp2=round(temp[2],5)
        if temp0 >=-1e-6 and temp0< 1-1e-6 and temp1 >=-1e-6 and temp1< 1-1e-6 and temp2 >=-1e-6 and temp2< 1-1e-6:
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
    vec=np.array([[1,0,0],[0,1,0],[0,0,1]])
    if len(sys.argv)==1:
      rawdata=' 0.2500000000000000  0.2500000000000000  0.2870217730698080 1\
  0.2500000000000000  0.2500000000000000  0.7870217730698079 1\
  0.2500000000000000  0.7500000000000000  0.2870217730698080 1\
  0.2500000000000000  0.7500000000000000  0.7870217730698079 1\
  0.7500000000000000  0.2500000000000000  0.2870217730698080 1\
  0.7500000000000000  0.2500000000000000  0.7870217730698079 1\
  0.7500000000000000  0.7500000000000000  0.2870217730698080 1\
  0.7500000000000000  0.7500000000000000  0.7870217730698079 1\
  0.0000000000000000  0.0000000000000000  0.0187874868186365 2\
  0.0000000000000000  0.0000000000000000  0.5187874868186365 2\
  0.0000000000000000  0.5000000000000000  0.0187874868186365 2\
  0.0000000000000000  0.5000000000000000  0.5187874868186365 2\
  0.5000000000000000  0.0000000000000000  0.0187874868186365 2\
  0.5000000000000000  0.0000000000000000  0.5187874868186365 2\
  0.5000000000000000  0.5000000000000000  0.0187874868186365 2\
  0.5000000000000000  0.5000000000000000  0.5187874868186365 2\
  0.0000000000000000  0.0000000000000000  0.2424831609664446 3\
  0.0000000000000000  0.0000000000000000  0.7424831609664447 3\
  0.0000000000000000  0.2500000000000000  0.9858537895725570 3\
  0.0000000000000000  0.2500000000000000  0.4858537895725571 3\
  0.0000000000000000  0.5000000000000000  0.2424831609664446 3\
  0.0000000000000000  0.5000000000000000  0.7424831609664447 3\
  0.0000000000000000  0.7500000000000000  0.9858537895725570 3\
  0.0000000000000000  0.7500000000000000  0.4858537895725571 3\
  0.2500000000000000  0.0000000000000000  0.9858537895725570 3\
  0.2500000000000000  0.0000000000000000  0.4858537895725571 3\
  0.2500000000000000  0.5000000000000000  0.9858537895725570 3\
  0.2500000000000000  0.5000000000000000  0.4858537895725571 3\
  0.5000000000000000  0.0000000000000000  0.2424831609664446 3\
  0.5000000000000000  0.0000000000000000  0.7424831609664447 3\
  0.5000000000000000  0.2500000000000000  0.9858537895725570 3\
  0.5000000000000000  0.2500000000000000  0.4858537895725571 3\
  0.5000000000000000  0.5000000000000000  0.2424831609664446 3\
  0.5000000000000000  0.5000000000000000  0.7424831609664447 3\
  0.5000000000000000  0.7500000000000000  0.9858537895725570 3\
  0.5000000000000000  0.7500000000000000  0.4858537895725571 3\
  0.7500000000000000  0.0000000000000000  0.9858537895725570 3\
  0.7500000000000000  0.0000000000000000  0.4858537895725571 3\
  0.7500000000000000  0.5000000000000000  0.9858537895725570 3\
  0.7500000000000000  0.5000000000000000  0.4858537895725571 3'

    else:
	fname=sys.argv[1]
	f=open(fname,'r')
	lines=f.readlines()
	for i in range(len(lines)):	
	    if st.find(lines[i],'Direct')>= 0 or st.find(lines[i],'Cartesian')>= 0:
		startline=i
		break
	atom_spe=lines[startline-1].split() # atom species, and number of each type
	rawdata=''
	count=0
	for i in range(len(atom_spe)):
	    for j in range(int(atom_spe[i])):
		temp=lines[startline+count+1].split()
		count = count+1
      	        rawdata=rawdata+temp[0]+' '+temp[1]+' '+ temp[2]+' '+str(i+1)+' '	
    number_in_a_row=4
    temp=st.split(rawdata)
    pos=[]
    for i in range(len(temp)/number_in_a_row):
        pos.append([float(temp[4*i]),float(temp[4*i+1]),float(temp[4*i+2]),float(temp[4*i+3])])

    pos=np.array(pos)

    car=enlarge(vec,pos,3)
    newvec=np.array([[2,0,0],[0,3,0],[0,0,1]])

    newpos=trunc(newvec,car)
    m,n=newpos.shape
    print 'Number of atoms=',m
    newpos.view('f8, f8, f8, i8').sort(axis=0,order='f3') # built-in sort code from numpy
    for i in range(m):
        print ' %10.8f %10.8f %10.8f'  %(newpos[i,0],newpos[i,1],newpos[i,2])
    print newpos[:,3]
main()
