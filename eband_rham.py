from scipy import *
import pylab as pl
from kpath import k_path
import numpy.linalg as LA
import sys
from scipy.special import erf
from scipy.integrate import *
#from rham import Hopping
execfile('./rham.py')
def getDOS(Hopping,nkx,nky,nkz):
    print "-------------------DOS calculation-----------------"
    kx=linspace(-0.5+0.5/nkx,0.5-0.5/nkx,nkx)
    ky=linspace(-0.5+0.5/nky,0.5-0.5/nky,nky)
    kz=linspace(-0.5+0.5/nkz,0.5-0.5/nkz,nkz)
    ks=[]
    for kxi in kx:
       for kyi in ky:
          for kzi in kz:
	     ks.append([kxi,kyi,kzi])
    ks=array(ks)
    nedos=2001
    Emin=-5
    Emax=0
    omega=linspace(Emin,Emax,nedos)

    sigma=0.1
    cshift=0.05 
   #epsilon2=[]
    fout=open("dos.out",'w')
    dos=[0]*nedos
    dw=omega[1]-omega[0]
    norb1=len(Hopping[(0,0,0)])
    for ik,k in enumerate(ks):
    	ham = zeros((norb1,norb1),dtype=complex)
        for i,ii in enumerate(sorted(Hopping.keys())):
           ham+=array(Hopping[ii])*exp(2j*pi*dot(k,array(ii)))
  	curE=LA.eigvalsh(ham)
	for Ei in curE:
	    imin=int((Ei-8*sigma-Emin) / dw)
	    imax=int((Ei+8*sigma-Emin) / dw+1)
	    if imin<0:
		imin=0
	    if imin>nedos:
		imin=nedos
	    if imax<1:
		imax=1
	    if imax>nedos:
		imax=nedos
	    ef_done=0
	    for j in range(imin,imax):
		dE=Emin+dw*(j)-Ei
		ef=0.5+0.5*erf((dE+dw/2)/sigma)
		effdos=(ef-ef_done)/dw
		if j>=0:
		   dos[j]+=effdos
		ef_done = ef
    dos = array(dos)
    dos/=nkx*nky*nkz
    for i,iw in enumerate(omega):
       print >> fout, iw, dos[i]
    fout.close()
    return omega,dos
   
norb1 = len(Hopping[(0,0,0)])
lat=array([[1,0,0],[0,1,0],[0,0,2]])
k=array([[0,0,0],[0.0,0.5,0.],[0.5,0.50,0],[0.,0.,0.]])
kp = k_path(k,lat)
ham = zeros((len(kp),norb1,norb1),dtype=complex)
evals = zeros((len(kp),norb1))
print kp
for ik in range(len(kp)):
    for i,ii in enumerate(sorted(Hopping.keys())):
        ham[ik]+=array(Hopping[ii])*exp(2j*pi*dot(kp[ik],array(ii)))
    evals[ik] += LA.eigvalsh(ham[ik])		

Ef=float(sys.argv[1])
fig=pl.figure()
ax=fig.add_subplot(111)
for i in range(norb1):
   ax.plot(evals[:,i],'o-',c='k')

ax.axhline(y=Ef,c='k')
xticker=[]
j=0
for i in range(len(kp)):

    if LA.norm(kp[i]-k[j])==0:
        xticker.append(i)
        j+=1
        pl.axvline(x=i)

#pl.xlabel('kpath')
pl.ylabel('Energy(eV)')
#pl.title('Band structure near fermi energy')
pl.xlim(0,len(kp))

#xlabels = ["$\Gamma$","A","H",'K',"$\Gamma$",'M','L']
xlabels= ["$\Gamma$","X","M",'$\Gamma$']
#xlabels= ['E0',"$\Gamma$",'D',"Y",'\$Gamma','X',"A",'$\Gamma$','D']
ax.set_xticks(xticker)
ax.set_xticklabels(xlabels)

#fig2=pl.figure()
#ax2=fig2.add_subplot(111)
#omega,dos = getDOS(Hopping,12,12,12)
#tdos=simps(dos[:990],omega[:990])

#print 'tdos=',tdos
#ax2.plot(dos[:,0],dos[:,1])

pl.show()
