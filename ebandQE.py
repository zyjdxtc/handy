#plot e band structure from the EIGENVAL file.

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys,string
import numpy.linalg as LA
import  xml.etree.ElementTree as ET

fermi=string.atof(sys.argv[1]) #fermi level
erange=float(sys.argv[2]) # plotting range from fermi level

# read kpts
tree2 = ET.parse('data-file.xml')
root2 = tree2.getroot()
Nk = int(root2.find('.//NUMBER_OF_K-POINTS').text.split()[0])

b =  root2.find('.//RECIPROCAL_LATTICE_VECTORS')
bvec = []
for line in b[1:]:
    bvec.append([ float(i) for i in line.text.split() ])
bvec = np.array(bvec)


kpts = []
for i in range(Nk):
   n = root2.find('.//K-POINT.'+str(i+1)).attrib
   kpts.append([float(i) for i in n['XYZ'].split()])
kpts = np.array(kpts)
kpts_reduce = np.dot(kpts,LA.inv(bvec))


eigs = []
ha2eV=27.2114

for i in range(Nk):
    ik = str(i+1)
    ik = 'K' + '0'*(5-len(ik))+ik
    tree = ET.parse(ik+'/eigenval.xml')
    root = tree.getroot()
    
    eig0 = root.find('.//EIGENVALUES').text.split()
    tempE = [float(ie) for ie in eig0] 
    eigs.append(tempE)
eigs=np.array(eigs)*ha2eV
dum,nb = eigs.shape
# plotting
fig=pl.figure()
ax=fig.add_subplot(111)
for i in range(nb):
    ax.plot(eigs[:,i],'k-')


#pl.axhline(y=0)

#kpath=np.array([[0,0,0],[0.5,0.,0],[0.5,0.5,0],[0,0,0]])
#kpath=np.array([[0,0,0],[0.5,0.,0],[0.5,0.5,0],[0,0,0],[0,0,0.5]])
#kpath=np.array([[0.0,0.5,0],[0.,0.,0.],[0.,0.,0.5],[0.5,0.,0.5],[0.5,0.,0.],[0.,0.,0.],[0.5,0.5,0.]])
kpath=np.array([[0.0,0.5,0],[0.,0.,0.],[0.5,0.,0.],[0.5,0.5,0.],[0.,0.,0.],\
		[0.,0.,0.5],[0.5,0.,0.5],[0.5,0.5,0.5],[0,0,0]])

xticker=[]
j=0

print kpts_reduce
for i in range(Nk):
    if LA.norm(kpts_reduce[i]-kpath[j])<1e-4:
    	xticker.append(i)
	j+=1
    #	pl.axvline(x=i)

#pl.xlabel('kpath')
pl.ylabel('Energy(eV)')
#pl.title('Band structure near fermi energy')
pl.xlim(0,Nk)

pl.ylim(-erange,erange)
xlabels = ['Y',"$\Gamma$","X","M",'$\Gamma$','Z','B','R','$\Gamma$']
#xlabels= ["$\Gamma$","X","M",'$\Gamma$','Y']

ax.set_xticks(xticker)
ax.set_xticklabels(xlabels)

#ax.reset_ticks()

pl.show()    
fig.savefig('band.png')
