import numpy as np
import pylab as pl
import sys

fig=pl.figure()
for i in range(1,31):
   data=np.loadtxt('Sig.out.'+str(i)+'.1')
   pl.plot(data[:,0],data[:,1])
pl.xlim(0,10)   
pl.show()
