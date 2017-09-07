import pylab as pl
import numpy as np
import sys
import string as st

fname=sys.argv[1]
bandlist=[]
for line in reversed(open(fname,'r').readlines()): 
     temp=line.split()
     if len(temp)==2:
	break
     elif len(temp)==3:
     	bandlist.append([float(temp[0]),float(temp[1]),float(temp[2])])
bandlist=np.array(bandlist)
fig=pl.figure()
ax=fig.add_subplot(111)
pl.scatter(bandlist[:,0], bandlist[:,1],s=15, c=bandlist[:,2],vmin=0,vmax=1,edgecolors='none')	
ax.ylim=(-100,100)
pl.colorbar()
xlabels= ["$\Gamma$","X","M","$\Gamma$","A","R","Z","$\Gamma$"]
xticker=np.linspace(min(bandlist[:,0]),max(bandlist[:,0]),len(xlabels))
ax.set_xticks(xticker)
ax.set_xticklabels(xlabels)

pl.show()
