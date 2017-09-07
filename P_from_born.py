import numpy as np
import string as st
import Position_displace
import sys
def P_from_born(fname,disp):
    f=open(fname) 
    lines=f.readlines()
    p=np.array([0,0,0]).T
    for i in range(len(disp)):
	bornM=np.zeros((3,3),dtype=float)
	
	for j in range(3):
	    temp=lines[i*4+1+j].split()
	    bornM[j,0]=float(temp[1])
	    bornM[j,1]=float(temp[2])
	    bornM[j,2]=float(temp[3])
   	p += np.dot(bornM,disp[i].T) 
    return p

if __name__=='__main__':
   undis=sys.argv[1]
   dis=sys.argv[2]
   bornf=sys.argv[3]
   coordundis,posundis,fhead,specundis=readpos(undis)
   coorddis,posdis,fhead,specdis=readpos(dis)
   posundis=sort1(posundis,specundis)
   posdis=sort1(posdis,specdis)
   p=P_from_born(bornf,posdis-posundis)
   print p 
  
