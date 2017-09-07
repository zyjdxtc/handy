tar xzvf xml1.tgz
awk 'BEGIN{i=1} /imag/,\
                /\/imag/ \
                 {a[i]=$2 ; b[i]=$5 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' vasprun.xml > imag.dat

awk 'BEGIN{i=1} /real/,\
                /\/real/ \
                 {a[i]=$2 ; b[i]=$5 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' vasprun.xml > real.dat

#cat >plotfile<<!
# set term postscript enhanced png colour lw 2 "Helvetica" 20
# set output "optics.png"
#plot [0:25] "imag.dat" using (\$1):(\$2) w lp, "real.dat" using (\$1):(\$2) w lp
#!

#cat >optics.py<<!
#import numpy as np
#import pylab as pl

#f1=open('real.dat','r')
#f2=open('imag.dat','r')

#real=np.loadtxt(f1)
#imag=np.loadtxt(f2)

#l1,l2=real.shape
#n=np.zeros((l1,l2))
#R=np.zeros((l1,l2))

#absorbtion=np.zeros((l1,l2))
#absorbtion[:,0]=real[:,0]
#n[:,0]=real[:,0]
#n[:,1]=np.sqrt(0.5*(real[:,1]+np.sqrt(real[:,1]**2+imag[:,1]**2)))

#R[:,0]=3e8/(real[:,0]/6.63e-34*1.6e-19)*1e9
#R[:,1]=((1-n[:,1])/(1+n[:,1]))**2

#absorbtion[:,1]=4*np.pi*imag[:,1]/R[:,0]/1e7

#fig=pl.subplot(121)


#pl.plot(real[:,0],real[:,1],label='real')
#pl.plot(imag[:,0],imag[:,1],label='imag')
#fig.plot(R[:,0],1-R[:,1])
#fig.set_xlim([0,1000])
#fig.set_ylim([0,1])
#fig.set_xlabel('Wavelengh (nm)')
#fig.set_ylabel('T')

#fig2=pl.subplot(122)
#fig2.plot(absorbtion[:,0],absorbtion[:,1])
#fig2.set_xlim([0,10])
#fig2.set_ylim([0,1])
#fig2.set_xlabel('h$\omega$ (eV)')
#fig2.set_ylabel('Absorbtion (cm$^{-1}$)')


#pl.show()

#!
#python optics.py

rm vasprun.xml
#gnuplot -persist plotfile
