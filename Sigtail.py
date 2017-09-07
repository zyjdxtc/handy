from scipy import *
import scipy.interpolate as ip
import sys
from scipy.optimize import *
import pylab as pl

data = loadtxt(sys.argv[1])

def y(x,c):
   return c/x

popt,pcov = curve_fit(y,data[3000:,0],data[3000:,2])

print popt,pcov
fig = pl.figure()
ax=fig.add_subplot(111)
ax.plot(data[:,0],data[:,2])
ax.plot(data[:,0],y(data[:,0],popt[0]))
pl.show()

