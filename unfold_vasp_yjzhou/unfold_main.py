# parameters that need define:
# Emin; Emax; 
import sys
from unfold_in import *
import numpy as np
import numpy.linalg as LA
from wf_map import orb_s,orb_p
import pylab as pl
from parse import parse_procar
'''
    return orbitals, kpoints, kweights, bands, occupancies, \
           weights[:,:,:,:dim,:], phases

    orbitals    - (norbs) string array of orbital labels (s, px, py etc...)
    kpoints     - (npoints,3) float array of k-point coordinates
    kweights    - (npoints) float array of k-point weights
    bands       - (npoints,nbands,nspin) float array of band energies
    occupancies - (npoints,nbands,nspin) float array of band occupancies
    weights     - (npoints,nions*norbs,nbands,ndim,nspin) float array
                  of orbital weights
    ndim = 1 collinear, 4 otherwise
    phases      - (npoints,nions*norbs,nbands,nspin) complex array of
                  phases of orbital weights if LORBIT=12, otherwise None
'''


def gau(x,x0,sigma):
    return 1/np.sqrt(2*np.pi)/sigma*np.exp(-((x-x0)/2/sigma)**2)

def main():
    data=parse_procar(sys.argv[1])
    print "PROCAR read successfully"
    idim=0
    Ef=float(sys.argv[2])
    ispin=int(sys.argv[3])
#ax=fig.add_subplot(111)
    nkpt=data[3].shape[0]
    nband=data[3].shape[1]
    band=data[3]
    kpts=data[1]
    orbitals=data[0]
    norb=len(orbitals)
    weight=data[-2]
    phases = data[-1]
    orb_index=[]



    WF_map=np.loadtxt(wfmap_file)
    nband_s,dum=WF_map.shape
    nband_p=int(nband_s*V_p/V_s)
#    evals=np.zeros((nband,nkpt,2)) # evals and weights

    for j in range(len(projorb)): # orbital index
        temp=[]
      	for i in projorb[j]:
             temp.append(orbitals.index(i))
      	orb_index.append(temp)

#    projion=[ i for i in range(2,4)] # the ions that should be focus on
# read projion from unfold_in

    fig=pl.figure(figsize=(4,6))
    ax=fig.add_subplot(111)
#    for i in range(nband):
#      ax.plot(band[:,i,ispin],c='k')
    if len(projorb)>0:
      klist=np.arange(0,nkpt,1)
      for i_at_type in range(len(projorb)):
          weight_plot=np.zeros((nkpt,nband),dtype=complex)

          for i in range(nband):
              for orb in  orb_index[i_at_type]:
		  for ii,ion in enumerate(projion[i_at_type]):
			  
                          #weight_plot[:,i]+=weight[:,(ion)*norb+orb,i,0,ispin] \
			weight_plot[:,i]+=phases[:,(ion)*norb+orb,i,ispin] \
			  		   * (np.exp(-2j*np.pi*np.dot(kpath[:],WF_map[ii,2:])))
	      ax.scatter(klist,band[:,i,ispin],c=mycolor[i_at_type],s=(abs(weight_plot[:,i])**2 *40),alpha=0.7,edgecolors='none')


#-------------------------------------------
    pl.axhline(y=Ef,color='k')
    xticker=[]
    j=0
    for i in range(len(kpts)):

      if LA.norm(kpts[i]-Kpts[j])==0:
        xticker.append(i)
        j+=1
        pl.axvline(x=i,color='k')

    pl.ylabel('Energy(eV)')
    pl.xlim(0,len(klist)-1)
    pl.ylim(-1,3.5)
  #pl.ylim(-10,5)
#xlabels = ["$\Gamma$","Z","T",'Y',"$\Gamma$",'X','S','R','U']
    ax.set_xticks(xticker)
    ax.set_xticklabels(xlabels)
    pl.legend(loc='best')
    
    pl.tight_layout()
    pl.show()
    fig.savefig('./band_int.png')


if __name__=='__main__':
   main()
    
    
