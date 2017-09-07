from scipy import *
import sys
import pylab as pl
sig = loadtxt(sys.argv[1])
w = sig[:,0]
sigN = sig[:,1]+1j*sig[:,2]
sigA = sig[:,3] + 1j*sig[:,4]

gN = (w-0.5-sigN)/((w -0.5 -sigN)**2 )
gA = sigA/((w-0.5-sigN)**2 )
fout = open('green.out','w')
for i in range(len(w)):
    print >> fout, w[i], gN[i].real, gN[i].imag, gA[i].real, gA[i].imag

fout.close()

