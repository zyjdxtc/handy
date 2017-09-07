import numpy as np
import numpy.linalg as LA
import sys
from unfold_in import *
import string as st


red_pos=[] # reduced positions
n=0 # type of atoms
red_pos=np.array(red_pos)
print red_pos


# read norb and orb_s from unfold_in.py

#orb_s=np.array(orb_s)

print 'orbital read in finished'
print orb_s

#orb_car=np.dot(orb_s[:,0:3],vec_s) # cartesian orbital position
orb_p=np.zeros(orb_s.shape) # orb_p contains the same number of atoms in orb_s, but in the primitive cell, 
			    #so some of them are out of the cell
orb_p[:,0:3]=np.dot(orb_s[:,:3],LA.inv(vec_p)) # reduced orbital positions in primitive cell
orb_p[:,3:] =orb_s[:,3:]
norb = len(orb_s)
print 'orb in supercell', norb
#norb_p=int(norb*V_p/V_s) # orbital numbers in primitive cell
norb_p = 64
print 'orb in primitive cell', norb_p, 'Vp=',V_p, 'Vs=',V_s



#double check
orb_single=[] # orbital in a single primitive cell, all atoms should fit in the cell
n=0

eps=0.0023
def backtrack(temp,ret):
    if len(temp)==3:
	ret.append(temp[:])
	return
    for i in [0,1,-1]:
	temp.append(i)
	backtrack(temp,ret)
	temp.pop()

dirs = []
backtrack([],dirs)
print 'shifts'
print dirs

for i,pos in enumerate(orb_p):
	print pos
        # for particular cases:
	#if pos[0]<1.-eps and pos[0]>=eps and pos[1]<1.-eps and pos[1]>=eps and pos[2]<1-eps and pos[2]>=eps:
	#if pos[0] %1 ==pos[0] and pos[1]%1==pos[1] and pos[2]%2==pos[2]:    
	if pos[0]>=1. or pos[0]<0 or pos[1]>=1. or pos[1]<0 or pos[2]>=1. or pos[2]<0:
	    continue
	valid = True
	for j in orb_single:
	    for x,y,z in dirs:
		x1,y1,z1 = x+pos[0],y+pos[1], z+pos[2]
	    	if abs(x1-j[0]) < 0.02 and abs(y1-j[1])<0.02 and abs(x1-j[0]) <0.02:
		   valid = False
		   break
	    if not valid:
		break 
	if not valid:
	    continue
	orb_single.append(pos)
	n+=1
print n 
shift_vec=np.array([[1,0,0],[0,1,0],[1,1,0],[-1,0,0],[0,-1,0],[-1,-1,0]]) # enlarge the supercell to include more atoms, then transfer to primitive cell
if n<norb_p: # if not enough, for ex, the r2xr2x1 to 1x1x1 transfer
    for disp in shift_vec:
	if n==norb_p:
	    break
        for i,pos0 in enumerate(orb_s):
        #if pos[0]<1-eps and pos[0]>=0 and pos[1]<1-eps and pos[1]>=0 and pos[2]<1-eps and pos[2]>=0:
            pos=np.dot(np.dot(pos0[0:3]-disp,vec_s),LA.inv(vec_p)) 
	    if pos[0] %1 ==pos[0] and pos[1]%1==pos[1] and pos[2]%1==pos[2]:
          #  if pos[0]<0.9 and pos[0]>=-0.1 and pos[1]<0.9 and pos[1]>=-0.1 and pos[2]<1-eps and pos[2]>=0:
	        orb_single.append(np.append(pos,pos0[3:]))
                n+=1
	    if n==norb_p:
	        break
orb_single=np.array(orb_single)
nc = 0
for i in orb_single:
    if i[-1] == 1.:
	nc+=1
print 'nc=',nc
orb_single.view('f8, f8, f8, i8').sort(axis=0,order='f3')
#print 'orb_p'
#print orb_p
print 'orb_s'
print orb_s
print 'orb_single'
print orb_single


if n!=norb_p:
    print 'orbital number not match'
    print 'n_orb_single=', len(orb_single)
    for i in range(len(orb_single)-1):
	for j in range(i+1,len(orb_single)):
	    if LA.norm(orb_single[i,:3] - orb_single[j,:3]) < 0.1**0.5 \
		 or LA.norm(orb_single[i,:3] - orb_single[j,:3])>2.99**0.5:
		print 'care ', i, j, 'orbs'
		print  orb_single[i], orb_single[j]
    sys.exit(0)

f2=open(wfmap_file,'w')
print >> f2,"#orb_s\t orb_p\t a\t b\t c"
wfnum=0
# for distorted supercell, eps needs to be larger
# actually the below should be ions rather than orbs
eps1=0.3 
nC=0
for i,orb0 in enumerate(orb_single):
    N_map=0 # the mapping orbital in the supercell number for each orbital
    for j,orb1 in enumerate(orb_p):
	if N_map==V_s/V_p:
	    break

	shift=orb1-orb0
	
	if abs(round(shift[0])-shift[0])< eps1 \
	   and abs(round(shift[1])-shift[1])< eps1 \
	   and abs(round(shift[2])-shift[2])< eps1 \
	   and orb0[-1]==orb1[-1]:
	   #and np.prod(orb0[3:]==orb1[3:]):
	   #orb0[3:]==orb1[3:] returns an array of true or false
	    if int(orb0[-1])==1:
		nC+=1
		for it in range(3):
	    	    f2.write('{0}\t {1}\t {2}\t {3}\t {4}\n '.format(j,i,int(shift[0]),int(shift[1]),int(shift[2])))
	    f2.write('{0}\t {1}\t {2}\t {3}\t {4}\n '.format(j,i,int(shift[0]),int(shift[1]),int(shift[2])))
		
	    N_map+=1
	    wfnum+=1
print 'C atoms = ',nC
print 'total wf', wfnum,len(orb_s)
if wfnum!=len(orb_s):
    print 'problem in mapped wf', wfnum,len(orb_s)
    sys.exit(0)
f2.close()	



