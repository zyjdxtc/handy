#plot e band structure from the EIGENVAL file.

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys,string

fname = sys.argv[1]  # EIGVALUE file
fermi=string.atof(sys.argv[2]) #fermi level
erange=float(sys.argv[3]) # plotting range from fermi level

f= open(fname,'r')
lines=f.readlines()
N=20 #points in each section
startline=1000 #a large number at beginning
spin=int(sys.argv[4]) #choose to plot band for spin 1 or 2 

fig=pl.figure()
n=-1
onekpt=[]
band=[]
kpt2=[]
i=0
while i<len(lines):
    temp=string.split(lines[i])
    if ((string.find(lines[i],'E')>0 and len(temp)==4)):
        kpt1=lines[i]
        startline=i
        n=n+1
        
        if (kpt2==kpt1):
            i=i+len(band[0])
            n=n-1
        kpt2=kpt1
        if len(onekpt)>1:
            band.append(onekpt)
            onekpt=[]
        num=n
#print startline
    elif(i>startline and len(temp)<4 and len(temp)>1):
      
        #print temp
        onekpt.append(string.atof(temp[spin])-fermi)
        if (i==len(lines)-1):
            band.append(onekpt)
    i=i+1
print len(band[-1]),len(band[0])
print num
bandstr=np.array(band)
for i in range(len(band[0])):
    if(erange != 0 and bandstr[0,i]>-1*erange and bandstr[0,i]<erange):
        pl.plot(bandstr[:,i],'k-')
    elif erange ==0:
        pl.plot(bandstr[:,i],'k-')
ax=fig.add_subplot(111)
pl.axhline(y=0)
xticker=[0]
for i in range(6):
    xticker.append((i+1)*(N-1))
    pl.axvline(x=(i+1)*(N-1))
xticker.append(len(xticker)*(N-1))

pl.xlabel('kpath')
pl.ylabel('Energy(eV)')
pl.title('Band structure near fermi energy')
pl.xlim(0,num)

#xlabels = ["$\Gamma$","Z","T",'Y',"$\Gamma$",'X','S','R','U']
xlabels= ["$\Gamma$","X","M",'$\Gamma$','A','R','Z','$\Gamma$']
ax.set_xticks(xticker)
ax.set_xticklabels(xlabels)
#ax.reset_ticks()
pl.show()    
