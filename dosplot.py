import numpy as np
import pylab as pl
import sys
f=sys.argv[1]
data=np.loadtxt(f,skiprows=1)

fig=pl.figure()
ax=fig.add_subplot(111)

ax.plot(data[:,0],data[:,1],c='k',linewidth=1.5)
ax.plot(data[:,0],data[:,2],c='r',linewidth=1.5)
ax.set_xlabel('E (eV)')
ax.set_ylabel('DOS')
ax.set_ylim([min(data[:,2])-1,max(data[:,1])+1])
ax.set_xlim([-2,2])
ax.axvline(x=0,c='k')
pl.show()
