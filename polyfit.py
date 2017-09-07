#from scipy import *
import sys
import numpy as np
import pylab as pl
data = np.loadtxt(sys.argv[1])
x= data[:,0]
y = data[:,1]
z = np.polyfit(x,y,6)
p = np.poly1d(z)
xr = np.linspace(x[0],x[-1],50)
fig = pl.figure()
ax = fig.add_subplot(111)
ax.plot(xr,p(xr))
ax.plot(x,y,'o')

pl.show()
fig.savefig('./fitting.pdf')
print z
