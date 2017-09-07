# parameters that need define:
# projfile; wfmap_file; wannier90wout; 
# vec_p; vec_s; kpts; klabel; Npt; Ef 

import numpy as np
import numpy.linalg as LA

wfmap_file = 'wf_map.dat' # output
#WF_map= np.loadtxt(wfmap_file) # the relation between the wannier function in the supercell and the wannier functions in the primitive cell.
                                 # They are typically just displacements in units of the primitive cell lattice constance.

Ef=2.23090820
a0=3.935 # scale
vec_p=np.array([[0.7071067811865476,0,0],[0.,0.7071067811865476,0],[0,0,1.5642543357518053]]) # lattice of primitive cell
vec_s=np.array([[0.7071067811865476,-0.7071067811865476,0],[0.7071067811865476,0.7071067811865476,0],[0,0,1.5642543357518053]]) # lattice of supercell

# shift_origin can shift the primitive cell
shift_origin =np.array([0,-1,0]) 

#reduced orbital positions in supercell, the last index is the type of ion 
orb_s=[  [0.0000000000000000,  0.5000000000000000,  0.5614271275197709, 2], \
         [0.5000000000000000 , 0.0000000000000000,  0.5614271275197709, 2]] 
norb=2 # orb number in the supercell

projorb=[['dxy'],['dyz'],['dxz']]
mycolor=['b','g','r']
projion=[[2,3],[2,3],[2,3]]

V_p=np.dot(vec_p[0],np.cross(vec_p[1],vec_p[2])) # volume of primitive cell
V_s=np.dot(vec_s[0],np.cross(vec_s[1],vec_s[2])) # volume of supercell

G_p=np.zeros((3,3)) # reciprocal lattice of primitive cell
G_s=np.zeros((3,3)) # supercell
for i in range(3):
    G_p[i]=np.cross(vec_p[(i+1) % 3],vec_p[(i+2)%3])/V_p
    G_s[i]=np.cross(vec_s[(i+1) % 3],vec_s[(i+2)%3])/V_s

kpts=np.array([[0.5,0.5,0],[0.,0.5,0]]) # high sym kpoints
Kpts=np.dot(np.dot(kpts,G_p),LA.inv(G_s)) # high sym kpoints in the supercell, for plotting
Npt = 120 # num of kpoints in the length of G_p[0]
kpath=[] # kpath in primitive cell
nkpt=[] # num of kpts between each two high sym kpts
for i in range(len(kpts)-1):
        dk=(kpts[i+1]-kpts[i])
        Nk=int(LA.norm(np.dot(dk,G_p))/LA.norm(G_p[0])*Npt)
        nkpt.append(Nk)
        for j in range(Nk):
            kpath.append(kpts[i]+dk/Nk*j)
kticks=[0] # ticks for k path
temp=0
for i in nkpt:
    temp+=i
    kticks.append(temp)

kpath.append(kpts[-1])
kpath=np.array(kpath)

Kpath = np.dot(np.dot(kpath,G_p),LA.inv(G_s)) # kpath in the supercell
#for k in Kpath:
#	if k[0]>0.5: 
#	    k[0]-=1.0
#	elif k[0]<=-0.5:
#	    k[0]+=1.0
#	if k[1]>0.5:
#	    k[1]-=1.0
#	elif k[1]<=-0.5:
#	    k[1]+=1.0
#	if k[2]>0.5:
#	    k[2]-=1.0
#	elif k[2]<=-0.5:
#	    k[2]+=1.0 

# plot parameters
xlabels= ["$\Gamma$","X"]

if __name__ == "__main__":
	print kpath
	print len(Kpath)
	print 'reciprocal'
	for i in range(len(Kpath)):
	   print Kpath[i,0],Kpath[i,1],Kpath[i,2],1

