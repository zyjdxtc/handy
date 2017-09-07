from scipy import *
import sys
import pylab as pl

Sig = loadtxt(sys.argv[1])
g = 1.0/(Sig[:,0] - Sig[:,1] -1j*Sig[:,2])

fig = pl.figure()
ax=fig.add_subplot(111)

ax.plot(Sig[:,0], -1./pi*g.imag)
pl.show()

