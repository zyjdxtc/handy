import pylab as pl
import numpy.linalg as LA
import sys
from copy import deepcopy
from scipy import *
from kpath import k_path # kpath routine
 
dmft_orb=[[1,2,4]]


rham=sys.argv[1] 		# rham.py file
execfile(rham) 			# such that the TB matrix is imported

sig_raw=loadtxt(sys.argv[2]) 	# load the sigma file in real frequency
Sig= zeros((len(sig_raw),(len(sig_raw[0])-1)/2),dtype=complex)
ommesh = deepcopy(sig_raw[:,0])
for i in range((len(sig_raw[0])-1)/2):
    Sig[:,i] = sig_raw[:,i*2+1]+1j*sig_raw[:,i*2+2]
mu=float(sys.argv[3])
nw = len(sig_raw)
# define kpath
# high sym kpoints
k=array([[0.0,0.0,0],[0.5,0.,0.],[0.5,0.5,0.],[0.,0.,0.],[0.5,0.5,0.5]])
# lattice shape in real space
lat=array([[1,0,0],[0,1,0],[0,0,1.]])*3.9

kpath = k_path(k,lat)

# read TB hamiltonian
nr=len(Hopping.keys())		# Hopping comes from rham.py file
norb = len(Hopping[Hopping.keys()[0]])
ham=zeros((nr,norb,norb),dtype=complex)
tran=zeros((nr,3),dtype=int)
for i,ii in enumerate(sorted(Hopping.keys())):
        ham[i,:,:]=Hopping[ii]
for i,ii in enumerate(sorted(Hopping.keys())):
        tran[i,:]=array(ii)

Ginv=zeros((len(kpath), norb,norb,nw),dtype=complex)
G = zeros((len(kpath), norb,norb,nw),dtype=complex)
# set up the TB hamiltonian

broaden = 1e-3
print '================ Constructing G function...============='
for ik,kp in enumerate(kpath): 
    for iw,w in enumerate(ommesh):
        for i in range(nr):
            Ginv[ik,:,:,iw]-=ham[i,:,:]*exp(1j*dot(kpath[ik],tran[i,:]))
    # add in the self energy, for which the double counting should already be substracted
#        Ginv[ik,:,:,iw]+=w+1j*broaden
        for ib,ibath in enumerate(dmft_orb):
	    for iorb in ibath:
	        Ginv[ik,iorb,iorb,iw] -= Sig[iw,ib]
	(eigs,eigv)=LA.eigh(Ginv[ik,:,:,iw])
	# construct the diagonal terms
	for ib in range(norb):
	    for jb in range(norb):
		
        	G[ik,jb,jb,iw]+=1./(w+1j*broaden +mu - eigs[ib])*conj(eigv[jb,ib])*eigv[jb,ib]

fig=pl.figure()
ax=fig.add_subplot(111)

print '=============== Plotting... ================='
A = -1./pi*G.imag
bands=zeros(nw)
for ib,ibath in enumerate(dmft_orb):
     for iorb in ibath:
	ax.imshow(A[:,ib,ib,:],cmap=grey,origin='lower')
fig.savefig('./contour.pdf')
pl.show()
		



