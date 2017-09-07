from scipy import *
import sys
import pylab as pl
sig = loadtxt(sys.argv[1])
w = sig[:,0]
g = 1./(w - sig[:,1] - sig[:,2]*1j)

fig= pl.figure()
ax = fig.add_subplot(111)

ax.plot(w,-g.imag/pi)
pl.show()
