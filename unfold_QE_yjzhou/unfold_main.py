# parameters that need define:
# Emin; Emax; 
import sys
from unfold_in import *
import numpy as np
import numpy.linalg as LA
from wf_map import orb_s,orb_p
import pylab as pl
import  xml.etree.ElementTree as ET


def parse_QE(xmlname):
	'''
	read projections from xml file
	bands
	projections
	'''
	tree = ET.parse(xmlname)
	root = tree.getroot()
	nb = int(root.findall('.//NUMBER_OF_BANDS')[0].text.strip())
	nk = int(root.findall('.//NUMBER_OF_K-POINTS')[0].text.strip())
	nat = int(root.findall('.//NUMBER_OF_ATOMIC_WFC')[0].text.strip())

	# projections
	# projection
	#  nk
	#    natom
	#      nband
	projs = root.find('.//PROJECTIONS')
	proj_weight = []
	#bands
	bands=[]
	#eigs = root.find('.//EIGENVALUES')
	for ik in range(nk):
	    ks = str(ik+1)
    	    ks = 'K' + '0'*(5-len(ks))+ks
            tree_eig = ET.parse(ks+'/eigenval.xml')
    	    eig_root = tree_eig.getroot()
    
    	    eig0 = eig_root.find('.//EIGENVALUES').text.split()
    	    tempE = [float(ie) for ie in eig0] 
    
	    #iband =eigs[ik][0].text.split()
	    #band_t=[]
	    #for ib in range(nb):
		#band_t.append(float(iband[ib]))
	    bands.append(tempE)
	    temp = []
	    for iat in range(nat):
		temp2 =[]
		
		nums = projs[ik][iat].text.strip().split('\n')
		for i in range(nb):
		    newline = nums[i].split(',')
		    temp2.append(float(newline[0]) + float(newline[1])*1j)
		temp.append(temp2[:])
	    proj_weight.append(temp)
	proj_weight=np.array(proj_weight)
  	ha2eV = 27.2114
	bands = np.array(bands)*ha2eV
	
        return bands,proj_weight


def gau(x,x0,sigma):
    return 1/np.sqrt(2*np.pi)/sigma*np.exp(-((x-x0)/2/sigma)**2)

def main():
    data=parse_QE(sys.argv[1])
    print "atmproj.xml read successfully"
    band = data[0]
    phases = data[1]
    nkpt,norb,nband = phases.shape
    print 'nkpt, norb, nband',nkpt,norb,nband
    for i in band[0]:
	print i
    idim=0
    '''
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
    '''


    WF_map=np.loadtxt(wfmap_file)
    nband_s,dum=WF_map.shape
    nband_p=int(nband_s*V_p/V_s)
    '''
    for j in range(len(projorb)): # orbital index
        temp=[]
      	for i in projorb[j]:
             temp.append(orbitals.index(i))
      	orb_index.append(temp)
    '''
    fig=pl.figure(figsize=(4,6))
    ax=fig.add_subplot(111)

#    for i in range(nband):
#      ax.plot(band[:,i,ispin],c='k')

#    if len(projorb)>0:
    klist=np.arange(0,nkpt,1)
#      for i_at_type in range(len(projorb)):
    weight_plot=np.zeros((nkpt,nband),dtype=complex)

#          for i in range(nband):
#              for orb in  orb_index[i_at_type]:
#		  for ii,ion in enumerate(projion[i_at_type]):
			  
                          #weight_plot[:,i]+=weight[:,(ion)*norb+orb,i,0,ispin] \
    if len(WF_map)!= norb:
	print 'WF_map contains different number than norb!!'
	print 'WF_map',len(WF_map), 'norb',norb
	sys.exit(1)
    fout = open('unfolded_bands.dat','w')
    for i in range(nband):
        for ii in range(norb):
	    weight_plot[:,i]+=phases[:,ii,i] \
		    * (np.exp(-2j*np.pi*np.dot(kpath[:],WF_map[ii,2:])))
	    
    for ik in range(nkpt):
	print >> fout, klist[ik],
	for i in range(nband):
	    print >> fout, band[ik,i],abs(weight_plot[ik,i])**2,'  ',
	print >>fout,''
	#ax.scatter(klist,band[:,i],c='b',s=(abs(weight_plot[:,i])**2 *40),alpha=0.7,edgecolors='none')
    fout.close() 

#-------------------------------------------
#    pl.axhline(y=Ef,color='k')
    '''
    xticker=[]
    j=0
    for i in range(Nk):

      if LA.norm(Kpath[i][:3]-Kpts[j])<1e-5:
        xticker.append(i)
        j+=1
        pl.axvline(x=i,color='k')

    pl.ylabel('Energy(eV)')
    pl.xlim(0,len(klist)-1)
#    pl.ylim(-1,3.5)
  #pl.ylim(-10,5)
#xlabels = ["$\Gamma$","Z","T",'Y',"$\Gamma$",'X','S','R','U']
    ax.set_xticks(xticker)
    ax.set_xticklabels(xlabels)
    pl.legend(loc='best')
    
    pl.tight_layout()
    pl.show()
    fig.savefig('./band_int.png')
    '''

if __name__=='__main__':
   main()
    
    
