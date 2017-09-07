import numpy as np
import pylab as pl
import sys

fig=pl.figure()
data=np.loadtxt('Sig.out')
pl.plot(data[:,0],data[:,-2])
pl.plot(data[:,0],data[:,-1])
#pl.xlim(-30,30)   
pl.show()
