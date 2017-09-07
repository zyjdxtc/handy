import xml.etree.ElementTree as ET
from scipy import *
import numpy as np
#from parse import *

def readE(xmlfile):
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	kpts = root[2][0]
	kpoints=[]
	# get kpoints
	#for i in kpts:
	#    kpoints.append([float(j) for j in i.text.split()])

	# get bands
	eigs = root[6][-4][0][5][0]
	Nk =  len(eigs)
	proj = root[6][-1][1][-1][0] 
	# nk * nband * natom * nproj_orb
	##dxy, dyz, dxz = 4,5,7
	eig_t2g=[]
	efermi = float(root.findall('.//dos')[0][0].text)
	for ik,k in enumerate(eigs):
	    '''
	    nbands = len(k)
	    local_e = [0,0,0]
	    for i in range(nbands-4,nbands-1):
	    	localene = float(k[i].text.split()[0])
		weight = [ float(ni) for ni in proj[ik][i][1].text.split()]
		localm = max(weight)
		ind = weight.index(localm)
		print 'k=',ik, 'ib=',i, weight, ind 
		if ind==dxy:
		   local_e[0] = localene
		elif ind==dyz:
		   local_e[1] = localene
		elif ind ==dxz:
		   local_e[2] = localene
	    eig_t2g.append(local_e)
	    '''
	    eig_t2g.append([float(i.text.split()[0]) for i in k])
	    
	return array(eig_t2g),Nk,efermi
def gauss(x,x0,sigma):
    return np.exp(-(x-x0)*(x-x0)/2/sigma/sigma)

def deriv(ene,ef,disp):
    dEdu =[]
    ndisp, nk, nband = ene.shape
    for i in range(1,ndisp-1):
	tot = np.zeros(nk)
	for ie in range(nband):
	    Ei = ene[i-1][:,ie]
	    for iep in range(nband):
		Eip = ene[i+1][:,iep]
		#if all(abs(eip - ef) < 1. for eip in Eip) and all(abs(ei-ef)<1. for ei in Ei):
		tot += (Eip-Ei)/(disp[i+1]-disp[i-1])\
			*gauss(Eip,ef,0.1)*gauss(Ei,ef,0.1)
	# tot dim = (nk,)
	dEdu.append(tot)	

		
#	dEdu.append((ene[i+1] - ene[i-1])/(disp[i+1]-disp[i-1])\
#			*gauss(ene[i+1],ef,0.1)*gauss(ene[i-1],ef,0.1))
	
    return array(dEdu)

if __name__ == '__main__':
    disp=[-0.0889753728792*5 + 0.0889753728792*i for i in range(11)]
    #disp=[-0.0784022796151*5 + 0.0784022796151*i for i in range(11)]
    d =['-5','-4','-3','-2','-1','1','2','3','4','5']
    eig_t2g = []
    ef = 0
    # read eigenvalues for t2g bands
    modes =[13,14,15]
    for m in modes:
        eig_t2g.append([])
        for i in d:
            ene,Nk,efermi = readE('./mode.'+str(m)+'.'+i+'/vasprun.xml')
            #ene,Nk = readPROCAR('./disp'+i+'/PROCAR0')
            eig_t2g[-1].append(ene)
            #ef.append(efermi)
        Eundis,Nk,ef = readE('../../static/vasprun.xml')
        eig_t2g[-1].insert(5,Eundis) # insert
    eig_t2g=array(eig_t2g)
    # derivative
    dEdu_t = []
    print 'eig_t2g shape = ', eig_t2g.shape
    nmode, ndisp, nk, nband = eig_t2g.shape
    # eig_t2g dim = nmode x ndisp x nk x nband
    for m in range(len(eig_t2g)):
        dEdu = deriv(eig_t2g[m],ef,disp)
	# dEdu dim (ndisp,Nk,)
        dEdu_t.append( np.sum(dEdu,axis = 1) / Nk ) # sum over kpts, resulting n_disp x norb dimension
    dEdu_t = np.array(dEdu_t)
    # dEdu_t dim = nmode x ndisp 
    dEdu_tot = np.sum(dEdu_t,axis = 0)/len(dEdu_t)
    # summed over nmode, leaving ndisp 
    print dEdu_tot
    f = open('tot_coupling.dat','w')
    for i in range(len(dEdu_t[0])):
 	print >> f, disp[i+1], 
	
        #for m in range(len(dEdu_t)):
	#    n = dEdu_t[m][i]
	#    print >>f, sum(n)*nband/2/3,
	print >>f, dEdu_tot[i] #sum(dEdu_tot[i])*nband/2/3

		#   disp, 	t2g_1, t2g_2, t2g_3
    f.close()
   
