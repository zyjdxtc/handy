import numpy as np
import numpy.linalg as LA
import sys
from unfold_in import *
import string as st


red_pos=[] # reduced positions
n=0 # type of atoms
red_pos=np.array(red_pos)
print red_pos




#norb=2  # number of orbitals in supercell
#orb_s=[  [0.0000000000000000,  0.5000000000000000,  0.5614271275197709, 2], \
#  	 [0.5000000000000000 , 0.0000000000000000,  0.5614271275197709, 2]] #reduced orbital positions in supercell 

# read norb and orb_s from unfold_in.py

orb_s=np.array(orb_s)
print 'orbital read in finished'

print orb_s
orb_car=np.dot(orb_s[:,0:3],vec_s) # cartesian orbital position

orb_p=np.zeros(orb_s.shape) # orb_p contains the same number of atoms in orb_s, but in the primitive cell, 
			    #so some of them are out of the cell
orb_p[:,0:3]=np.dot(orb_car,LA.inv(vec_p)) # reduced orbital positions in primitive cell
orb_p[:,3:] =orb_s[:,3:]
norb_p=int(norb*V_p/V_s) # orbital numbers in primitive cell
print 'orb in primitive cell', norb_p, 'Vp=',V_p, 'Vs=',V_s



#double check
orb_single=[] # orbital in a single primitive cell, all atoms should fit in the cell
n=0
eps=1e-6
for i,pos in enumerate(orb_p):
        # for particular cases:
	if pos[0]<0.9 and pos[0]>=-0.1 and pos[1]<0.9 and pos[1]>=-0.1 and pos[2]<1-eps and pos[2]>=0:
	#if pos[0] %1 ==pos[0] and pos[1]%1==pos[1] and pos[2]%2==pos[2]:    
	    orb_single.append(pos)
	    n+=1
shift_vec=np.array([[1,0,0],[0,1,0],[0,0,1]]) # enlarge the supercell to include more atoms, then transfer to primitive cell
if n<norb_p: # if not enough, for ex, the r2xr2x1 to 1x1x1 transfer
    for disp in shift_vec:
	if n==norb_p:
	    break
        for i,pos0 in enumerate(orb_s):
        #if pos[0]<1-eps and pos[0]>=0 and pos[1]<1-eps and pos[1]>=0 and pos[2]<1-eps and pos[2]>=0:
            pos=np.dot(np.dot(pos0[0:3]-disp,vec_s),LA.inv(vec_p)) 
	    if pos[0] %1 ==pos[0] and pos[1]%1==pos[1] and pos[2]%2==pos[2]:
          #  if pos[0]<0.9 and pos[0]>=-0.1 and pos[1]<0.9 and pos[1]>=-0.1 and pos[2]<1-eps and pos[2]>=0:
	        orb_single.append(np.append(pos,pos0[3:]))
                n+=1
	    if n==norb_p:
	        break
orb_single=np.array(orb_single)
orb_single.view('f8, f8, f8, i8').sort(axis=0,order='f3')
print 'orb_p'
print orb_p
print 'orb_s'
print orb_s
print 'orb_single'
print orb_single


if n!=norb_p:
    print 'orbital number not match'
    sys.exit(0)

f2=open(wfmap_file,'w')
print >> f2,"#orb_s\t orb_p\t a\t b\t c"
wfnum=0
# for distorted supercell, eps needs to be larger
# actually the below should be ions rather than orbs
eps1=0.01 
for i,orb0 in enumerate(orb_single):
    N_map=0 # the mapping orbital in the supercell number for each orbital
    for j,orb1 in enumerate(orb_p):
	shift=orb1-orb0
	if abs(round(shift[0])-shift[0])< eps1 \
	   and abs(round(shift[1])-shift[1])< eps1 \
	   and abs(round(shift[2])-shift[2])< eps1 \
	   and orb0[-1]==orb1[-1] \
	   and np.prod(orb0[3:]==orb1[3:]): 
	   #orb0[3:]==orb1[3:] returns an array of true or false
	    f2.write('{0}\t {1}\t {2}\t {3}\t {4}\n '.format(j,i,int(shift[0]),int(shift[1]),int(shift[2])))
	    N_map+=1
	    wfnum+=1
	if N_map==V_s/V_p:
	    break
if wfnum!=len(orb_s):
    print 'problem in mapped wf'
    sys.exit(0)
f2.close()	



