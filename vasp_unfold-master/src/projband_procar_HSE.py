from parse import parse_procar
import numpy as np
import pylab as pl
import sys
import numpy.linalg as LA
def main():
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
  data=parse_procar(sys.argv[1])
  idim=0
  Ef=float(sys.argv[2])
  ispin=int(sys.argv[3])
#ax=fig.add_subplot(111)
  nkpt=data[3].shape[0]
  nband=data[3].shape[1]
  band=data[3]
  kweight=data[2]
  kpts=data[1]  
  orbitals=data[0]
  norb=len(orbitals)
  weight=data[-2]
  projorb=[['dxz','dxy','dyz','dx2','dz2']]
  colors=['b']
  orb_index=[]
  kzero=0
  for i in range(len(kweight)):
      if kweight[i]==0:
         kzero=i
	 break
  for j in range(len(projorb)): # orbital index
      temp=[]
      for i in projorb[j]:
         temp.append(orbitals.index(i))
      orb_index.append(temp)

  projion=[ i for i in range(2,4)]
  fig=pl.figure()
  ax=fig.add_subplot(111)
  for i in range(band.shape[1]):
      ax.plot(band[kzero:,i,ispin],c='k')
  for iatom in range(len(projorb)):
      
      weight_plot=np.zeros((nkpt-kzero,nband))
      for i in range(nband):
      	  for ion in projion:
              for orb in orb_index[iatom]:
	          weight_plot[:,i]+=weight[kzero:,(ion)*norb+orb,i,0,ispin]
      klist=np.arange(0,nkpt-kzero,1)
      print weight_plot[:,1].shape,band[kzero:,0,0].shape
      for i in range(nband):
          ax.scatter(klist[:],band[kzero:,i,ispin],c=colors[iatom],s=(weight_plot[:,i]*50),edgecolors='none')      

  kpath=np.array([[0,0,0],[0.5,0.,0],[0.5,0.5,0.],[0,0,0]])
  xticker=[]
  j=0
  for i in range(kzero,len(kpts)):
    if LA.norm(kpts[i]-kpath[j])==0:
        xticker.append(i-kzero)
        j+=1
        pl.axvline(x=i-kzero,color='k')

  pl.ylabel('Energy(eV)')
  pl.xlim(0,len(klist)-1)
#xlabels = ["$\Gamma$","Z","T",'Y',"$\Gamma$",'X','S','R','U']
  #pl.ylim(0,11)
  pl.ylim(-3,5)
  xlabels= ["$\Gamma$","X","M",'$\Gamma$']
  ax.set_xticks(xticker)
  ax.set_xticklabels(xlabels)


  pl.axhline(y=Ef,color='k')
   
  pl.show()


if __name__=='__main__':
  main()
 
