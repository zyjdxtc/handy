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
  kpts=data[1]
  orbitals=data[0]
  norb=len(orbitals)
  weight=data[-2]
  projorb=[['dxz','dxy','dyz','dz2','dx2'],['dxz','dxy','dyz','dz2','dx2'],['dxz','dxy','dyz','dz2','dx2'],\
	  ['px','py','pz'],['px','py','pz']]
#  projorb=[['dxz','dxy','dyz','dz2','dx2'],['dxz','dxy','dyz','dz2','dx2'],['dxz','dxy','dyz','dz2','dx2'],\
#         ['px','py','pz'],['px','py','pz']]
  #projorb=[['dxz','dxy','dyz','dz2','dx2']]
  mycolor=['g','m','r','y','b']
  orb_index=[]
  
  for i in range(len(projorb)): # orbital index
      orb_temp=[]
      for j in projorb[i]:
          orb_temp.append(orbitals.index(j))
      orb_index.append(orb_temp)
  projion= [[2,3],\
  	    [8],[11],[12],[19,23]]
	    #[27,31,43,47]] #,\
  	  #  [ i for i in range(4,8)]] #,\
	   # [19,23]]
	  # [27,34,40,46]]
	  # [31,33,43,45]]
	 #  [27,34,40,46]]
	 #  [i for i in range(8,31)]+[32]+[j for j in range(33,43)]+[44]+[k for k in range(46,48)] ]
  
  if len(projion)!=len(projorb):
      print 'projected orbital are not specified clearly with projected ions'
      sys.exit(0)
  
  fig=pl.figure()
  ax=fig.add_subplot(111)
  #for i in range(band.shape[1]):
  #    ax.plot(band[:,i,ispin],c='k')
  if len(projorb)>0:
      klist=np.arange(0,nkpt,1)
      for i_at_type in range(len(projorb)):
          weight_plot=np.zeros((nkpt,nband))
      
          for i in range(nband):
      	      for ion in projion[i_at_type]:
	          for orb in  orb_index[i_at_type]:
	                  weight_plot[:,i]+=weight[:,(ion)*norb+orb,i,0,ispin]
      #for i in range(nband):
              ax.scatter(klist,band[:,i,ispin],c=mycolor[i_at_type],s=(weight_plot[:,i]*40),alpha=0.7,edgecolors='none')      
  pl.axhline(y=Ef,color='k')
  kpath=np.array([[0,0,0],[0.5,0,0],[0.5,0.5,0],[0,0,0]])
  xticker=[]
  j=0
  for i in range(len(kpts)):

    if LA.norm(kpts[i]-kpath[j])==0:
        xticker.append(i)
        j+=1
        pl.axvline(x=i,color='k')

  pl.ylabel('Energy(eV)')
  pl.xlim(0,len(klist)-1)
  pl.ylim(-3,6)
  #pl.ylim(-10,5)
#xlabels = ["$\Gamma$","Z","T",'Y',"$\Gamma$",'X','S','R','U']
  xlabels= [r"$\Gamma$","X","M",r'$\Gamma$']
  ax.set_xticks(xticker)
  ax.set_xticklabels(xlabels)
  
  
  pl.show()
  fig.savefig('./band.png')

if __name__=='__main__':
  main()
 
