#!/usr/bin/env python
import numpy as np
import pylab as pl

G=np.loadtxt('Gfr.out')

fig=pl.figure()

ax=fig.add_subplot(111)

A_eg=np.zeros(len(G[:,0]))
A_t2g=np.zeros(len(G[:,0]))
A_Op=np.zeros(len(G[:,0]))
for i in [0,3]:
   A_eg+=-1./np.pi*G[:,i*2+2]
ax.plot(G[:,0],A_eg,c='r')#eg
for i in [1,2,4]:
   A_t2g+=-1./np.pi*G[:,i*2+2]
ax.plot(G[:,0],A_t2g,c='b')#t2g
#for i in range(5,14):
#   A_Op+=-1./np.pi*G[:,i*2+2]
#ax.plot(G[:,0],A_Op,c='k')#Op
pl.show()
fig.savefig('./DOS.png')
